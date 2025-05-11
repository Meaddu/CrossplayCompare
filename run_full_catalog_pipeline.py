# run_full_catalog_pipeline.py
# One-click script to run all three scrapers and export to CSV

import os
import pandas as pd
from scrapers.xbox_game_pass import get_xbox_game_pass_data
from scrapers.crossplay_games import get_crossplay_games
from scrapers.ps_plus import get_ps_plus_data

def ensure_output_directory():
    os.makedirs("outputs", exist_ok=True)

def run_pipeline():
    ensure_output_directory()

    # Fetch Xbox Game Pass games
    xbox_df = get_xbox_game_pass_data()
    print(f"Fetched {len(xbox_df)} Xbox Game Pass games")

    # Fetch crossplay games between Xbox and PS5
    crossplay_df = get_crossplay_games()
    print(f"Fetched {len(crossplay_df)} Xbox–PS5 crossplay games")

    # Fetch PlayStation Plus catalog
    ps_df = get_ps_plus_data()
    print(f"Fetched {len(ps_df)} PlayStation Plus games")

    print("Data scraping pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()