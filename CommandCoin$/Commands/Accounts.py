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
    
    """
    Accounts datastructure info
    Accounts are stored in the Account table
    The table contains : 
        -id : id of the account, this is unique, used to find chil table
        -name : name of the account
    For each Account there is a corresponding table named Account_ID with the ID replaced by the ID number of the account
    Each Account_ID folder will contain the following data
        -id : id of a wallet
        -name : name of the wallet
    """
    pass

@accounts.command()
def create(name:str) -> None:
    database_dir : str = get_setting("database_dir")
    