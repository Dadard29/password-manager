import json
from hashlib import md5
from pathlib import Path

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

from models.directory import TYPE_DIRECTORY
from models.utils import get_current_date

NONCE_LENGTH = 12


class DatabaseFile(object):
    # the path where to find the database file
    path: Path = None

    # key used for enc/dec
    key: bytes = None

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
        self.nonce = b''
        self.encrypted = b''
        self.key = b''

    def load(self, key_raw: int):

        initialized = True
        with self.path.open("rb") as f:
            content = f.read()
            if content == b'':
                initialized = False

        self.key = self.key_hash(key_raw)

        if initialized:
            # get the file fields
            self.nonce = content[:NONCE_LENGTH]
            self.encrypted = content[NONCE_LENGTH:]
        else:
            # if file empty, init a new db
            self.reset()

        return self._decrypt()

    def reset(self):
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

        content = self.nonce + self.encrypted

        with self.path.open("wb") as f:
            f.write(content)

    @staticmethod
    def key_hash(key_raw: int) -> bytes:
        """
        hash key raw to hash to enable decryption
        :param key_raw: the master key
        :return: the hashed master key
        """

        # use md5 to make the key 32 bytes length for ChaCha algorithm
        return md5(
            str(key_raw).encode()
        ).hexdigest().encode()

    def _encrypt(self, decrypted: dict) -> (bytes, bytes):
        """
        encrypts a dictionary
        :param decrypted: the dict to encrypt
        :return: encrypted raw data and nonce
        """
        decrypted_data: bytes = json.dumps(decrypted).encode()

        self.nonce = get_random_bytes(NONCE_LENGTH)
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        self.encrypted = cipher.encrypt(decrypted_data)

    def _decrypt(self) -> dict:
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        plain = cipher.decrypt(self.encrypted)
        return json.loads(plain)
