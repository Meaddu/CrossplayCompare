# comparators/common_crossplay.py
# Compares Xbox Game Pass, PlayStation Plus, and Crossplay games
# Outputs a CSV file of games that are common across all three lists

import pandas as pd

def normalize_title(title):
    """Normalize title for consistent comparison."""
    return title.strip().lower()

def compare_common_games(xbox_df, ps_df, crossplay_df, output_path):
    """
    Compares normalized titles across all three DataFrames and saves common entries to a CSV.

    Args:
        xbox_df (pd.DataFrame): Xbox Game Pass games
        ps_df (pd.DataFrame): PlayStation Plus games
        crossplay_df (pd.DataFrame): Crossplay-enabled games
        output_path (str): CSV file path to export
    """
    xbox_titles = set(xbox_df['Title'].map(normalize_title))
    ps_titles = set(ps_df['Title'].map(normalize_title))
    crossplay_titles = set(crossplay_df['Title'].map(normalize_title))

    # Find intersection of all three sources
    common_titles = xbox_titles & ps_titles & crossplay_titles

    # Extract rows matching the common titles
    common_xbox = xbox_df[xbox_df['Title'].map(normalize_title).isin(common_titles)]
    common_ps = ps_df[ps_df['Title'].map(normalize_title).isin(common_titles)]
    common_crossplay = crossplay_df[crossplay_df['Title'].map(normalize_title).isin(common_titles)]

    # Merge on title
    merged = pd.merge(common_xbox, common_ps, on='Title', suffixes=('_Xbox', '_PS'))
    merged = pd.merge(merged, common_crossplay, on='Title')

    # Drop all other columns and keep only unique Title
    merged = merged[['Title']].drop_duplicates()

    # Save to CSV
    merged.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Exported {len(merged)} common crossplay games to {output_path}")
