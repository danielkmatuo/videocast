import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.seasonal as tsa
from statsmodels.graphics.tsaplots import plot_acf
from datetime import datetime
import calendar
import os

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

def plot_general_trend_per_bucket(df: pd.DataFrame, agg_df: pd.DataFrame):
    for bucket in df["year_bucket"].unique():
        subset = agg_df.loc[bucket]

        plt.figure()
        plt.plot(subset.index, subset["avg_players"], label=f"{bucket} avg", color="blue")
        plt.plot(subset.index, subset["peak_players"], linestyle="--", label=f"{bucket} peak", color="green")
        
        plt.legend()
        plt.xlabel("Month")
        plt.ylabel("Players")
        plt.title("Trend per Year Bucket")
        
        if not os.path.exists("plots/"):
            os.makedirs("plots/")
            print("Directory created: plots/")
        elif not os.path.exists(f"plots/bucket_{bucket}/"):
            os.makedirs(f"plots/bucket_{bucket}/")
            print(f"Directory created: plots/bucket_{bucket}/")

        plt.savefig(f"plots/bucket_{bucket}/general_trend_{bucket}.png")
        plt.close()
        print(f"File created: general_trend_{bucket}.png")

def group_by_category(df: pd.DataFrame):
    temp_df = df.copy()

    category_grouped = temp_df.groupby(["category", "year_bucket", "month"])[["avg_players", "peak_players"]].agg("sum")

    return category_grouped

def plot_by_category(df: pd.DataFrame):
    temp_df = df.reset_index()
    
    for bucket in temp_df["year_bucket"].unique():
        bucket_df = temp_df[temp_df["year_bucket"] == bucket]
        for category in bucket_df["category"].unique():
            subset = bucket_df[bucket_df["category"] == category]
            
            plt.figure()
            plt.plot(subset.index, subset["avg_players"], label=f"{category} {bucket} avg", color="blue")
            plt.plot(subset.index, subset["peak_players"], label=f"{category} {bucket} peak", color="green")

            plt.legend()
            plt.xlabel("Month")
            plt.ylabel("Players")
            plt.title(f"{category} trend for games released in {bucket}")
            
            if not os.path.exists("plots/"):
                os.makedirs("plots/")
                print("Directory created: plots/")
            elif not os.path.exists(f"plots/bucket_{bucket}/"):
                os.makedirs(f"plots/bucket_{bucket}/")
                print(f"Directory created: plots/bucket_{bucket}/")

            plt.savefig(f"plots/bucket_{bucket}/{category}_{bucket}_trend.png")
            plt.close()
            print(f"File created: plots/bucket_{bucket}/{category}_{bucket}_trend.png")

def bucket_decompose(df: pd.DataFrame, bucket: int):
    try:
        subset = df.loc[bucket]
    except KeyError as e:
        print(f"Invalid year ({e})")
        return
    
    print(f"Decomposing avg_players data for {bucket}")
    decompose = tsa.seasonal_decompose(x=subset["avg_players"], model="additive", period=12)

    decompose.plot()

    plt.show()

def category_decompose(df: pd.DataFrame, category: str, bucket: int): 
    df = df.reset_index()
    subset = df[(df["category"] == category) & (df["year_bucket"] == bucket)]
    
    if len(subset.index) == 0:
        print(f"There is no game from category {category} released in the year {bucket}")
        return

    print(f"Decomposing avg_players data for {category} with release year {bucket}")
    decompose = tsa.seasonal_decompose(x=subset["avg_players"], model="additive", period=12)

    decompose.plot()

    plt.show()

def acf_plot_per_bucket(df: pd.DataFrame, agg_df: pd.DataFrame):
    for bucket in df["year_bucket"].unique():
        subset = agg_df.loc[bucket]
        subset = subset.sort_index()

        fig = plot_acf(x=subset["avg_players"], title=f"ACF for games with release year {bucket}", alpha=0.05)

        fig.savefig(f"plots/bucket_{bucket}/general_acf_{bucket}.png")
        plt.close(fig)
        print(f"ACF plot file created: plots/bucket_{bucket}/general_acf_{bucket}.png")

def acf_plot_per_category(df: pd.DataFrame):
    temp_df = df.reset_index()
    
    for bucket in temp_df["year_bucket"].unique():
        bucket_df = temp_df[temp_df["year_bucket"] == bucket]
        for category in bucket_df["category"].unique():
            subset = bucket_df[bucket_df["category"] == category]
            subset = subset.sort_index()
                                    
            fig = plot_acf(x=subset["avg_players"], title=f"ACF for game within category {category} with release year {bucket}", alpha=0.05)

            fig.savefig(f"plots/bucket_{bucket}/{category}_acf_{bucket}.png")
            plt.close(fig)
            print(f"ACF plot file created: plots/bucket_{bucket}/{category}_acf_{bucket}.png")

def calculate_share(df: pd.DataFrame, bucket: int):
    subset = df[df["year_bucket"] == bucket]

    if len(subset.index) == 0: 
        print(f"There is no game released in the year {bucket}")

    dfs = []

    for date in subset["month"].unique():
        date_df = subset[subset["month"] == date]
        avg_total_players_month = date_df["avg_players"].sum()
        peak_total_players_month = date_df["peak_players"].sum()

        date_df["market_share_avg"] = date_df["avg_players"].apply(lambda x: (x / avg_total_players_month) * 100)
        date_df["market_share_peak"] = date_df["peak_players"].apply(lambda x: (x / peak_total_players_month) * 100)
        dfs.append(date_df)

    temp_df = pd.concat(dfs)

    print(temp_df.to_string())

    return temp_df