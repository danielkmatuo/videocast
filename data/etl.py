import requests
from bs4 import BeautifulSoup
import json
import dotenv
import os

def fetch_raw_data():
    """Here is where the ETL starts. We are ingesting data directly from the SteamCharts website, using the requests library and storing the information as a .json file"""
    
    folder_path = "data/raw"

    if os.path.exists(folder_path) and os.listdir(folder_path):
        print("Data already exists, skipping ingestion phase...")
        return

    print("Fetching data...")

    dotenv.load_dotenv()

    shooters = {
        "cs2": "730",
        "overwatch_2": "2357570",
        "apex_legends": "1172470",
        "rainbow_six": "359550",
        "ultrakill": "1229490",
        "marvel_rivals": "2767030",
        "tf2": "440",
        "l4d2": "550",
        "pubg": "578080",
        "destiny_2": "1085660"
    }

    rogues = {
        "slay_the_spire": "646570",
        "hades": "1145360",
        "darkest_dungeon": "262060",
        "isaac_rebirth": "250900",
        "enter_the_gungeon": "311690",
        "risk_of_rain_2": "632360",
        "children_of_morta": "330020",
        "megabonk": "3405340",
        "for_the_king": "527230",
        "dead_cells": "588650"
    }

    rpgs = {
        "bg3": "1086940",
        "divinity_2": "435150",
        "elden_ring": "1245620",
        "ds3": "374320",
        "skyrim": "374320",
        "path_of_exile": "238960",
        "undertale": "391540",
        "the_witcher_3": "292030",
        "persona_5": "1687950",
        "expedition_33": "1903340"
    }
    
    root_url = os.getenv("url")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        s_responses = [requests.get(root_url + shooters[key], headers=headers) for key in shooters.keys()]
        r_responses = [requests.get(root_url + rogues[key], headers=headers) for key in rogues.keys()]
        rpg_responses = [requests.get(root_url + rpgs[key], headers=headers) for key in rpgs.keys()]
    except Exception:
        print("Something went wrong while fetching the data... Cancelling operation...")

    s_html = [response.text for response in s_responses]
    r_html = [response.text for response in r_responses]
    rpg_html = [response.text for response in rpg_responses]

    s_keys = list(shooters.keys())
    r_keys = list(rogues.keys())
    rpg_keys = list(rpgs.keys())

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

        with open(f"data/raw/{s_keys[i] + "_" + shooters[s_keys[i]]}.json", "w") as f:
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

        with open(f"data/raw/{r_keys[i] + "_" + rogues[r_keys[i]]}.json", "w") as f:
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

        with open(f"data/raw/{rpg_keys[i] + "_" + rpgs[rpg_keys[i]]}.json", "w") as f:
            json.dump(data, f, indent=4)  

    print("Data fetched successfully!")

    return