from pathlib import Path


class Database(object):

    # the location of the db file, where to write secrets
    path = Path()

    def __init__(self, file_path):
        self.path = Path(file_path)

