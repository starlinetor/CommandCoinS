import sqlite3
import click
import Commands.Utils.SQL as u_sql

@click.group()
def wallets() -> None:
    """
    Used to track expenses and earings\n
    Each wallet requires a parent Account\n
    Multiple wallets can be used to divide your money\n
    """
    pass

@wallets.command()
@click.argument('name')
@click.argument('account')
@click.option("-v", "--verbose", default = True, help='Increased debug information')
def create(name:str, account:str, verbose:bool) -> None:
    """Creates a new wallet

    Args:
        name (str): name of the new wallet
        account (str) : name of the account
    """
    try:
        with sqlite3.connect(SQL.get_data("database_dir")) as conn:
            cur : sqlite3.Cursor = conn.cursor()
            account_id : int = SQL.get_id(cur, account, "account")
            wallet_id : int = SQL.get_new_id("wallet")
            SQL.add_entry_database(cur,"wallets", (account_id, wallet_id, name))
            conn.commit()
        if verbose: click.echo(f"{name} wallet created successfully")
    except sqlite3.IntegrityError as e:
        if verbose: 
            if "UNIQUE constraint failed:" in str(e):
                click.echo(f"A wallet with the following name already exists : {name}")
            else : 
                click.echo(e)
    except Exception as e :
        if verbose: 
            click.echo(e)