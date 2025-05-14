# utils/metacritic_enricher.py

import pandas as pd
from utils.metacritic import get_metacritic_score

def enrich_with_metacritic(input_csv_path, output_csv_path, limit=None):
    """
    Adds Metacritic scores to a CSV of games with a 'Title' column.

    Args:
        input_csv_path (str): Path to the input CSV
        output_csv_path (str): Path to save the updated CSV
        limit (int, optional): Max number of rows to process (for testing)
    """
    df = pd.read_csv(input_csv_path, encoding="utf-8-sig")

    if limit:
        df = df.head(limit)

    scores = []
    for title in df['Title']:
        score = get_metacritic_score(title)
        scores.append(score)

    df['MetacriticScore'] = scores
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved enriched CSV with Metacritic scores to: {output_csv_path}")
