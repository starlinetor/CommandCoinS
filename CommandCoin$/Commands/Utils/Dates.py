import datetime
import time
import Commands.Utils.SQL as SQL

def get_date_id(date:datetime.date) -> int:
    """Returns the id of a given date\n
    Date format "%Y-%m-%d"

    Args:
        date (str): date as a string ("%Y-%m-%d")

    Returns:
        int: id of the date
    """
    start_date : datetime.date = datetime.datetime.strptime(SQL.get_data("start_date"), "%Y-%m-%d").date()
    delta : datetime.timedelta = date-start_date 
    return delta.days