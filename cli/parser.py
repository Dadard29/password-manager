import click


class Parser(object):

    @staticmethod
    def get_master_key():
        return click.prompt('master key', hide_input=True, type=str)

    @staticmethod
    def get_entry_value():
        return click.prompt(
            'Enter the entry\'s value', hide_input=True,
            confirmation_prompt=True)

    @staticmethod
    def update_metas(metas) -> dict:
        while True:
            print('Add or update a metadata (press `enter` to skip)')
            label = click.prompt('label', type=str, default='')
            if label == '':
                print()
                return metas

            value = click.prompt('value', type=str, default='')
            if value == '':
                print()
                return metas

            metas[label] = value

    @staticmethod
    def get_metas() -> dict:
        return Parser.update_metas({})
