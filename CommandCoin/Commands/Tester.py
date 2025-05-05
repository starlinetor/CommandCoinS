import click

@click.group()
def tester():
    """Testing and debug"""
    pass

@tester.command()
def hello_world():
    """Hello world test"""
    click.echo("Hello World")