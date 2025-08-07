import datetime
import time
import Commands.Utils.SQL as SQL

def get_date_id(date:datetime.datetime) -> int:
    start_date : datetime.date = datetime.datetime.strptime(SQL.get_data("start_date"), "%Y-%m-%d").date()
    delta : datetime.timedelta = date-start_date 
    return delta.days