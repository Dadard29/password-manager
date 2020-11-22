from base64 import b64encode, b64decode
from hashlib import md5

import click
from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import bcrypt

salt = b'\xad\x9a\x8e\xdf`X\x82\x8a\xfb_\xfeVS\xaf\x95\x12'


class Parser(object):

    @staticmethod
    def cipher_encode(plain: str, master_key_derived: bytes) -> str:
        cipher = ChaCha20.new(key=master_key_derived)
        ciphered = cipher.encrypt(plain.encode())
        nonce = cipher.nonce

        ciphered_64 = b64encode(ciphered)
        nonce_64 = b64encode(nonce)

        return f"{ciphered_64.decode()}.{nonce_64.decode()}"

    @staticmethod
    def decipher_decode(ciphered_nonce: str, master_key_derived: bytes) -> str:
        s = ciphered_nonce.split('.')
        ciphered_64 = s[0]
        nonce_64 = s[1]

        ciphered = b64decode(ciphered_64)
        nonce = b64decode(nonce_64)

        cipher = ChaCha20.new(key=master_key_derived, nonce=nonce)
        plain = cipher.decrypt(ciphered)

        return plain.decode()

    @staticmethod
    def derive_master_key(master_key: str) -> bytes:
        return md5(
            bcrypt(master_key, 14, salt=salt)
        ).hexdigest().encode()

    @staticmethod
    def get_master_key():
        return click.prompt('master key', hide_input=True, type=str)

    @staticmethod
    def get_entry_value_from_input(master_key_derived: bytes):
        plain_value = click.prompt(
            'Enter the entry\'s value', hide_input=True,
            confirmation_prompt=True)

        return Parser.cipher_encode(plain_value, master_key_derived)

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
        return Parser.update_metas({})
