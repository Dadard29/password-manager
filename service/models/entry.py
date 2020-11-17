from datetime import datetime

TYPE_ENTRY = 'entry'


class Entry(object):

    type = TYPE_ENTRY

    def __init__(self, name: str, d: dict):
        self.name = name
        if d['type'] != TYPE_ENTRY:
            raise TypeError("cant parse non-entry objects")

        self.created_at = d['created_at']
        self.updated_at = d['updated_at']

        content = d['content']
        self.value = content['value']
        self.metas = content['metas']

    def to_dict(self):
        return dict(
            type=self.type,
            created_at=self.created_at,
            updated_at=self.updated_at,
            content=dict(
                value=self.value,
                metas=self.metas
            )
        )
