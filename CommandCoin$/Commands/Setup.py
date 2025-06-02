import os
import sqlite3
import click
from datetime import date
from pathlib import Path

#settings location
from Commands.Utils.SQL import settings_dir

@click.group()
def setup() -> None:
    """Setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.option('-d','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
@click.option('-w','--wipe', default=False, type = bool, help='Wipes old settings file') 
@click.option('-u','--update_date', default=True, type = bool, help='Update starting date') 
def basic(directory:str, wipe:bool, update_date:bool) -> None:
    """
    Basic setup for command coin. It will save the database directory and the current date.\n
    The current date is used as the starting date for all expenses. 
    """
    
    #TODO this problably needs some polishing
    
    #get settings file directory
    database_dir : str = directory+"\\CommandCoin$.db"
    
    #delete save file if needed
    if wipe:
        os.remove(settings_dir)
    
    #open save file
    settings : sqlite3.Connection = sqlite3.connect(settings_dir) 
    #create settings data and save it
    cur : sqlite3.Cursor = settings.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings(setting TEXT PRIMARY KEY, value TEXT)")
    #save database dir
    cur.execute(f"""INSERT OR REPLACE INTO settings VALUES
                ('database_dir','{database_dir}')
                """)
    #update if asked the starting date
    #TODO this does not make sence, you always want to have a date so check if is already present
    #TODO arguably i don't even know why i need a starting date 
    if update_date:
        cur.execute(f"""INSERT OR REPLACE INTO settings VALUES  
                ('start_date','{str(date.today())}')
                """)
    settings.commit()
    #create database
    sqlite3.connect(database_dir)

@setup.command()
@click.option('-w','--wipe', default=False, type = bool, help='Wipes old settings file') 
def accounts():
    #TODO this should create a basic table that stores each account info
    #name, id (i think is better if each table for each account is named after the id and not the actual name)
    pass