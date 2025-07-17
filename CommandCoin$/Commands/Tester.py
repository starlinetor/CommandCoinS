import sqlite3
import click
import Commands.Utils.SQL  as SQL

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
def get_id(id_name : str):
    """Returns a new id for the specified object\n
    increments automatically ids"""
    click.echo(SQL.get_id(id_name))

@sql.command()
@click.argument('table')
@click.option("--entries", "-e", multiple=True, required=True)
def add_entry_database(table:str, entries):
    """add_entry_database tester"""
    conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
    cur : sqlite3.Cursor = conn.cursor()
    SQL.add_entry_database(cur,table,*entries)
    conn.commit()
    conn.close()

