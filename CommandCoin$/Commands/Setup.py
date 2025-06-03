import os
import sqlite3
import time
import click
from datetime import date
from pathlib import Path
from Commands.Utils.SQL import *


@click.group()
def setup() -> None:
    """Setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.option('-d','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
def complete(directory:str) -> None:
    """
    Complete setup for CommandCoin$\n
    It will wipe all old data
    """
    #execute partial setups
    
    ctx = click.get_current_context()
    ctx.invoke(set_db, directory=directory)
    ctx.invoke(accounts)
    click.echo("Setup completed")

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your settings and database, are you sure?')
@click.option('-d','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
def set_db(directory:str) -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
    Creates settings file and database, stores current date as starting date\n
    It will wipe old data
    """    
    #wipe old files
    try:
        #remove old database
        os.remove(get_setting("database_dir"))
        #sleep needed to be sure that the settings file is released
        time.sleep(0.1)
    except FileNotFoundError:
        # File not found, not a problem
        pass
    except sqlite3.OperationalError:
        click.echo("No previous database detected - initializing fresh installation", err=True)  
    try:
        os.remove(settings_dir)
    except FileNotFoundError:
        # File not found, not a problem
        pass  

    #database directory
    database_dir : str = directory+"\\CommandCoin$.db"
    
    #open settings file and save data
    conn : sqlite3.Connection = sqlite3.connect(settings_dir) 
    cur : sqlite3.Cursor = conn.cursor()
    cur.execute("CREATE TABLE settings(setting TEXT PRIMARY KEY, value TEXT)")
    cur.execute(f"""INSERT OR REPLACE INTO settings VALUES
                ('database_dir','{database_dir}'),
                ('start_date','{str(date.today())}')
                """)
    conn.commit()
    conn.close()
    
    #create database
    sqlite3.connect(database_dir).close()
    

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Accounts table in the database, are you sure?')
def accounts() -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
    Creates the Accounts table in the database\n
    It will wipe old data
    """
    #get database
    databse_dir : str = get_setting("database_dir")
    conn : sqlite3.Connection = sqlite3.connect(databse_dir)
    cur : sqlite3.Cursor = conn.cursor()
    
    #wipe old table and create a new one
    cur.execute("DROP TABLE IF EXISTS Accounts")
    cur.execute("CREATE TABLE Accounts(id TEXT PRIMARY KEY, name TEXT)")
    conn.commit()
    #close connection
    conn.close()