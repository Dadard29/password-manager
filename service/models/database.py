from datetime import datetime

from models.database_decrypted import DatabaseDecrypted
from models.database_file import DatabaseFile


class Database(object):
    # the location of the db file, where to write secrets
    file: DatabaseFile = None

    # the decrypted entries
    decrypted: DatabaseDecrypted = None

    # tells if the decrypted data is available
    loaded = False

    # last save time, lost if the service restart
    updated_at = datetime.now()

    def __init__(self, file_path):
        # open database file
        self.file = DatabaseFile(file_path)

        # only load decrypted values when asked to
        self.decrypted = None

        self.loaded = False

    def load(self, master_key):
        decrypted_data = self.file.load(master_key)
        self.decrypted = DatabaseDecrypted(decrypted_data)
        self.loaded = True

    def unload(self):
        self.file.unload()
        self.decrypted = None
        self.loaded = False

    def save(self):
        if self.decrypted is None:
            return

        self.updated_at = datetime.now()
        self.file.write(self.decrypted.get_dict())
