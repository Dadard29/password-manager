import unittest

from models.database import Database

p = "./"
master_key = "master_key"
filename = "new.db"


class DatabaseTest(unittest.TestCase):

    def test_raises_FileNotFound(self):
        filename = "wrong.db"
        self.assertRaises(
            FileNotFoundError,
            Database, p + filename, master_key
        )

    def test_reset_nonce(self):
        d = Database(p + filename, master_key)
        nonce = d.file.nonce

        d.file.reset(master_key)
        nonce_2 = d.file.nonce

        assert nonce != nonce_2

    def test_decrypt(self):
        d = Database(p + filename, master_key)

        assert not d.loaded
        assert d.decrypted is None

        d.load()
        assert d.loaded
        assert d.decrypted is not None

        print(d.decrypted._dictionary)


if __name__ == '__main__':
    unittest.main()
