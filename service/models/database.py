import json
from base64 import b64decode
from pathlib import Path
from Crypto.Protocol.KDF import bcrypt

from service.config.config import config



# serialize fields from the db file
class DatabaseFile(object):
    # the SHA256 hash of the master key
    master_key = None

    # the path where to find the database file
    path: Path = None

    # tells if the database is initialized
    initialize: bool = None

    # the encrypted content of the database
    encrypted: bytes = None

    def __init__(self, path: str, master_key: str):
        self.path = Path(path)
        self.master_key = master_key

        if not self.path.exists() or not self.path.is_file():
            raise FileNotFoundError

        with self.path.open("r") as f:
            j = json.loads(f.read())

        self.initialized = j['initialized']
        if self.initialized:
            self.encrypted = b64decode(j['encrypted'].encode())
            self.nonce = b64decode(j['nonce'].encode())
        else:
            self.encrypted = b''
            self.nonce = b''

    # erase the current file content and put an empty database
    def reset(self):
        self.write({})


    def write(self, decrypted: dict):
        self.encrypted, self.nonce = self._encrypt(decrypted)

        j = {
            "initialized": True,
            "nonce": self.nonce,
            "encrypted": self.encrypted,
        }

        jd = json.dumps(j, indent=4)

        with self.path.open("w") as f:
            f.write(jd)


    @staticmethod
    def key_derivation(master_key_raw) -> bytes:
        return bcrypt(master_key_raw, config.crypto['key_derivation_cost'])


    @staticmethod
    def _encrypt(decrypted: dict) -> bytes:
        decrypted_data = json.dumps(decrypted)



class DatabaseDecrypted(object):
    def __init__(self):
        return


class Database(object):
    # the location of the db file, where to write secrets
    file: DatabaseFile = None
    decrypted: DatabaseDecrypted = None

    def __init__(self, file_path, master_key):
        self.file = DatabaseFile(file_path, master_key)


    def decrypt(self):


