import datetime
from email.policy import default
import sqlite3
import click
import Commands.Utils.SQL as u_sql
import Commands.Utils.Dates as u_dates

@click.group()
def expenses() -> None:
    """
    Used to add and handle expenses\n
    """
    pass

@expenses.command()
@click.argument('account', type = click.STRING)
@click.argument('wallet', type = click.STRING)
@click.argument('date', type = click.DateTime(formats=["%Y-%m-%d"]), default = datetime.date.today())
@click.argument('name', type = click.STRING)
@click.argument('description', type = click.STRING)
@click.argument('value', type = click.INT)
@click.argument("tags", nargs=-1, type = str)
@click.option("-v", "--verbose", default = True, help='Increased debug information')
def create(account : str, wallet : str, date : datetime.datetime, name : str, description : str, value : int, verbose : bool, tags : tuple[str]) -> None: 
    try:
        with sqlite3.connect(u_sql.get_data("database_dir")) as conn:
            #add expense
            cur : sqlite3.Cursor = conn.cursor()
            account_id : int = u_sql.get_id(cur, account, "account")
            wallet_id : int = u_sql.get_id(cur, wallet, "wallet")
            date_id : int = u_dates.get_date_id(date.date(), u_sql.get_data("start_date"))
            expense_id : int = u_sql.get_new_id("expense")
            u_sql.add_entry_database(cur, "expenses", (account_id, wallet_id, date_id, expense_id, name, description, value))
            #add tags to the expense
            if len(tags) == 0:
                tags = ("None",)
            for tag in tags:
                tag_id = u_sql.get_id(cur, tag, "tag")
                u_sql.add_entry_database(cur, "expenses_tags", (account_id, wallet_id, date_id, expense_id, tag_id))
            conn.commit()
            if verbose: click.echo(f"{name} expense created successfully")
    except sqlite3.IntegrityError as e:
        if verbose:
            if "UNIQUE constraint failed:" in str(e):
                click.echo(f"An account with the following name already exists : {name}")
            else : 
                click.echo(e)
    except Exception as e :
        if verbose: 
            click.echo(e)



