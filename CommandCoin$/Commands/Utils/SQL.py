from pathlib import Path
import sqlite3

config_dir : str = Path(__file__).parents[3] / "data\\Config.db"

def get_setting(key:str) -> str:
    """Returns the value of a given setting

    Args:
        key (str): name of the setting

    Returns:
        setting (str): value of the setting
        
    """
    try:
        with sqlite3.connect(config_dir)  as conn:  
            #get cursor
            cur : sqlite3.Cursor = conn.cursor()
            #selects the column setting from the table settings
            cur.execute(f"SELECT Value FROM settings WHERE Setting='{key}'")
            #get value
            setting = cur.fetchone()[0]
            #return value
            return setting
    except sqlite3.Error as e:
        #Something went wrong, just close the connection and return nothing
        print(e)
        print(f"{key} was not found, returned an empty string")
        conn.close()
        return ""
    finally:
        conn.close()
    

def get_data(key:str) -> str:
    """Returns the value of a data entry in the config file

    Args:
        key (str): name of the data

    Returns:
        data (str): value of the data
        
    """
    #get connection with database
    try:
        with sqlite3.connect(config_dir)  as conn:  
            #get cursor
            cur : sqlite3.Cursor = conn.cursor()
            #selects the column setting from the table settings
            cur.execute(f"SELECT Value FROM data WHERE Name='{key}'")
            #get value
            data = cur.fetchone()[0]
            #return value
            return data
    except sqlite3.Error as e:
        #Something went wrong, just close the connection and return nothing
        print(e)
        print(f"{key} was not found, returned an empty string")
        conn.close()
        return ""
    finally:
        conn.close()

