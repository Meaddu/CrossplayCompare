# === scrapers/xbox_game_pass.py ===
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.trueachievements.com/xbox-game-pass/games"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_xbox_game_pass_data():
    print("Sending request to TrueAchievements...")
    try:
        response = requests.get(URL, headers=HEADERS, verify=False)
        response.raise_for_status()
        print("Successfully fetched data from TrueAchievements.")
    except requests.RequestException as e:
        print("Failed to fetch data:", e)
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    print("Parsing HTML...")
    for li in soup.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag and a_tag['href'].startswith('/game/'):
            title = a_tag.text.strip()
            link = "https://www.trueachievements.com" + a_tag['href']
            data.append({"Title": title, "Link": link})

    print(f"Found {len(data)} games.")

    df = pd.DataFrame(data)

    output_dir = "outputs"
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "xbox_game_pass.csv")
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    return df