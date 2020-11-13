from datetime import datetime
from service.models.databaseDecrypted import DatabaseDecrypted
from service.models.databaseFile import DatabaseFile


class Database(object):
    # the location of the db file, where to write secrets
    file: DatabaseFile = None

    # the decrypted entries
    decrypted: DatabaseDecrypted = None

    # tells if the decrypted data is available
    loaded = False

    # last save time, lost if the service restart
    updated_at = datetime.now()

    def __init__(self, file_path, master_key):
        # open database file
        self.file = DatabaseFile(file_path, master_key)

        # only load decrypted values when asked to
        self.decrypted = None

        self.loaded = False

    def load(self):
        decrypted_data = self.file.decrypt()
        self.decrypted = DatabaseDecrypted(decrypted_data)
        self.loaded = True

    def unload(self):
        self.decrypted = None
        self.loaded = False

    def save(self):
        self.updated_at = datetime.now()
        self.file.write(self.decrypted.get_dict())
