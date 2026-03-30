import pandas as pd
from datetime import datetime
import calendar

def parse_month(month_str):
    months_dict = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    split_month = month_str.lower().split(" ") #2 cases -> 1. "month year"; 2. "last 30 days"
    day = None
    month = None
    year = None
    
    if split_month[0] in months_dict.keys():
        month = months_dict[split_month[0]]
        year = int(split_month[1])
        day = calendar.monthrange(year=year, month=month)[1] #calendar.monthrange() returns tuple(weekday_of_first_day, number_of_days)
    else:
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

    return datetime(day=day, month=month, year=year)

def normalize_dates(df: pd.DataFrame):    
    temp_df = df.copy()

    temp_df["month"] = temp_df["month"].apply(lambda x: parse_month(x))

    print(temp_df)