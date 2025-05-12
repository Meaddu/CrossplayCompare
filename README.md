## CrossplayCompare

**CrossplayCompare** is a data scraping and comparison utility that aggregates game listings from:

* Xbox Game Pass
* PlayStation Plus
* Crossplay-enabled games (Xbox ↔ PlayStation)

It also enriches the final dataset with **Metacritic scores** via direct scraping.

---

### Features

* Scrapes and deduplicates Xbox Game Pass titles from TrueAchievements
* Scrapes and deduplicates PlayStation Plus titles from PushSquare
* Scrapes and deduplicates crossplay-enabled games from CrossplayGames
* Compares all three datasets to generate a list of common games
* Enriches the final result with Metacritic scores
* Outputs clean CSV files suitable for analysis or reporting

---

### Directory Structure

```
CrossplayCompare/
├── outputs/
│   ├── xbox_game_pass.csv
│   ├── playstation_plus_catalog.csv
│   ├── xbox_ps5_crossplay.csv
│   └── common_crossplay_ps_xbox.csv
│
├── scrapers/
│   ├── __init__.py
│   ├── xbox_game_pass.py
│   ├── ps_plus.py
│   └── crossplay_games.py
│
├── comparators/
│   ├── __init__.py
│   └── common_crossplay.py
│
├── utils/
│   ├── __init__.py
│   └── metacritic.py
│
├── run_full_catalog_pipeline.py
└── README.md
```

---

### Requirements

* Python 3.8+
* Internet access (Metacritic, PushSquare, CrossplayGames, TrueAchievements)

Install dependencies:

```bash
pip install requests beautifulsoup4 pandas
```

---

### Usage

Run the full pipeline with one command:

```bash
python run_full_catalog_pipeline.py
```

This will:

1. Scrape and store clean `Title` lists for each source
2. Identify common games across Xbox, PlayStation, and crossplay
3. Fetch and append Metacritic scores
4. Save the final result to:

   ```
   outputs/common_crossplay_ps_xbox.csv
   ```

---

### Notes

* Metacritic score fetching uses a slug-based strategy with direct page access.
* SSL verification is disabled for development environments (`verify=False`). Enable it for production.
* Includes retry safety and human-like pacing (`time.sleep`) to avoid request throttling.

---

### License

This project is for educational and internal use only. Respect each source site's `robots.txt` and terms of service.

---
