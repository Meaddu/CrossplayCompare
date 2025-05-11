# === scrapers/crossplay_games.py ===
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://crossplaygames.com/crossplay?p1=xbox-sx&p2=playstation-5"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_crossplay_games():
    response = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for li in soup.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag and a_tag['href'].startswith("https://crossplaygames.com/games/"):
            title = a_tag.text.strip()
            link = a_tag['href']
            data.append({"Title": title, "Link": link})

    df = pd.DataFrame(data)
    df.to_csv("outputs/xbox_ps5_crossplay.csv", index=False)
    return df