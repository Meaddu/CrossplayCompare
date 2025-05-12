import pandas as pd

def normalize_title(title):
    return title.strip().lower()

def compare_common_games(xbox_df, ps_df, crossplay_df, output_path):
    xbox_titles = set(xbox_df['Title'].map(normalize_title))
    ps_titles = set(ps_df['Title'].map(normalize_title))
    crossplay_titles = set(crossplay_df['Title'].map(normalize_title))

    # Intersection
    common_titles = xbox_titles & ps_titles & crossplay_titles

    common_xbox = xbox_df[xbox_df['Title'].map(normalize_title).isin(common_titles)]
    common_ps = ps_df[ps_df['Title'].map(normalize_title).isin(common_titles)]
    common_crossplay = crossplay_df[crossplay_df['Title'].map(normalize_title).isin(common_titles)]

    # Merge on title
    merged = pd.merge(common_xbox, common_ps, on='Title', suffixes=('_Xbox', '_PS'))
    merged = pd.merge(merged, common_crossplay, on='Title')

    merged.to_excel(output_path, index=False)
    print(f"Exported {len(merged)} common crossplay games to {output_path}")
