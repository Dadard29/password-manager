import click


class Parser(object):
    def get_group_entry(self):
        return

    @staticmethod
    def get_metas() -> dict:
        metas = dict()
        while True:
            print('Add a metadata to this entry (press Enter to skip)')
            label = click.prompt('label', type=str, default='')
            if label == '':
                print()
                return metas

            value = click.prompt('value', type=str, default='')
            if value == '':
                print()
                return metas

            metas[label] = value
