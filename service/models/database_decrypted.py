from datetime import datetime

from service.models.directory import Directory, TYPE_DIRECTORY
from service.models.entry import Entry


class DatabaseDecrypted(object):
    def __init__(self, decrypted: dict):

        # simulate the root directory
        self.tree = Directory('root', decrypted)
        return

    # utils
    def get_dict(self):
        return self.tree.to_dict()

    def access_path(self, path: str) -> Directory:
        if path == '':
            return self.tree

        path_list = path.split('/')

        rv = self.tree
        for p in path_list:

            rv = rv.get_directory(p)

        return rv

    # entries
    def new_entry(self, path: str, entry: Entry):
        d = self.access_path(path)
        d.new_entry(entry)

        return entry.to_dict()

    def get_entry(self, path: str, entry_name: str):
        d = self.access_path(path)
        return d.get_entry(entry_name).to_dict()

    def update_entry(self, path: str, entry_name: str, entry_content):
        d = self.access_path(path)
        return d.update_entry(entry_name, entry_content).to_dict()

    def delete_entry(self, path: str, entry_name: str):
        d = self.access_path(path)
        return d.delete_entry(entry_name).to_dict()

    # directories
    def new_directory(self, path: str, dir_name: str):
        d = self.access_path(path)
        return d.new_directory(dir_name).to_dict()

    def get_directory(self, path: str, dir_name: str) -> list:
        d = self.access_path(path)
        if dir_name == '':
            return self.tree.ls()

        d_to_list = d.get_directory(dir_name)
        return d_to_list.ls()

    def delete_directory(self, path: str, dir_name: str):
        d = self.access_path(path)
        return d.delete_directory(dir_name).to_dict()
