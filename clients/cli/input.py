import click

from diffie_hellman import gen_public_key
from parsing import Parser


class Input(object):
    @staticmethod
    def get_public_key() -> (int, bytes):
        private_key = click.prompt('private key', hide_input=True, type=str)
        # derive private_key to avoid dictionary attack
        private_key_derived = Parser.derive(private_key)
        return gen_public_key(private_key_derived), private_key_derived

    @staticmethod
    def get_entry_value_from_input(key_derived: bytes):
        plain_value = click.prompt(
            'Enter the entry\'s value', hide_input=True,
            confirmation_prompt=True)

        return Parser.cipher_encode(plain_value, key_derived)

    @staticmethod
    def update_metas(metas) -> dict:
        while True:
            click.echo('Add or update a metadata (press `enter` to skip)')
            label = click.prompt('label', type=str, default='')
            if label == '':
                break

            value = click.prompt('value', type=str, default='')
            if value == '':
                break

            metas[label] = value

        click.echo()
        return metas

    @staticmethod
    def get_metas() -> dict:
        return Input.update_metas({})
