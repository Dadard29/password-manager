from datetime import datetime

from service.models.entry import TYPE_ENTRY, Entry
from service.models.utils import get_current_date

TYPE_DIRECTORY = 'directory'

"""
Example
{
    "type": "directory",
    "content": {
        "SUB_DIR_1": {
            "type": "directory",
            "content": ...
        },
        "SUB_DIR_2": {
            "type": "directory",
            "content": ...
        },
        "ENTRY_1": {
            "type": "entry",
            "content": {
                "value": "some_value",
                "metas": {
                    "meta_label_1": "meta_value_1",
                    ...
                }
            }
        }
    }
}
"""


class Directory(object):
    type = TYPE_DIRECTORY

    def __init__(self, name: str, body: dict):
        if body['type'] != TYPE_DIRECTORY:
            raise TypeError('cant parse non-directory object')

        self.name = name

        self.created_at = body['created_at']
        self.updated_at = body['updated_at']

        self._content = {}
        for k in body['content'].keys():
            k_object = body['content'][k]
            if k_object['type'] == TYPE_DIRECTORY:
                self._content[k] = Directory(k, k_object)
            elif k_object['type'] == TYPE_ENTRY:
                self._content[k] = Entry(k, k_object)

    def to_dict(self):
        content_d = dict()
        for k in self._content:
            content_d[k] = self._content[k].to_dict()

        return dict(
            type=self.type,
            created_at=self.created_at,
            updated_at=self.updated_at,
            content=content_d
        )

    # entries
    def new_entry(self, entry: Entry) -> Entry:
        if entry.name in self._content.keys():
            raise KeyError(f'name `{entry.name}` already exists')

        self._content[entry.name] = entry

        return entry

    def get_entry(self, entry_name: str) -> Entry:
        if entry_name not in self._content.keys():
            raise KeyError(f'entry `{entry_name}` does not exists')

        entry = self._content[entry_name]
        if not entry.type == TYPE_ENTRY:
            raise TypeError("the requested entry is a directory")

        return entry

    def update_entry(self, entry_name: str, entry_content: dict) -> Entry:
        if entry_name not in self._content.keys():
            raise KeyError(f'entry `{entry_name}` does not exists')

        e = self.get_entry(entry_name)
        e.updated_at = get_current_date()
        e.value = entry_content['value']
        e.metas = entry_content['metas']

        return e

    def delete_entry(self, entry_name: str) -> Entry:
        if entry_name not in self._content.keys():
            raise KeyError(f'entry `{entry_name}` does not exists'
                           )
        entry = self.get_entry(entry_name)

        del self._content[entry_name]
        return entry

    # sub directories
    def new_directory(self, directory_name: str):
        if directory_name in self._content.keys():
            raise KeyError(f'name `{directory_name}` already exists')

        new_directory = Directory(directory_name, dict(
            type=TYPE_DIRECTORY,
            created_at=get_current_date(),
            updated_at=get_current_date(),
            content=dict()
        ))

        self._content[directory_name] = new_directory

        return new_directory

    def get_directory(self, directory_name: str):
        if directory_name not in self._content.keys():
            raise KeyError(f"name `{directory_name}` does not exists")

        directory = self._content[directory_name]
        if directory.type != TYPE_DIRECTORY:
            raise TypeError("the requested directory is an entry")

        return directory

    def delete_directory(self, directory_name: str):
        if directory_name not in self._content.keys():
            raise KeyError(f'directory `{directory_name}` does not exists'
                           )
        directory = self.get_directory(directory_name)
        if directory.type != TYPE_DIRECTORY:
            raise TypeError("the requested directory is an entry")

        del self._content[directory_name]
        return directory

    def ls(self) -> list:
        ls = []
        for k in self._content.keys():
            o = self._content[k]
            ls.append(dict(
                type=o.type,
                name=o.name,
                created_at=o.created_at,
                updated_at=o.updated_at,
                size=str(o.count()) if o.type == TYPE_DIRECTORY else '-'
            ))

        sorted_ls = sorted(ls, key=lambda i: i['type'])
        return sorted_ls

    def count(self) -> int:
        return len(self._content.keys())

