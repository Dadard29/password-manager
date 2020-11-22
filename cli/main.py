import click
import requests
from requests import ConnectionError

from caller import Caller
from interactive import InteractiveInput
from logger import Logger
from parsing import Parser


def check_up(host):
    r = requests.get(host)
    return r.status_code == 404


@click.command()
@click.option('--debug/--no-debug', default=False, help='activate debug mode')
@click.option('--host', '-h', help='set the host where the service is running', required=True)
def pm(debug, host):
    """Connect to password manager"""

    logger = Logger(debug)
    logger.debug('debug mode on')

    caller = None
    key = None

    try:
        if not check_up(host):
            logger.error('error creating session: host down')
        else:
            logger.debug('host up')

        key = Parser.get_master_key()

        logger.debug('creating a new session...')
        caller = Caller(host, key)
        logger.info(f'session created')

    except ConnectionError as ce:
        logger.error(f'error creating session: connection error - {str(ce)}')
    except TypeError as te:
        logger.error(f'error creating session: wrong input - {str(te)}')

    if caller is not None:
        master_key_derived = Parser.derive_master_key(key)
        InteractiveInput(caller, logger, master_key_derived).cmdloop()


if __name__ == "__main__":
    pm()
