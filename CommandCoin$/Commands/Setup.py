import os
import random
import sqlite3
import json
import click
from datetime import date
from io import TextIOWrapper
from pathlib import Path

@click.group()
def setup() -> None:
    """setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.option('-d','--directory', required=True, help='Directory for database')
@click.option('-w','--wipe', default=False, type = bool, help='Wipes old settings file') 
def basic(directory:str, wipe:bool) -> None:
    """Basic setup for command coin. It will save the database directory and the current date.
    The current date is used as a starting point for the data. 
    """
    #get settings file directory
    settings_dir : str = Path(__file__).parents[2] / "settings.db"
    database_dir : str = directory+"\\CommandCoin$.db"
    
    #delete save file if needed
    if wipe:
        os.remove(settings_dir)
    
    #open save file
    settings : sqlite3.Connection = sqlite3.connect(settings_dir) 
    #create settings data and save it
    cur : sqlite3.Cursor = settings.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings(setting TEXT PRIMARY KEY, value TEXT)")
    cur.execute(f"""INSERT OR REPLACE INTO settings VALUES
                ('database_dir','{database_dir}'),  
                ('start_date','{str(date.today())}')
                """)
    settings.commit()
    #create database
    sqlite3.connect(database_dir)
    