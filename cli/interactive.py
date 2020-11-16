import cmd
from urllib.parse import urlparse

from logger import Logger


def print_entry(group: str, name: str, body: dict):
    print(group.upper())
    print('=' * len(group) + '\n')

    metas = body['metas']
    value = body['value']

    data = [[name, '', value], ['metas', '', '']]
    for k in metas.keys():
        data.append(['', k, metas[k]])

    col_width = max(len(word) for row in data for word in row) + 2  # padding
    for row in data:
        print("".join(word.ljust(col_width) for word in row))


def print_group(group: str, body: dict):
    print(group.upper())
    print('=' * len(group) + '\n')

    for e in body:
        print(f'- {e}')


class InteractiveInput(cmd.Cmd):
    def __init__(self, caller, logger: Logger):
        super().__init__()
        self.file = None

        host = caller.host
        hostname = urlparse(host).hostname
        self.prompt = f'({hostname}) '

        self.logger = logger

        self.intro = f'*connected*, type help or ? for a list of commands\n'

        self.caller = caller

    def do_get(self, arg):
        """
            Get secrets and groups content:
            - `get`: get the list of the groups
            - `get group1`: get the list of the entries of a group
            - `get group1 entry1`: get a specific entry value
        """
        words = arg.split(' ')

        if arg == '':
            print('todo')
            return
        elif len(words) == 1:
            group = words[0]
            r = self.caller.get_group(group)
            if r.status_code != 200:
                print(r.status_code)
                self.logger.error(r.json()['message'])
                return

            print_group(group, r.json()['body'])

        elif len(words) == 2:
            group = words[0]
            entry = words[1]

            r = self.caller.get_secret(group, entry)
            if r.status_code != 200:
                self.logger.error(r.json()['message'])
                return

            print_entry(group, entry, r.json()['body'])
        else:
            self.logger.error('expecting an secret name and a group')
            return

    def do_quit(self, arg):
        """exit the interactive shell"""
        self.logger.debug('closing session...')

        # check if existing session already closed
        r = self.caller.get_session()
        if r.status_code == 404:
            # no session to close
            self.logger.warning('no session to be closed')
            return True

        r = self.caller.delete_session()
        if r.status_code != 200:
            m = r.json()['message']
            self.logger.error(f'your changes could\'nt be saved: {r.json()["message"]}')

        self.logger.info('session closed')
        return True
