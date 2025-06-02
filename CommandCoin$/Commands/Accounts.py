import sqlite3
import click

@click.group()
def accounts() -> None:
    """
    Rappresentation of one of your bank accounts\n
    Holds information, settings and automations\n
    You can create a wallets to track expenses\n
    """
    pass

@accounts.command()
def create() -> None:
    pass