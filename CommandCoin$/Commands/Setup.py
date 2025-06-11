from ast import Str
import os
import sqlite3
import time
from tracemalloc import start
import click
from datetime import date
from pathlib import Path
from Commands.Utils.SQL import *
import gc


@click.group()
def setup() -> None:
    """Setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.confirmation_option(prompt='This will wipe your Config file and database, are you sure?')
@click.option('-d','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
@click.option('-d','--start_date',type=click.DateTime(formats=["%Y-%d-%m"]), default=str(date.today()), help='Starting date (YYYY-MM-DD)')
def complete(directory:str, start_date:str) -> None:
    """
    Complete setup for CommandCoin$\n
    It will wipe all old data
    """
    #execute partial setups
    
    ctx = click.get_current_context()
    ctx.invoke(config_database, directory=directory, start_date=start_date)
    ctx.invoke(accounts)
    click.echo("Setup completed")
    

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Accounts table in the database, are you sure?')
def database() -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
    Creates the Accounts table in the database\n
    It will wipe old data
    """
    #get database
    
@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Config file and database, are you sure?')
@click.option('-dir','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
@click.option('-d','--start_date',type=click.DateTime(formats=["%Y-%d-%m"]), default=str(date.today()), help='Starting date (YYYY-MM-DD)')
def config(directory:str, start_date:str) -> None:
    """[INTERNAL/DEBUG] use complete instead\n
    Creates Config database, stores current date as starting date\n
    Wipes the old Config file and old database
    """
    #wipe old files
    try:
        #remove old database
        os.remove(get_data("database_dir"))
    except FileNotFoundError:
        #File not found, not a problem
        click.echo("No previous database detected - initializing fresh installation", err=True) 
    except sqlite3.OperationalError:
        #Missing config database
        click.echo("No previous database detected - initializing fresh installation", err=True) 
    #sleep needed to be sure that the config file is released
    time.sleep(0.1)
    try:
        #Remove config database
        os.remove(config_dir)
    except PermissionError:
        #exit the application if the file is open
        click.echo("Config.db is open, close it before proceeding", err=True)  
        exit()
    except FileNotFoundError:
        # File not found, not a problem
        pass  

    #database directory
    database_dir : str = directory+"\\CommandCoin$.db"
    
    #open settings file and save data
    conn : sqlite3.Connection = sqlite3.connect(config_dir) 
    cur : sqlite3.Cursor = conn.cursor()
    #create tables
    cur.execute("CREATE TABLE settings(Setting TEXT PRIMARY KEY, Value TEXT)")
    cur.execute("CREATE TABLE data(Name TEXT PRIMARY KEY, Value TEXT)")
    cur.execute(f"""INSERT OR REPLACE INTO data VALUES
                ('database_dir','{database_dir}'),
                ('start_date','{start_date}')
                """)
    conn.commit()
    conn.close()
    
    #create database
    sqlite3.connect(database_dir).close()