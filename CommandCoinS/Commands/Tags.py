import sqlite3
import click
from .Utils import SQL as u_sql

@click.group()
def tags() -> None:
    """
    Used to differentiate expenses
    """
    pass

@tags.command()
@click.argument("name")
@click.argument("description")
@click.option("-v", "--verbose", default = True, help='Increased debug information')
def create(name:str, description:str, verbose:bool)->None:
    """
    \b
    Creates a new tag
    Args:
        name (str): name of the tag, unique
        description (str): short description of the tag, use "" for phrases
    """
    
    try:
        with sqlite3.connect(u_sql.get_data("database_dir")) as  conn :
            cur : sqlite3.Cursor = conn.cursor()
            tag_id : int = u_sql.get_new_id("tag")
            u_sql.add_entry_database(cur, "tags", (tag_id, name, description))
            conn.commit()
        if verbose : click.echo(f"{name} tag created successfully")
    except sqlite3.IntegrityError as e:
        if verbose :
            if "UNIQUE constraint failed:" in str(e):
                click.echo(f"A tag with the following name already exists : {name}")
            else:
                click.echo(e)
    except Exception as e :
        if verbose: 
            click.echo(e)