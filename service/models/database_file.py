import json
from base64 import encodebytes, decodebytes, b64decode, b64encode
from datetime import datetime
from hashlib import md5
from pathlib import Path

from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Random import get_random_bytes

from config.config import config
from models.directory import TYPE_DIRECTORY
from models.utils import get_current_date

SALT_LENGTH = 16
NONCE_LENGTH = 12


class DatabaseFile(object):
    # the path where to find the database file
    path: Path = None

    # the master key derived
    master_key_derived: bytes = None

    # salt used for key derivation
    salt: bytes = None

    # encrypted content
    encrypted: bytes = None

    # nonce used for encryption
    nonce: bytes = None

    def __init__(self, path: str):
        """
        open db file and read its fields
        :param path: location of the db file
        """
        self.path = Path(path)

        if not self.path.exists() or not self.path.is_file():
            raise FileNotFoundError

        self.unload()

    def unload(self):
        self.salt = b''
        self.nonce = b''
        self.encrypted = b''
        self.master_key_derived = b''

    def load(self, master_key_raw: str):

        initialized = True
        with self.path.open("rb") as f:
            content = f.read()
            if content == b'':
                initialized = False

        if initialized:
            # get the file fields
            self.salt = content[:SALT_LENGTH]
            self.nonce = content[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
            self.encrypted = content[SALT_LENGTH + NONCE_LENGTH:]

            self.master_key_derived = self.key_derivation(master_key_raw)
        else:
            # if file empty, init a new db
            self.reset(master_key_raw)

        return self._decrypt()

    def reset(self, master_key_raw):
        self.salt = get_random_bytes(SALT_LENGTH)
        self.master_key_derived = self.key_derivation(master_key_raw)

        self.write({
            "type": TYPE_DIRECTORY,
            "created_at": get_current_date(),
            "updated_at": get_current_date(),
            "content": {}
        })

    def write(self, decrypted: dict):
        """
        encrypt and write content into db file
        :param decrypted: plain text dict
        :return:
        """
        self._encrypt(decrypted)

        content = self.salt + self.nonce + self.encrypted

        with self.path.open("wb") as f:
            f.write(content)

    def key_derivation(self, master_key_raw) -> bytes:
        """
        derive master key to make dictionary attack computational difficult
        :param master_key_raw: the master key
        :return: the derived master key
        """
        d = bcrypt(master_key_raw, config.crypto['key_derivation_cost'], salt=self.salt)

        # use md5 to make the derived key 32 byte length for ChaCha algorithm
        return md5(d).hexdigest().encode()

    def _encrypt(self, decrypted: dict) -> (bytes, bytes):
        """
        encrypts a dictionary
        :param decrypted: the dict to encrypt
        :return: encrypted raw data and nonce
        """
        decrypted_data: bytes = json.dumps(decrypted).encode()

        self.nonce = get_random_bytes(NONCE_LENGTH)
        cipher = ChaCha20.new(key=self.master_key_derived, nonce=self.nonce)
        self.encrypted = cipher.encrypt(decrypted_data)

    def _decrypt(self) -> dict:
        cipher = ChaCha20.new(key=self.master_key_derived, nonce=self.nonce)
        plain = cipher.decrypt(self.encrypted)
        return json.loads(plain)
