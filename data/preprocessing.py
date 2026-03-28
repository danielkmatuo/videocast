import pandas as pd
import os

def join_data():
    cwd = os.getcwd()
    files = os.listdir(path=cwd + "\\data\\raw")

    games = {
        "apex_legends": "shooter",
        "bg3": "rpg",
        "children_of_morta": "roguelike",
        "cs2": "shooter",
        "darkest_dungeon": "roguelike",
        "dead_cells": "rogue_like",
        "destiny_2": "shooter",
        "divinity_2": "rpg",
        "ds3": "rpg",
        "elden_ring": "rpg",
        "enter_the_gungeon": "roguelike",
        "expedition_33": "rpg",
        "for_the_king": "roguelike",
        "hades": "roguelike",
        "isaac_rebirth": "roguelike",
        "l4d2": "shooter",
        "marvel_rivals": "shooter",
        "megabonk": "roguelike",
        "overwatch_2": "shooter",
        "path_of_exile": "rpg",
        "persona_5": "rpg",
        "pubg": "shooter",
        "rainbow_six": "shooter",
        "risk_of_rain_2": "roguelike",
        "skyrim": "rpg",
        "slay_the_spire": "roguelike",
        "tf2": "shooter",
        "the_witcher_3": "rpg",
        "ultrakill": "shooter",
        "undertale": "rpg",                
    }

    shooter_dfs = []
    rogue_dfs = []
    rpg_dfs = []

    data_dir = "data/raw/"

    for file in files:
        split_file = file.split("_") #First split the file name, then separate game name from game id
        game_id = None

        for i, elem in enumerate(split_file):
            if elem.find(".json") > -1:
                elem = elem.replace(".json", "")

                if elem.isdigit():
                    game_id = elem
                    split_file.pop(i) #Works only because game id is the last element of list for each .json file

        game_name = "_".join(split_file)
        game_category = games[game_name]

        df = pd.read_json(data_dir + file)
        df["game_name"] = game_name
        df["game_id"] = game_id
        df["category"] = game_category
        
        match game_category:
            case "shooter":
                shooter_dfs.append(df)
            case "roguelike":
                rogue_dfs.append(df)
            case "rpg":
                rpg_dfs.append(df)

    shooter_df = pd.concat(shooter_dfs, ignore_index=True)
    rogue_df = pd.concat(rogue_dfs, ignore_index=True)
    rpg_df = pd.concat(rpg_dfs, ignore_index=True)

    final_df = pd.concat([shooter_df, rogue_df, rpg_df], ignore_index=True)

    return final_df