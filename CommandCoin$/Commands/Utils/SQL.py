from pathlib import Path
import sqlite3
#software variables
config_dir : str = Path(__file__).parents[3] / "data\\Config.db"
#list of objects that have an id
#update as needed
valid_ids : list[str] = ["account", "wallet","expense", "tag"]

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
                raise sqlite3.Error("No entries matching the criteria")
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

def check_valid_id_type(id_type:str)->None:
    """Checks if an id is valid. In the case is not trows an error. 

    Args:
        id_name (str): name of the object which the id is for
    """
    if id_type not in valid_ids:
        raise ValueError(f"{id_type} is not a valid id\n valid ids : {valid_ids}")

def get_new_id(id_type:str) -> int:
    """Returns a new id for the specified type\n
    increments automatically ids
    Args:
        id_type (str): type of id
        example  : "account", "wallet","expense", "tag"

    Returns:
        int: new id for the object
    """
    check_valid_id_type(id_type)
    #Other ids are incremental so you just need to add one and get a new one
    #The format in the database for ids is {id_type}_id_counter
    entry : str = f"{id_type}_id_counter"
    new_id : int = int(get_data(entry)) + 1
    edit_data(entry, str(new_id))
    return new_id

def add_entry_database(cur:sqlite3.Cursor, table:str, entries:tuple[str]) -> None:
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
    entries = tuple(f"'{entry}'" for entry in entries)
    command = command + "(" + ",".join(entries) + ")"
    cur.execute(command)

def read_entry_database(cur:sqlite3.Cursor, table:str, target:str, columns:tuple[str], keys:tuple[str]) -> tuple:
    """Returns the entries that match the specified criteria

    Args:
        cursor (sqlite3.Cursor): cursor connected to the database
        table (str): table in the database
        target (str): name of the target entries column
        columns (tuple[str]): columns to search trough
        keys (tuple[str]): key for each column

    Returns:
        tuple: list of found entries
    """
    #target 
    #SELECT Value FROM table WHERE Name='key' AND Name='key'
    if len(columns) != len(keys):
        raise ValueError(f"columns and keys must have the same length\ncolumns : {columns}\nkeys : {keys}")
    command : str = f"SELECT {target} FROM {table} WHERE " + "=? AND ".join(columns) + "=?"
    try :
        cur.execute(command, keys)
        value = cur.fetchone()
        if value is None:
            raise sqlite3.Error("No entries matching the criteria")
        #return value
        return value
    except sqlite3.Error as e:
        #Something went wrong, return nothing
        print(e)
        print(f"{target} was not found, returned an empty tuple")
        return ()

def get_ids(cur:sqlite3.Cursor, name : str, id_type:str)->tuple[int]:
    """Returns the ids of all objects matching a given name

    Args:
        cur (sqlite3.Cursor): cursor connected to CommandCoin$.db
        name (str): name of the object we are trying to find the id of
        id_type (str): type of object, check the documentation

    Returns:
        tuple[int]: list of ids matching the same name, some object have unique names
    """
    check_valid_id_type(id_type)
    #f"{id_name}s" is the table
    #f"{id_name}_id" is the column with the ids we are trying to find
    #("name") is the column containing the names
    # name is the target 
    ids_str : tuple[str] = read_entry_database(cur, f"{id_type}s", f"{id_type}_id",("name",),(name,))
    ids = tuple(int(id_str) for id_str in ids_str)
    return ids

def get_id(cur:sqlite3.Cursor, name : str, id_name:str)-> int:
    """Returns the first matching id given a name,\n
    If none or more than one are found a sqlite3.IntegrityError will be thrown\n
    Should be used only when one and only one id is required   

    Args:
        cur (sqlite3.Cursor): cursor connected to CommandCoin$.db
        name (str): name of the object we are trying to find the id of
        id_name (str): type of object, check the documentation

    Returns:
        int: first matching id
    """
    ids : tuple[int] = get_ids(cur, name, id_name)
    if len(ids) == 0:
        raise sqlite3.IntegrityError(f"No {id_name} named {name} has been found")
    if len(ids) == 1:
        return ids[0]
    raise sqlite3.IntegrityError(f"Multiple {id_name} named {name} have been found")