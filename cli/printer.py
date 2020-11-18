import click


class Printer(object):
    @staticmethod
    def _print_title(title: str):
        print(title.upper())
        print('=' * len(title))

    @staticmethod
    def _print_columns(data: list):
        print("")

        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
            print("".join(word.ljust(col_width) for word in row))

        print("")

    @staticmethod
    def print_entry(body: dict):
        created_at = body['created_at']
        updated_at = body['updated_at']

        content = body['content']
        metas = content['metas']
        value = content['value']

        print('-' * len(value))
        print(click.style(value, bold=True))
        print('-' * len(value))

        data = [
            ['created at', created_at],
            ['updated at', updated_at],
            ['-', '-']
        ]
        for k in metas.keys():
            data.append([k, metas[k]])

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
