import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.seasonal as tsa
from datetime import datetime
import calendar

#Support functions
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

def parse_num_with_signal(value): #4 cases -> "value" or "-value" or "-"
    if value == "-":
        new_value = 0.0

        return new_value
    elif value.find("-") > -1:
        new_str = value[1:]
        new_value = float(new_str) * -1

        return new_value
    else:
        return float(value)

def return_datetime(x):
    return pd.to_datetime(x)

#Main functions
def normalize_dates(df: pd.DataFrame):    
    temp_df = df.copy()

    temp_df["month"] = temp_df["month"].apply(lambda x: parse_month(x))

    return temp_df

def normalize_num_data(df: pd.DataFrame):
    temp_df = df.copy()

    temp_df["avg_players"] = temp_df["avg_players"].astype(float)
    temp_df["peak_players"] = temp_df["peak_players"].astype(int)

    temp_df["gain"] = temp_df["gain"].apply(lambda x: parse_num_with_signal(x))
    temp_df["percent_gain"] = temp_df["percent_gain"].apply(lambda x: parse_num_with_signal(x.replace("%", "").replace("+", "")))

    return temp_df

def get_release_date(df: pd.DataFrame):
    temp_df = df.copy()
    temp_df["release_date"] = df.groupby("game_id")["month"].transform("min")

    return temp_df

def separate_buckets(df: pd.DataFrame):
    temp_df = df.copy()
    
    year_buckets_s = temp_df["release_date"].apply(lambda x: return_datetime(x).year)

    temp_df["year_bucket"] = year_buckets_s

    return temp_df

def sum_players_by_bucket(df):
    temp_df = df.copy()
    
    return temp_df.groupby(["year_bucket", "month"])[["avg_players", "peak_players"]].agg("sum")

def plot_general_trend_per_bucket(df: pd.DataFrame, bucket: int):
    try:
        subset = df.loc[bucket]
    except KeyError as e:
        print(f"Invalid year ({e})")
        return

    plt.plot(subset.index, subset["avg_players"], label=f"{bucket} avg", color="blue")
    plt.plot(subset.index, subset["peak_players"], linestyle="--", label=f"{bucket} peak", color="green")
    
    plt.legend()
    plt.xlabel("Month")
    plt.ylabel("Players")
    plt.title("Trend per Year Bucket")
    plt.show()
    plt.show()

def group_by_category(df: pd.DataFrame):
    temp_df = df.copy()

    category_grouped = temp_df.groupby(["category", "month"])[["avg_players", "peak_players"]].agg("sum")

    return category_grouped

def plot_by_category(df: pd.DataFrame, category: str):
    try:
        subset = df.loc[category]
    except KeyError as e:
        print(f"Invalid category ({e})")
        return

    plt.plot(subset.index, subset["avg_players"], label=f"{category} avg", color="blue")
    plt.plot(subset.index, subset["peak_players"], label=f"{category} peak", color="green")

    plt.legend()
    plt.xlabel("Month")
    plt.ylabel("Players")
    plt.title(f"{category} Trend per Month")
    plt.show()
    plt.show()

def decompose_time_series_per_bucket(df: pd.DataFrame, bucket: int):
    try:
        subset = df.loc[bucket]
    except KeyError as e:
        print(f"Invalid year ({e})")
        return
    
    print(f"Decomposing avg_players data for {bucket}")
    decompose = tsa.seasonal_decompose(x=subset["avg_players"], model="additive", period=12)

    decompose.plot()

    plt.show()

def decompose_timeseries_per_category(df: pd.DataFrame, category: str): 
    try:
        subset = df.loc[category]
    except KeyError as e:
        print(f"Invalid category ({e})")
        return
    
    print(f"Decomposing avg_players data for {category}")
    decompose = tsa.seasonal_decompose(x=subset["avg_players"], model="additive", period=12)

    decompose.plot()

    plt.show()