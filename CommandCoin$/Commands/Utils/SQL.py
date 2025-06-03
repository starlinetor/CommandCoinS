from pathlib import Path
import sqlite3

settings_dir : str = Path(__file__).parents[3] / "data\\settings.db"

def get_setting(key:str) -> str:
    """Returns the value of a given setting

    Args:
        key (str): name of the setting

    Returns:
        setting (str): value of the setting
        
    """
    #get connection with database
    conn : sqlite3.Connection = sqlite3.connect(settings_dir) 
    #get cursor
    cur : sqlite3.Cursor = conn.cursor()
    #selects the column setting from the table settings
    cur.execute(f"SELECT value FROM settings WHERE setting='{key}'")
    #get value
    setting = cur.fetchone()[0]
    #close connection
    conn.close()
    #return value
    return setting

