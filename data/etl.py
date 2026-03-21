import requests
from bs4 import BeautifulSoup
import json
import dotenv
import os

def ingest_data():
    """Here is where the ETL starts. We are ingesting data directly from the **API NAME** API, using the requests library and storing the information as a .json file"""
    
    folder_path = "data/raw"

    if os.path.exists(folder_path) and os.listdir(folder_path):
        print("Data already exists, skipping ingestion phase...")
        return

    print("Fetching data...")

    dotenv.load_dotenv()

    shooters = ["730#All"] #730 -> cs2; #All -> create the chart with information about all timeseries data
    rogues = ["646570#All"] #646570 -> slay the spire; #All -> create the chart with information about all timeseries data
    rpgs = ["1086940#All"] #1086940 -> bg3; #All -> create the chart with information about all timeseries data
    root_url = os.getenv("url")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    s_responses = [requests.get(root_url + s, headers=headers) for s in shooters]
    r_responses = [requests.get(root_url + r, headers=headers) for r in rogues]
    rpg_responses = [requests.get(root_url + rpg, headers=headers) for rpg in rpgs]

    s_html = [response.text for response in s_responses]
    r_html = [response.text for response in r_responses]
    rpg_html = [response.text for response in rpg_responses]

    for i, html in enumerate(s_html):    
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"class": "common-table"})
        rows = table.find_all("tr")[1:] #skip header of table

        data = []

        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")] #find each value for each column
    
            if cols:
                data.append({
                    "month": cols[0],
                    "avg_players": cols[1],
                    "gain": cols[2],
                    "percent_gain": cols[3],
                    "peak_players": cols[4]
                })

        with open(f"data/raw/{shooters[i]}.json", "w") as f:
            json.dump(data, f, indent=4)  

    for i, html in enumerate(r_html):    
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"class": "common-table"})
        rows = table.find_all("tr")[1:] #skip header of table

        data = []

        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")] #find each value for each column
    
            if cols:
                data.append({
                    "month": cols[0],
                    "avg_players": cols[1],
                    "gain": cols[2],
                    "percent_gain": cols[3],
                    "peak_players": cols[4]
                })

        with open(f"data/raw/{rogues[i]}.json", "w") as f:
            json.dump(data, f, indent=4)

    for i, html in enumerate(rpg_html):    
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"class": "common-table"})
        rows = table.find_all("tr")[1:] #skip header of table

        data = []

        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")] #find each value for each column
    
            if cols:
                data.append({
                    "month": cols[0],
                    "avg_players": cols[1],
                    "gain": cols[2],
                    "percent_gain": cols[3],
                    "peak_players": cols[4]
                })

        with open(f"data/raw/{rpgs[i]}.json", "w") as f:
            json.dump(data, f, indent=4)  

    print("Data ingested successfully!")

    return

def run_etl():
    ingest_data()