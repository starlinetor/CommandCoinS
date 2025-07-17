from ast import expr_context
import sqlite3
import click
import Commands.Utils.SQL as SQL

class account:
    def __init__(self, id, name):
        pass


@click.group()
def accounts() -> None:
    """
    Representation of one of your bank accounts\n
    Holds information, settings and automation\n
    You can create a wallets to track expenses\n
    """
    #TODO : create a class for accounts
    #Each account has a name, and Id, a list of wallets, and special rules
    #Create methods to check info on groups
    
    pass

@accounts.command()
@click.argument('name')
def create(name:str) -> None:
    """Creates a new account

    Args:
        name (str): name of the new account
    """
    try:
        conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
        cur : sqlite3.Cursor = conn.cursor()
        account_id : int = SQL.get_new_id("account")
        SQL.add_entry_database(cur,"accounts", (account_id, name))
        conn.commit()
        conn.close()
        click.echo(f"{name} account created successfully")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed:" in str(e):
            click.echo(f"An account with the following name already exists : {name}")
        else : 
            click.echo(e)