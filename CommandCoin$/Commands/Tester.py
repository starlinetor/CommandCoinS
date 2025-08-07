import datetime
import sqlite3
import click
import Commands.Utils.SQL as SQL
import Commands.Utils.Dates as Dates

@click.group()
def tester() -> None:
    """Testing and debug"""
    pass

@tester.command()
def print_test() -> None:
    """Print to screen test"""
    string =[
    ""
    r"_________                                           .____________        .__         ____/\__ ",
    r"\_   ___ \  ____   _____   _____ _____    ____    __| _/\_   ___ \  ____ |__| ____  /   / /_/ ",
    r"/    \  \/ /  _ \ /     \ /     \\__  \  /    \  / __ | /    \  \/ /  _ \|  |/    \ \__/ / \  ",
    r"\     \___(  <_> )  Y Y  \  Y Y  \/ __ \|   |  \/ /_/ | \     \___(  <_> )  |   |  \/ / /   \ ",
    r" \______  /\____/|__|_|  /__|_|  (____  /___|  /\____ |  \______  /\____/|__|___|  /_/ /__  / ",
    r"    \/             \/      \/     \/     \/      \/         \/               \/  \/   \/      ",
    ""]
    
    click.echo("\n".join(string))
    click.echo("Font credits : https://github.com/Marak/asciimo/blob/master/fonts/Graffiti.flf")

#tests related to sql
@tester.group()
def sql() -> None:
    """SQL tests"""
    pass

@sql.command()
@click.argument('key')
@click.argument('table')
def get_config(key : str, table : str):
    """Returns the value of a setting or a data entry in the config database"""
    click.echo(SQL.get_config(key, table))

@sql.command()
@click.argument('key')
@click.argument('new_value')
@click.argument('table')
def edit_config(key : str, new_value : str, table : str):
    """Edits and returns the value of a setting or a data entry in the config database"""
    click.echo(SQL.edit_config(key, new_value, table))

@sql.command()
@click.argument('id_name')
def get_new_id(id_name : str):
    """
    \b
    Returns a new id for the specified object
    increments automatically ids"""
    click.echo(SQL.get_new_id(id_name))

@sql.command()
@click.argument('table')
@click.option("--entries", "-e", multiple=True, required=True)
def add_entry_database(table:str, entries:tuple[str]):
    """add_entry_database tester"""
    conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
    cur : sqlite3.Cursor = conn.cursor()
    SQL.add_entry_database(cur,table,entries)
    conn.commit()
    conn.close()

@sql.command()
@click.argument('table')
@click.argument('name')
@click.option("--columns", "-c", multiple=True, required=True)
@click.option("--keys", "-k", multiple=True, required=True)
def read_entry_database(table:str, name:str, columns:tuple[str], keys:tuple[str]):
    """read_entry_database tester"""
    conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
    cur : sqlite3.Cursor = conn.cursor()
    click.echo(SQL.read_entry_database(cur,table,name,columns,keys))
    conn.commit()
    conn.close()

@sql.command()
@click.argument('name')
@click.argument('id_type')
def get_ids(name:str, id_type : str):
    """
    \b
    Returns a list of ids from the main database
    Args:
        name (str): name of the object
        id_type (str): type of the object
    """
    conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
    cur : sqlite3.Cursor = conn.cursor()
    print(SQL.get_ids(cur,name, id_type))
    conn.commit()
    conn.close()

@tester.group()
def dates() -> None:
    """Dates related testing"""
    pass

@dates.command()
@click.argument("date", type=click.DateTime(formats=["%Y-%m-%d"]))
def get_date_id(date:datetime.date):
    click.echo(Dates.get_date_id(date.date()))