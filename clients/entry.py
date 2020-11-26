class Entry(object):
    def __init__(self, json: dict):
        self.created_at = json['created_at']
        self.updated_at = json['updated_at']
        content = json['content']
        self.metas = content['metas']
        self.value = content['value']

        k = 'created_with_cli'
        if k in self.metas.keys():
            self.created_with_cli = self.metas[k] == 'true'
        else:
            self.created_with_cli = False
