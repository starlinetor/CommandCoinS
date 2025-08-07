import os
import sqlite3
import time
import click

from datetime import date
from pathlib import Path
#TODO REWRITE THIS AS import Commands.Utils.SQL as SQL
from Commands.Utils.SQL import *
import Commands.Tags as Tags


@click.group()
def setup() -> None:
    """Setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.confirmation_option(prompt='This will wipe your Config file and database, are you sure?')
@click.option('-d','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
@click.option('-d','--start_date',type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()), help='Starting date (YYYY-MM-DD)')
@click.option('-v','--verbose', default=False, help='Increased debug information')
def complete(directory:str, start_date:str, verbose:bool) -> None:
    """
    \b
    Complete setup for CommandCoin$
    It will wipe all old data
    """
    #execute all setups
    
    ctx = click.get_current_context()
    ctx.invoke(wipe_database, verbose=verbose)
    ctx.invoke(wipe_config, verbose=verbose)
    ctx.invoke(config, directory=directory, start_date=start_date)
    ctx.invoke(database)
    ctx.invoke(default_tags)
    click.echo("Setup completed")
    

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your database, are you sure?')
@click.option('-v','--verbose', default=True, help='Increased debug information')
def wipe_database(verbose:bool) -> None:
    """
    \b
    [INTERNAL/DEBUG] use complete instead
    Wipes the database
    """
    #wipe old files
    try:
        #remove old database
        os.remove(get_data("database_dir"))
    except (FileNotFoundError,sqlite3.OperationalError) as e:
        #File not found, not a problem
        if verbose:
            click.echo(e)
            click.echo("No previous database detected", err=True) 
    #sleep needed to be sure that the config file is released
    time.sleep(0.1)

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your config file, are you sure?')
@click.option('-v','--verbose', default=True, help='Increased debug information')
def wipe_config(verbose:bool) -> None:
    """
    \b
    [INTERNAL/DEBUG] use complete instead
    Wipes the config file
    """
    try:
        #Remove config database
        os.remove(config_dir)
    except PermissionError as e:
        #exit the application if the file is open
        if verbose:
            click.echo(e)
        click.echo("Config.db is open, close it before proceeding", err=True)  
        exit()
    except FileNotFoundError as e:
        # File not found, not a problem
        if verbose:
            click.echo(e)

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Config file data and settings, are you sure?')
@click.option('-dir','--directory', default=str(Path(__file__).parents[2] / "data"), help='Directory for database')
@click.option('-d','--start_date',type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()), help='Starting date (YYYY-MM-DD)')
def config(directory:str, start_date:str) -> None:
    """
    \b
    [INTERNAL/DEBUG] use complete instead
    Creates Config database
    Stores starting date and database directory
    Will wipe old data and settings on the database
    """
    #database directory
    database_dir : str = str(Path(directory) / "CommandCoin$.db")
    
    #open settings file and save data
    conn : sqlite3.Connection = sqlite3.connect(config_dir) 
    cur : sqlite3.Cursor = conn.cursor()
    #remove old tables
    #create new tables
    #store data
    #start_date.date() is used to remove the time
    cur.executescript(f"""
                DROP TABLE IF EXISTS settings;
                DROP TABLE IF EXISTS data;
                CREATE TABLE settings(name TEXT PRIMARY KEY, value TEXT);
                CREATE TABLE data(name TEXT PRIMARY KEY, value TEXT);
                INSERT OR REPLACE INTO data VALUES
                ('database_dir','{database_dir}'),
                ('start_date','{start_date.date()}'),
                ('account_id_counter','0'),
                ('wallet_id_counter','0'),
                ('date_id_counter','0'),
                ('expense_id_counter','0'),
                ('tag_id_counter','0')  
                """)
    conn.commit()
    conn.close()

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Accounts, Wallets and expenses, are you sure?')
def database() -> None:
    """
    \b
    [INTERNAL/DEBUG] use complete instead
    Creates database
    Will wipe old Accounts, Wallets and expenses
    """
    #open/create database and get cursor
    conn : sqlite3.Connection = sqlite3.connect(get_data("database_dir"))
    cur : sqlite3.Cursor = conn.cursor()
    #drop old tables
    cur.executescript("""
                DROP TABLE IF EXISTS accounts;
                DROP TABLE IF EXISTS wallets;
                DROP TABLE IF EXISTS tags;
                DROP TABLE IF EXISTS expenses;
                DROP TABLE IF EXISTS expenses_tags;
                DROP TABLE IF EXISTS accounts_settings;
                DROP TABLE IF EXISTS wallets_settings;
                """)   
    #create new tables
    #accounts
    cur.executescript("""
                CREATE TABLE accounts(
                    account_id INTEGER, 
                    name TEXT,
                    PRIMARY KEY (account_id),
                    UNIQUE (name)
                )
                """)   
    #wallets
    cur.executescript("""
                CREATE TABLE wallets(
                    account_id INTEGER, 
                    wallet_id INTEGER, 
                    name TEXT,
                    PRIMARY KEY (account_id, wallet_id),
                    UNIQUE (account_id, name),
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
                )
                """)
    #tags
    cur.executescript("""
                CREATE TABLE tags(
                    tag_id INTEGER, 
                    name TEXT, 
                    description TEXT,
                    PRIMARY KEY (tag_id),
                    UNIQUE (name)
                )
                """) 
    #expenses
    cur.executescript("""
                CREATE TABLE expenses(
                    account_id INTEGER,
                    wallet_id INTEGER,
                    date_id INTEGER,
                    expense_id INTEGER,
                    name TEXT,
                    description TEXT,
                    value INTEGER,
                    PRIMARY KEY (account_id, wallet_id, date_id, expense_id),
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
                    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id) ON DELETE CASCADE
                )
                """)
    #expenses_tags
    cur.executescript("""
                CREATE TABLE expenses_tags(
                    account_id INTEGER,
                    wallet_id INTEGER,
                    date_id INTEGER,
                    expense_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (account_id, wallet_id, date_id, expense_id, tag_id),
                    FOREIGN KEY (account_id, wallet_id, date_id, expense_id)
                    REFERENCES expenses(account_id, wallet_id, date_id, expense_id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
                )
                """)
    #accounts_settings
    cur.executescript("""
                CREATE TABLE accounts_settings(
                    account_id INTEGER,
                    setting TEXT,
                    type TEXT,
                    value TEXT,
                    PRIMARY KEY (account_id, setting),
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
                )
                """)
    #wallets_settings
    cur.executescript("""
                CREATE TABLE wallets_settings(
                    account_id INTEGER,
                    wallet_id INTEGER,
                    setting TEXT,
                    type TEXT,
                    value TEXT,
                    PRIMARY KEY (account_id, wallet_id, setting),
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
                    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id) ON DELETE CASCADE
                )
                """)
    conn.commit()
    conn.close()           

@setup.command(hidden=True)
@click.option('-v', '--verbose', default=True, help = 'Increased debug information')
def default_tags(verbose : bool)-> None: 
    """
    \b
    [INTERNAL/DEBUG] use complete instead
    Adds default tags to the database
    """
    ctx = click.get_current_context()
    ctx.invoke(Tags.create, name = "None", description = "Used when no tag is entered", verbose = verbose)
    ctx.invoke(Tags.create, name = "Transaction", description = "Used when an expense transfers money between wallets", verbose = verbose)


