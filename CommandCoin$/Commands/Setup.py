import sqlite3
from io import TextIOWrapper
from pathlib import Path


@click.group()
def setup() -> None:
    """setup CommandCoins$ on your pc"""
    pass

@setup.command()
@click.option('-d','--directory', help='Directory for database')
def basic(dir:str) -> None:
    """
    Creates a new setting file and database
    This will erase the settings file but not the databse
    """
    #get settings file directory
    settings_dir : str = Path(__file__).parents[2] / "settings.txt"
    settings : TextIOWrapper = open(settings_dir,mode = "w") 
    settings.write(dir)
    settings.close()
    database : sqlite3.Connection = sqlite3.connect(dir+"\\CommandCoin$.db")
    