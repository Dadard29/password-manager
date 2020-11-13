class Entry(object):

    def __init__(self, name: str, d: dict):
        self.name = name
        self.value = d['value']
        self.metas = d['metas']

    def to_dict(self):
        return dict(
            value=self.value,
            metas=self.metas
        )
