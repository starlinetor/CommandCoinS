import sqlite3
import click
from .Utils import SQL as u_sql

@click.group()
def accounts() -> None:
    """
    \b
    Representation of one of your bank accounts
    Holds information, settings and automation
    You can create a wallets to track expenses
    """
    #Each account has a name, and Id, a list of wallets, and special rules
    #Create methods to check info on groups
    
    pass

@accounts.command()
@click.argument('name')
@click.option("-v", "--verbose", default = True, help='Increased debug information')
def create(name:str, verbose:bool) -> None:
    """
    \b
    Creates a new account
    Args:
        name (str): name of the new account
    """
    try:
        with sqlite3.connect(u_sql.get_data("database_dir")) as conn:
            cur : sqlite3.Cursor = conn.cursor()
            account_id : int = u_sql.get_new_id("account")
            u_sql.add_entry_database(cur,"accounts", (account_id, name))
            conn.commit()
        if verbose : click.echo(f"{name} account created successfully")
    except sqlite3.IntegrityError as e:
        if verbose:
            if "UNIQUE constraint failed:" in str(e):
                click.echo(f"An account with the following name already exists : {name}")
            else : 
                click.echo(e)
    except Exception as e :
        if verbose: 
            click.echo(e)