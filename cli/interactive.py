import cmd
from urllib.parse import urlparse

import click

from caller import Caller
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


def print_group(group: str, body: list):
    print(group.upper())
    print('=' * len(group) + '\n')

    for e in body:
        print(f'- {e}')


def print_list(host: str, body: list):
    h = f'{host} - group list'.upper()
    print(h)
    print('=' * len(h) + '\n')

    for g in body:
        print(f'- {g}')


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
            """print the list of groups"""
            r = self.caller.list_group()
            if r.status_code != 200:
                self.logger.error(r.json()['message'])
                return

            print_list(self.prompt, r.json()['body'])
        elif len(words) == 1:
            """list the entry list of a group"""
            group = words[0]
            r = self.caller.get_group(group)
            if r.status_code != 200:
                self.logger.error(r.json()['message'])
                return

            print_group(group, r.json()['body'])

        elif len(words) == 2:
            """print an entry"""
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

    def do_create(self, arg):
        """
        Creates new entry:
        - `create group1`: creates a new group if it does not exist
        - `create group1 entry1`: creates a new group if needed and
        a new entry if it does not existss
        """
        words = arg.split(' ')
        if arg == '':
            self.logger.error('expecting a group and an entry to be created')
            return
        elif len(words) == 1:
            """create a group"""
            group = words[0]
            r = self.caller.post_group(group)
            if r.status_code != 201:
                self.logger.error(r.json()['message'])
                return

            self.logger.info(r.json()['message'])
            return
        elif len(words) == 2:
            """creates an entry"""
            group = words[0]
            entry = words[1]
            r = self.caller.get_group(group)
            if r.status_code != 200:
                # creating a new group cuz it doesnt exist yet
                r = self.caller.post_group(group)
                if r.status_code != 201:
                    self.logger.error('error creating a new group: '
                                      + r.json()['message'])
                    return

            else:
                self.logger.debug('group already exists')

            value = click.prompt('Enter the entry value', hide_input=True,
                                 type=str, confirmation_prompt=True)
            metas = get_metas()

            r = self.caller.post_entry(group, entry, value, metas)
            if r.status_code != 201:
                self.logger.error('error creating a new entry'
                                  + r.json()['message'])
                return

            self.logger.info('entry created')

        else:
            self.logger.error('expecting a group and an entry to be created')
            return

    def do_delete(self, arg):
        """
        Deletes an group or an entry (CAUTION: NOT RECOVERABLE):
        - `delete group1 entry1`: delete an entry
        - `delete group1`: delete all entries in group and delete the group
        """

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

    def do_refresh(self, arg):
        """get a fresh new session from server"""
        if arg == '':
            self.logger.error('expecting a master key as argument')
            return

        key = arg
        current_host = self.caller.host

        try:
            self.caller = Caller(current_host, key)
            self.logger.info('session refreshed')

        except ConnectionError as ce:
            self.logger.error(f'error creating session: connection error - {str(ce)}')

        except TypeError as te:
            self.logger.error(f'error creating session: wrong input - {str(te)}')
