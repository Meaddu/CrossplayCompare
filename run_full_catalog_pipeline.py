# run_full_catalog_pipeline.py
# One-click script to run all three scrapers, export to CSV, and generate comparison report

import os
import pandas as pd
from scrapers.xbox_game_pass import get_xbox_game_pass_data
from scrapers.crossplay_games import get_crossplay_games
from scrapers.ps_plus import get_ps_plus_data
from comparators.common_crossplay import compare_common_games
from utils.metacritic import get_metacritic_score
from utils.metacritic_enricher import enrich_with_metacritic
import time

def ensure_output_directory():
    os.makedirs("outputs", exist_ok=True)

def append_metacritic_scores(csv_path):
    print(f"Reading data from {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    scores = []
    for title in df['Title']:
        print(f"Fetching score for: {title}")
        score = get_metacritic_score(title)
        scores.append(score)
        time.sleep(1)
    df['MetacriticScore'] = scores
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Appended Metacritic scores to {csv_path}")

def run_pipeline():
    ensure_output_directory()

    # Fetch Xbox Game Pass games
    xbox_df = get_xbox_game_pass_data()
    xbox_df['NormalizedTitle'] = xbox_df['Title'].str.strip().str.lower()
    xbox_df = xbox_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    xbox_df = xbox_df[['Title']]
    xbox_df.to_csv("outputs/xbox_game_pass.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(xbox_df)} Xbox Game Pass games")

    # Fetch crossplay games between Xbox and PS5
    crossplay_df = get_crossplay_games()
    crossplay_df['NormalizedTitle'] = crossplay_df['Title'].str.strip().str.lower()
    crossplay_df = crossplay_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    crossplay_df = crossplay_df[['Title']]
    crossplay_df.to_csv("outputs/xbox_ps5_crossplay.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(crossplay_df)} Xbox–PS5 crossplay games")

    #Append Metacritic score to Xbox-PS5 Crossplay List
    enrich_with_metacritic(
        input_csv_path="outputs/xbox_ps5_crossplay.csv",
        output_csv_path="outputs/xbox_ps5_crossplay_scored.csv"
    )

    # Fetch PlayStation Plus catalog
    ps_df = get_ps_plus_data()
    ps_df['NormalizedTitle'] = ps_df['Title'].str.strip().str.lower()
    ps_df = ps_df.drop_duplicates(subset='NormalizedTitle').drop(columns='NormalizedTitle')
    ps_df = ps_df[['Title']]
    ps_df.to_csv("outputs/playstation_plus_catalog.csv", index=False, encoding="utf-8-sig")
    print(f"Fetched {len(ps_df)} PlayStation Plus games")

    # Compare and export intersection
    compare_common_games(xbox_df, ps_df, crossplay_df, "outputs/common_crossplay_ps_xbox.csv")

    # Add Metacritic scores to the common games
    append_metacritic_scores("outputs/common_crossplay_ps_xbox.csv")

    print("Data scraping and comparison pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
