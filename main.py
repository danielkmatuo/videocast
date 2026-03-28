from data.etl import run_etl
from data.preprocessing import join_data

def main():
    run_etl()

    main_df = join_data()

if __name__ == "__main__":
    main()