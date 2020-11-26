import click
import requests
from requests import ConnectionError

from caller import Caller
from cli.input import Input
from cli.interactive import InteractiveInput
from cli.logger import Logger


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
    p_key_derived = None

    try:
        if not check_up(host):
            logger.error('error creating session: host down')
        else:
            logger.debug('host up')

        key, p_key_derived = Input.get_public_key()

        logger.debug('creating a new session...')
        caller = Caller(host, key)
        logger.info(f'session created')

    except ConnectionError as ce:
        logger.error(f'error creating session: connection error - {str(ce)}')
    except TypeError as te:
        logger.error(f'error creating session: wrong input - {str(te)}')

    if caller is not None:
        InteractiveInput(caller, logger, p_key_derived).cmdloop()


if __name__ == "__main__":
    pm()
