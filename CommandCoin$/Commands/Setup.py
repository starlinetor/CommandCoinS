import os
import sqlite3
import time
from xmlrpc.client import Boolean
import click
from datetime import date
from pathlib import Path
from Commands.Utils.SQL import *


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
    Complete setup for CommandCoin$\n
    It will wipe all old data
    """
    #execute all setups
    
    ctx = click.get_current_context()
    ctx.invoke(wipe_database, verbose=verbose)
    ctx.invoke(wipe_config, verbose=verbose)
    ctx.invoke(config, directory=directory, start_date=start_date)
    ctx.invoke(database)
    click.echo("Setup completed")
    

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your database, are you sure?')
@click.option('-v','--verbose', default=True, help='Increased debug information')
def wipe_database(verbose:Boolean) -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
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
def wipe_config(verbose:Boolean) -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
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
@click.option('-d','--start_date',type=click.DateTime(formats=["%Y-%d-%m"]), default=str(date.today()), help='Starting date (YYYY-MM-DD)')
def config(directory:str, start_date:str) -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
    Creates Config database\n
    Stores starting date and database directory\n
    Will wipe old data and settings on the database
    """
    #database directory
    database_dir : str = directory+"\\CommandCoin$.db"
    
    #open settings file and save data
    conn : sqlite3.Connection = sqlite3.connect(config_dir) 
    cur : sqlite3.Cursor = conn.cursor()
    #remove old tables
    #create new tables
    #store data
    cur.executescript(f"""
                DROP TABLE IF EXISTS settings;
                DROP TABLE IF EXISTS data;
                CREATE TABLE settings(Setting TEXT PRIMARY KEY, Value TEXT);
                CREATE TABLE data(Name TEXT PRIMARY KEY, Value TEXT);
                INSERT OR REPLACE INTO data VALUES
                ('database_dir','{database_dir}'),
                ('start_date','{start_date}'),
                ('account_id_counter','0'),
                ('wallet_id_counter','0'),
                ('date_id_counter','0'),
                ('expense_id_counter','0') 
                """)
    conn.commit()
    conn.close()

@setup.command(hidden=True)
@click.confirmation_option(prompt='This will wipe your Accounts, Wallets and expenses, are you sure?')
def database() -> None:
    """
    [INTERNAL/DEBUG] use complete instead\n
    Creates database\n
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
                    Account_Id INTEGER PRIMARY KEY, 
                    Name TEXT
                )
                """)   
    #wallets
    cur.executescript("""
                CREATE TABLE wallets(
                    Account_Id INTEGER, 
                    Wallet_Id INTEGER, 
                    Name TEXT,
                    PRIMARY KEY (Account_Id, Wallet_Id),
                    FOREIGN KEY (Account_Id) REFERENCES accounts(Account_Id) ON DELETE CASCADE
                )
                """)
    #tags
    cur.executescript("""
                CREATE TABLE tags(
                    Tag_Id INTEGER PRIMARY KEY, 
                    Name TEXT, 
                    Description TEXT
                )
                """) 
    #expenses
    cur.executescript("""
                CREATE TABLE expenses(
                    Account_Id INTEGER,
                    Wallet_Id INTEGER,
                    Date_Id INTEGER,
                    Expense_Id INTEGER,
                    Description TEXT,
                    Value INTEGER,
                    PRIMARY KEY (Account_Id, Wallet_Id, Date_Id, Expense_Id),
                    FOREIGN KEY (Account_Id) REFERENCES accounts(Account_Id) ON DELETE CASCADE,
                    FOREIGN KEY (Wallet_Id) REFERENCES wallets(Wallet_Id) ON DELETE CASCADE
                )
                """)
    #expenses_tags
    cur.executescript("""
                CREATE TABLE expenses_tags(
                    Account_Id INTEGER,
                    Wallet_Id INTEGER,
                    Date_Id INTEGER,
                    Expense_Id INTEGER,
                    Tag_Id INTEGER,
                    PRIMARY KEY (Account_Id, Wallet_Id, Date_Id, Expense_Id, Tag_Id),
                    FOREIGN KEY (Account_Id, Wallet_Id, Date_Id, Expense_Id)
                    REFERENCES expenses(Account_Id, Wallet_Id, Date_Id, Expense_Id) ON DELETE CASCADE,
                    FOREIGN KEY (Tag_Id) REFERENCES tags(Tag_Id) ON DELETE CASCADE
                )
                """)
    #accounts_settings
    cur.executescript("""
                CREATE TABLE accounts_settings(
                    Account_Id INTEGER,
                    Setting TEXT,
                    Type TEXT,
                    Value TEXT,
                    PRIMARY KEY (Account_Id, Setting),
                    FOREIGN KEY (Account_Id) REFERENCES accounts(Account_Id) ON DELETE CASCADE
                )
                """)
    #wallets_settings
    cur.executescript("""
                CREATE TABLE wallets_settings(
                    Account_Id INTEGER,
                    Wallet_Id INTEGER,
                    Setting TEXT,
                    Type TEXT,
                    Value TEXT,
                    PRIMARY KEY (Account_Id, Wallet_ID, Setting),
                    FOREIGN KEY (Account_Id) REFERENCES accounts(Account_Id) ON DELETE CASCADE,
                    FOREIGN KEY (Wallet_Id) REFERENCES wallets(Wallet_Id) ON DELETE CASCADE
                )
                """)
    conn.commit()
    conn.close()           