import json
from base64 import encodebytes, decodebytes
from datetime import datetime
from hashlib import md5
from pathlib import Path

from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Random import get_random_bytes

from service.config.config import config
from service.models.directory import TYPE_DIRECTORY


class DatabaseFile(object):
    # the path where to find the database file
    path: Path = None

    # the master key derived
    master_key_derived: bytes = None

    # salt used for key derivation
    salt: bytes = None

    def __init__(self, path: str, master_key_raw: str):
        """
        open db file and read its fields
        :param path: location of the db file
        :param master_key_raw: key used for encryption/decryption of db
        """
        self.path = Path(path)

        if not self.path.exists() or not self.path.is_file():
            raise FileNotFoundError

        initialized = True
        with self.path.open("r") as f:
            content = f.read()
            if content == "":
                initialized = False

        def base64_decode(att: str):
            return decodebytes(att.encode())

        if initialized:
            # get the file fields
            j = json.loads(content)
            self.encrypted = base64_decode(j['encrypted'])
            self.nonce = base64_decode(j['nonce'])
            self.salt = base64_decode(j['salt'])

            self.master_key_derived = self.key_derivation(master_key_raw)
        else:
            # if file empty, init a new db
            self.reset(master_key_raw)

    def reset(self, master_key_raw):
        self.salt = get_random_bytes(16)
        self.master_key_derived = self.key_derivation(master_key_raw)

        self.write({
            "type": TYPE_DIRECTORY,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
            "content": {}
        })

    def write(self, decrypted: dict):
        """
        encrypt and write content into db file
        :param decrypted: plain text dict
        :return:
        """
        self.encrypt(decrypted)

        def base64_encode(att: bytes) -> str:
            return encodebytes(att).decode()

        j = {
            "nonce": base64_encode(self.nonce),
            "salt": base64_encode(self.salt),
            "encrypted": base64_encode(self.encrypted),
        }

        jd = json.dumps(j, indent=4, separators=(',', ': '))

        with self.path.open("w") as f:
            f.write(jd)

    def key_derivation(self, master_key_raw) -> bytes:
        """
        derive master key to make dictionary attack computational difficult
        :param master_key_raw: the master key
        :return: the derived master key
        """
        d = bcrypt(master_key_raw, config.crypto['key_derivation_cost'], salt=self.salt)

        # use md5 to make the derived key 32 byte length for ChaCha algorithm
        return md5(d).hexdigest().encode()

    def encrypt(self, decrypted: dict) -> (bytes, bytes):
        """
        encrypts a dictionary
        :param decrypted: the dict to encrypt
        :return: encrypted raw data and nonce
        """
        decrypted_data: bytes = json.dumps(decrypted).encode()

        self.nonce = get_random_bytes(12)
        cipher = ChaCha20.new(key=self.master_key_derived, nonce=self.nonce)
        self.encrypted = cipher.encrypt(decrypted_data)

    def decrypt(self) -> dict:
        cipher = ChaCha20.new(key=self.master_key_derived, nonce=self.nonce)
        plain = cipher.decrypt(self.encrypted)
        return json.loads(plain)
