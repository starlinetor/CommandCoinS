from pathlib import Path
import sqlite3

config_dir : str = Path(__file__).parents[3] / "data\\Config.db"
#list of valid ids
#update as needed
valid_id : list[str] = ["account", "wallet", "date", "expense", "tag"]

def get_setting(key:str) -> str:
    """Returns the value of a given setting

    Args:
        key (str): name of the setting

    Returns:
        setting (str): value of the setting
        
    """
    #invoking internal function
    return get_config(key, "settings")

def get_data(key:str) -> str:
    """Returns the value of a data entry in the config file

    Args:
        key (str): name of the data

    Returns:
        data (str): value of the data
        
    """
    #invoking internal function
    return get_config(key, "data")

def get_config(key:str, table:str) -> str:
    """[INTERNAL/DEBUG] use get_setting or get_data instead\n
    Returns the value of a setting/data entry in the config file\n

    Args:
        key (str): name of the entry
        table (str) : chose between "data" or "settings" table

    Returns:
        value (str): value of the entry
        
    """
    try:
        with sqlite3.connect(config_dir)  as conn:  
            cur : sqlite3.Cursor = conn.cursor()
            cur.execute(f"SELECT Value FROM {table} WHERE Name='{key}'")
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

def edit_settings(key:str, new_value:str) -> str:
    """
    Returns the value of a setting entry in the config file\n
    Updates the value of a setting entry in the config file\n

    Args:
        key (str): name of the entry
        value (str) : new value for the entry

    Returns:
        value (str): value of the data
        
    """
    return edit_config(key, new_value, "settings")

def edit_data(key:str, new_value:str) -> str:
    """
    Returns the value of a data entry in the config file\n
    Updates the value of a data entry in the config file\n

    Args:
        key (str): name of the entry
        value (str) : new value for the entry

    Returns:
        value (str): value of the data
    """
    return edit_config(key, new_value, "data")

def edit_config(key:str, new_value:str, table:str) -> str:
    """[INTERNAL/DEBUG] use complete edit_setting or edit_data instead\n
    Returns the value of a setting/data entry in the config file\n
    Updates the value of a setting/data entry in the config file\n

    Args:
        key (str): name of the entry
        value (str) : new value for the entry
        table (str) : chose between "data" or "settings" table

    Returns:
        value (str): value of the data
        
    """
    try:
        with sqlite3.connect(config_dir)  as conn:  
            cur : sqlite3.Cursor = conn.cursor()
            cur.execute(f"SELECT Value FROM {table} WHERE Name='{key}'")
            value = cur.fetchone()
            cur.execute(f"UPDATE {table} SET value={new_value} WHERE Name = '{key}'")
            #data might be None, in that case we just return an error
            if value is None:
                raise sqlite3.Error()
            return value[0]
    except sqlite3.Error as e:
        #Something went wrong, just close the connection and return nothing
        print(e)
        print(f"{key} was not found, returned an empty string")
        conn.close()
        return ""
    finally:
        conn.close()

def get_new_id(id_name:str) -> int:
    """Returns a new id for the specified object\n
    increments automatically ids
    Args:
        id_name (str): name of the object which the id is for

    Returns:
        int: new id for the object
    """
    if id_name not in valid_id:
        raise ValueError(f"{id_name} is not a valid id\n valid ids : {valid_id}")
    entry : str = f"{id_name}_id_counter"
    new_id : int = int(get_data(entry)) + 1
    edit_data(entry, str(new_id))
    return new_id

def add_entry_database(cursor:sqlite3.Cursor, table:str, *entries:str) -> None:
    """Adds a new entry in a target database and table\n
    does not commit or close the connection

    Args:
        cursor (sqlite3.Cursor): sqlite 3 cursor connected to the target database
        table (str): name of the target table
        entries (str) : all values of the data
    """
    #target  :
    # "INSERT OR REPLACE INTO data VALUES ('database_dir','database_dir')"
    command : str = f"INSERT INTO {table} VALUES "
    entries = [f"'{entry}'" for entry in entries]
    command = command + "(" + ",".join(entries) + ")"
    cursor.execute(command)