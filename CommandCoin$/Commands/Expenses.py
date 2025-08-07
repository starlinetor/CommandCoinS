import sqlite3
import click
import Commands.Utils.SQL as SQL

@click.group()
def expenses() -> None:
    """
    Used to add and handle expenses\n
    """
    pass

@expenses.command()
def create() -> None: 
    #WIP
    pass