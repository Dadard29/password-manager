import click


class Logger(object):
    def __init__(self, debug_mode: bool):
        self.debug_mode = debug_mode

    @staticmethod
    def _log(msg):
        click.echo(msg)

    def info(self, msg):
        self._log(click.style(msg, fg='green'))

    def warning(self, msg):
        self._log(click.style(msg, fg='magenta'))

    def error(self, msg):
        self._log(click.style(msg, fg='red'))

    def debug(self, msg):
        if self.debug_mode:
            self._log(msg)
