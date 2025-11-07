import datetime

date_format : str = "%Y-%m-%d"

def get_date_id(date:datetime.date, start_date_str : str) -> int:
    """Returns the id of a given date\n
    Date format "%Y-%m-%d"

    Args:
        date (str): date as a string ("%Y-%m-%d")

    Returns:
        int: id of the date
    """
    start_date : datetime.date = validate_date(start_date_str)
    delta : datetime.timedelta = date-start_date 
    return delta.days

def validate_date(date_2_validate:str) -> datetime.date:
    try:
        date : datetime.date = datetime.datetime.strptime(date_2_validate, "%Y-%m-%d").date()
    except ValueError as e:
        print(e)
        print("Returned date 1-1-1")
        return datetime.date(1,1,1)
    return date

#tests
def test():
    print(validate_date(str("12-09-2023")))   


if __name__ == "__main__":
    test()







