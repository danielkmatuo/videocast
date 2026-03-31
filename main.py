from data.etl import fetch_raw_data
from data.preprocessing import join_data
from exploration import *

def main():
    #Run ETL ==================================================================================================================================================================================
    fetch_raw_data()

    #Preprocess the data even further =========================================================================================================================================================
    preprocessed_df = join_data()

    #Start of EDA =============================================================================================================================================================================
    #EDA - Transformation of data
    date_norm_df = normalize_dates(preprocessed_df)
    num_norm_df = normalize_num_data(date_norm_df)

    release_date_df = get_release_date(num_norm_df)
    year_buckets_df = separate_buckets(release_date_df)
    players_by_bucket_df = sum_players_by_bucket(year_buckets_df)
    
    #EDA - Ploting
    #General plot by bucket
    plot_general_trend_per_bucket(players_by_bucket_df, bucket=2023) #bucket param can go from 2012 to 2025

if __name__ == "__main__":
    main()