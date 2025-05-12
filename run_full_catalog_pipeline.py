# run_full_catalog_pipeline.py
# One-click script to run all three scrapers, export to CSV, and generate comparison report

import os
import pandas as pd
from scrapers.xbox_game_pass import get_xbox_game_pass_data
from scrapers.crossplay_games import get_crossplay_games
from scrapers.ps_plus import get_ps_plus_data
from comparators.common_crossplay import compare_common_games

def ensure_output_directory():
    os.makedirs("outputs", exist_ok=True)

def run_pipeline():
    ensure_output_directory()

    # Fetch Xbox Game Pass games
    xbox_df = get_xbox_game_pass_data()
    xbox_df['NormalizedTitle'] = xbox_df['Title'].str.strip().str.lower()
    xbox_df = xbox_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    xbox_df.to_csv("outputs/xbox_game_pass.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(xbox_df)} Xbox Game Pass games")

    # Fetch crossplay games between Xbox and PS5
    crossplay_df = get_crossplay_games()
    crossplay_df['NormalizedTitle'] = crossplay_df['Title'].str.strip().str.lower()
    crossplay_df = crossplay_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    crossplay_df.to_csv("outputs/xbox_ps5_crossplay.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(crossplay_df)} Xbox–PS5 crossplay games")

    # Fetch PlayStation Plus catalog
    ps_df = get_ps_plus_data()
    ps_df['NormalizedTitle'] = ps_df['Title'].str.strip().str.lower()
    ps_df = ps_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    ps_df.to_csv("outputs/playstation_plus_catalog.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(ps_df)} PlayStation Plus games")

    # Compare and export intersection
    compare_common_games(xbox_df, ps_df, crossplay_df, "outputs/common_crossplay_ps_xbox.xlsx")

    print("Data scraping and comparison pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()