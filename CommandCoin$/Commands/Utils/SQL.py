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
    #invoking internal function
    return get_setting_data(key, "setting")
    

def get_data(key:str) -> str:
    """Returns the value of a data entry in the config file

    Args:
        key (str): name of the data

    Returns:
        data (str): value of the data
        
    """
    #invoking internal function
    return get_setting_data(key, "data")

def get_setting_data(key:str, setting_or_data:str) -> str:
    """[INTERNAL/DEBUG] use complete get_setting or get_data instead\n
    Returns the value of a setting/data entry in the config file\n

    Args:
        key (str): name of the data
        setting_or_data (str) : chose between "data" or "setting"

    Returns:
        data (str): value of the data
        
    """
    #get connection with database
    try:
        with sqlite3.connect(config_dir)  as conn:  
            #get cursor
            cur : sqlite3.Cursor = conn.cursor()
            #selects the column setting from the table settings
            cur.execute(f"SELECT Value FROM {setting_or_data} WHERE Name='{key}'")
            #get value
            value = cur.fetchone()
            #data might be None, in that case we just return an error
            if value is None:
                raise sqlite3.Error()
            #return value
            return value[0]
    except sqlite3.Error as e:
        #Something went wrong, just close the connection and return nothing
        print(e)
        print(f"{key} was not found, returned an empty string")
        conn.close()
        return ""
    finally:
        conn.close()