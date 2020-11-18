import cmd
from urllib.parse import urlparse

import click
from requests import ConnectionError

from caller import Caller
from interactive import InteractiveInput
from logger import Logger
from parser import Parser


@click.command()
@click.option('--debug/--no-debug', default=False, help='activate debug mode')
@click.option('--host', '-h', help='set the host where the service is running', required=True)
def pm(debug, host):
    """Connect to password manager"""

    logger = Logger(debug)
    logger.debug('debug mode on')

    caller = None

    key = Parser.get_master_key()

    try:
        logger.debug('creating a new session...')
        caller = Caller(host, key)
        logger.info(f'session created')

    except ConnectionError as ce:
        logger.error(f'error creating session: connection error - {str(ce)}')
    except TypeError as te:
        logger.error(f'error creating session: wrong input - {str(te)}')

    if caller is not None:
        InteractiveInput(caller, logger).cmdloop()


if __name__ == "__main__":
    pm()
