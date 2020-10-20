import click


@click.group()
@click.option('-v/--no-debug', default=False, help='activate debug mode')
def pm(debug):
    """Operate on your name"""
    print(f'Debug mode: {"on" if debug else "off"}')


@pm.command()
@click.option('--name', default="ouam")
def show(name):
    """Prints your name"""
    print(f"your name is {name}")


if __name__ == "__main__":
    pm()
