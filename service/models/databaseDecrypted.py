from service.models.entry import Entry


class DatabaseDecrypted(object):
    def __init__(self, decrypted: dict):
        self._dictionary = decrypted
        return

    def get_dict(self):
        return self._dictionary

    def new_group(self, group) -> dict:
        if group in self._dictionary.keys():
            raise KeyError("group already exists")

        self._dictionary[group] = {}

        return self._dictionary[group]

    def get_group(self, group) -> list:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        return list(self._dictionary[group].keys())

    def delete_group(self, group) -> dict:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        g = self._dictionary[group]
        del self._dictionary[group]

        return g

    def new_entry(self, group, entry: Entry) -> dict:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        entry_name = entry.name

        if entry_name in self._dictionary[group].keys():
            raise KeyError("entry already exist")

        self._dictionary[group][entry_name] = entry.to_dict()

        return self._dictionary[group][entry_name]

    def edit_entry(self, group, entry: Entry) -> dict:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        entry_name = entry.name

        if entry_name not in self._dictionary[group].keys():
            raise KeyError("entry does not exist")

        self._dictionary[group][entry_name] = entry.to_dict()

        return self._dictionary[group][entry_name]

    def get_entry(self, group, entry_name: str) -> dict:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        if entry_name not in self._dictionary[group].keys():
            raise KeyError("entry does not exist")

        return self._dictionary[group][entry_name]

    def delete_entry(self, group, entry_name: str) -> dict:
        if group not in self._dictionary.keys():
            raise KeyError("group not found")

        if entry_name not in self._dictionary[group].keys():
            raise KeyError("entry does not exist")

        e = self._dictionary[group][entry_name]
        del self._dictionary[group][entry_name]

        return e
