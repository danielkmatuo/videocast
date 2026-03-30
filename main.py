from data.etl import fetch_raw_data
from data.preprocessing import join_data
from exploration import normalize_dates

def main():
    fetch_raw_data()

    main_df = join_data()

    normalize_dates(main_df)

if __name__ == "__main__":
    main()