import click

from entry import Entry


class Printer(object):
    @staticmethod
    def _print_title(title: str):
        click.echo(title.upper())
        click.echo('=' * len(title))

    @staticmethod
    def _print_columns(data: list):
        click.echo("")

        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
            click.echo("".join(word.ljust(col_width) for word in row))

        click.echo("")

    @staticmethod
    def print_entry_encrypted(entry: Entry, plain_value: str):
        entry.value = plain_value
        Printer.print_entry(entry)

    @staticmethod
    def print_entry(entry: Entry):

        underline = '-' * len(entry.value)
        click.echo(underline)
        click.echo(entry.value)
        click.echo(underline)

        label_color = 'bright_black'
        data = [
            [click.style('created at', fg=label_color), entry.created_at],
            [click.style('updated at', fg=label_color), entry.updated_at],
            ['-', '-']
        ]
        for k in entry.metas.keys():
            data.append([click.style(k, fg=label_color), entry.metas[k]])

        Printer._print_columns(data)

    @staticmethod
    def print_ls(body: list):
        data = [[
            click.style('name', bold=True),
            click.style('size', bold=True),
            click.style('created at', bold=True),
            click.style('updated at', bold=True)
        ]]

        for e in body:
            color = 'white'
            if e['type'] == 'directory':
                color = 'bright_blue'

            data.append([
                click.style(e['name'], fg=color),
                click.style(e['size'], fg=color),
                click.style(e['created_at'], fg=color),
                click.style(e['updated_at'], fg=color)
            ])

        Printer._print_columns(data)
