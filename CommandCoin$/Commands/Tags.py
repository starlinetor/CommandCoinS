import sqlite3
import click
import Commands.Utils.SQL as SQL

@click.group()
def tags() -> None:
    """
    Used to differentiate expenses
    """
    pass

@tags.command()
@click.argument("name")
@click.argument("description")
def create(name:str, description:str)->None:
    """
    \b
    Creates a new tag
    Args:
        name (str): name of the tag, unique
        description (str): short description of the tag, use "" for phrases
    """
    
    try:
        conn : sqlite3.Connection = sqlite3.connect(SQL.get_data("database_dir"))
        cur : sqlite3.Cursor = conn.cursor()
        tag_id : int = SQL.get_new_id("tag")
        SQL.add_entry_database(cur, "tags", (tag_id, name, description))
        conn.commit()
        conn.close()
        click.echo(f"{name} tag created successfully")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed:" in str(e):
            click.echo(f"A tag with the following name already exists : {name}")
        else:
            click.echo(e)