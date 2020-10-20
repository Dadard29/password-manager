import os
from typing import List


class Config(object):
    def __init__(self, d: dict, env_list: List):
        for k, v in d.items():
            setattr(self, k, v)

        for e in env_list:
            setattr(self, e, os.environ[e])


config = Config({
    "app": {
        "name": "password_manager",
        "host": "0.0.0.0",
        "port": 5000
    }
}, ['DEBUG'])
