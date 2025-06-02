import sqlite3
import click
from Commands.Utils.SQL import get_setting

@click.group()
def accounts() -> None:
    """
    Rappresentation of one of your bank accounts\n
    Holds information, settings and automations\n
    You can create a wallets to track expenses\n
    """
    #TODO : create a class for accounts
    #Each account has a name, and Id, a list of wallets, and special rules
    #Create methods to check info on groups
    pass

@accounts.command()
def create(name:str) -> None:
    database_dir : str = get_setting("database_dir")
    