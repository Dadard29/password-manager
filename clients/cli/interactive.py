import cmd
from urllib.parse import urlparse

import click

from caller import Caller
from cli.input import Input
from entry import Entry
from cli.logger import Logger
from parsing import Parser
from cli.printer import Printer


class InteractiveInput(cmd.Cmd):
    def __init__(self, caller, logger: Logger, p_key_derived: bytes):
        super().__init__()
        self.file = None

        self.path = ''
        self.dir_name = ''

        host = caller.host
        self._hostname = urlparse(host).hostname
        self._set_prompt()

        self.logger = logger

        self.intro = f'*connected*, type help or ? for a list of commands\n'

        self.caller = caller

        self.p_key_derived = p_key_derived

    def _set_prompt(self):
        if self.path == '':
            cwd = self.dir_name
        else:
            cwd = f'{self.path}/{self.dir_name}'

        cwd = '/' + cwd

        self.prompt = f'[{self._hostname}] ({cwd}): '

    def _get_current_path(self):
        if self.path == '':
            return self.dir_name
        else:
            return f'{self.path}/{self.dir_name}'

    def do_ls(self, arg):
        """
        List the content of the current directory
        """
        r = self.caller.get_directory(self.path, self.dir_name)
        if r.status_code != 200:
            self.logger.error(r.json()['message'])
            return

        Printer.print_ls(r.json()['body'])

    def do_mkdir(self, arg):
        """
        Create a new directory:
        - `mkdir dir1`: create a new directory names dir1
        """
        dir_name = arg
        path = self._get_current_path()

        r = self.caller.post_directory(path, dir_name)
        if r.status_code != 201:
            self.logger.error(r.json()['message'])
            return

        self.logger.info(f'directory `{dir_name}` created')

    def do_rmdir(self, arg):
        """
        Delete a directory AND ALL THE CONTENT
        - `rmdir dir1`: delete this directory, all
        the subdirectories and all the entries
        """

        dir_name = arg

        path = self._get_current_path()

        r = self.caller.delete_directory(path, dir_name)
        if r.status_code != 200:
            self.logger.error(r.json()['message'])
            return

        self.logger.info(f'directory `{dir_name}` deleted')

    def do_cd(self, arg):
        """
        Change the current directory:
        - `cd dir_1`: change to directory `dir_1`
        - `cd ..`: go to parent directory
        - `cd`: go to root directory
        """

        # goes at root
        if arg == '':
            new_path = ''
            new_dir_name = ''

        # goes backward
        elif arg == '..':
            ps = self.path.split('/')
            borne = len(ps) - 1
            new_dir_name = ps[borne]
            new_path = '/'.join(ps[:borne])

        # goes forward
        else:
            new_path = self._get_current_path()

            new_dir_name = arg

        r = self.caller.get_directory(new_path, new_dir_name)
        if r.status_code != 200:
            self.logger.error(r.json()['message'])
            return

        self.logger.debug(f'changed to directory {new_dir_name}')

        self.path = new_path
        self.dir_name = new_dir_name
        self._set_prompt()

    def do_get(self, arg):
        """
        Get an entry value and metadata from the current directory:
        - `get entry1`: get entry1 value
        """
        entry_name = arg

        if self.path == '':
            path = self.dir_name
        else:
            path = f'{self.path}/{self.dir_name}'

        r = self.caller.get_entry(path, entry_name)
        if r.status_code != 200:
            self.logger.error(r.json()['message'])
            return

        entry = Entry(r.json()['body'])

        if entry.created_with_cli:
            ciphered_nonce = entry.value
            plain_value = Parser.decipher_decode(ciphered_nonce, self.p_key_derived)
            Printer.print_entry_encrypted(
                entry, plain_value)
        else:
            self.logger.warning('this entry has not been created with this CLI, the value is transferred to the '
                                'remote server in plain text')
            Printer.print_entry(entry)

    def do_set(self, arg):
        """
        Create a new entry, or update an existing one:
        - `set entry1`: you will be asked for its value and the metadata
        """
        entry_name = arg
        if entry_name == '':
            self.logger.error('expecting an entry name as parameter')
            return

        path = self._get_current_path()

        entry_exists_r = self.caller.get_entry(path, entry_name)
        entry_exists = entry_exists_r.status_code == 200

        if not entry_exists:
            # creates a new one
            entry_value = Input.get_entry_value_from_input(self.p_key_derived)

            metas = Input.get_metas()
            metas['created_with_cli'] = "true"

            r = self.caller.post_entry(path, entry_name, entry_value, metas)
            if r.status_code != 201:
                self.logger.error(r.json()['message'])
                return

            self.logger.info(f'entry `{entry_name}` created')
        else:
            # update the existing one
            entry = Entry(entry_exists_r.json()['body'])

            if click.confirm('Update the value of this entry ?'):
                entry_value = Input.get_entry_value_from_input(self.p_key_derived)

                entry.metas['created_with_cli'] = "true"
            else:
                entry_value = entry.value

            Input.update_metas(entry.metas)

            r = self.caller.update_entry(path, entry_name, entry_value, entry.metas)
            if r.status_code != 200:
                self.logger.error(r.json()['message'])
                return

            self.logger.info(f'entry `{entry_name}` updated')

    def do_rm(self, arg):
        """
        Remove an entry:
        - `rm entry1`: delete permanently this entry and its metadata
        """
        entry_name = arg
        if entry_name == '':
            self.logger.error('expecting an entry name as parameter')
            return

        path = self._get_current_path()

        r = self.caller.delete_entry(path, entry_name)
        if r.status_code != 200:
            self.logger.error(r.json()['message'])
            return

        self.logger.info(f'entry `{entry_name}` deleted')

    def do_quit(self, arg):
        """
        Exit the interactive shell
        """
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
        """
        Get a fresh new session from server
        """

        key = Input.get_public_key()
        current_host = self.caller.host

        try:
            self.caller = Caller(current_host, key)
            self.logger.info('session refreshed')

        except ConnectionError as ce:
            self.logger.error(f'error creating session: connection error - {str(ce)}')

        except TypeError as te:
            self.logger.error(f'error creating session: wrong input - {str(te)}')
