from os import environ
from typing import List


class Config(object):
    def __init__(self, d: dict, env_list: List):
        for k, v in d.items():
            setattr(self, k, v)

        for e in env_list:
            setattr(self, e, environ[e])


config = Config({
    "app": {
        "name": "password_manager",
        "host": environ['HTTP_HOST'],
        "port": environ['HTTP_PORT']
    },
    "session": {
        "timeout": 120,
    },
    "crypto": {
        "key_derivation_cost": 14
    }
}, ['DEBUG', 'MASTER_KEY', 'DB_PATH'])
