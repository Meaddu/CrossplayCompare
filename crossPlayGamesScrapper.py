#crossPlayGamesScrapper
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.trueachievements.com/xbox-game-pass/games"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_html(url):
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    return response.text

def parse_games(html):
    soup = BeautifulSoup(html, 'html.parser')
    games_data = []

    # Find all list items <li> with <a> tags that link to /game/ URLs
    for li in soup.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag and a_tag['href'].startswith('/game/'):
            title = a_tag.text.strip()
            link = "https://www.trueachievements.com" + a_tag['href']
            games_data.append({
                "Title": title,
                "Link": link
            })

    return games_data

def export_to_excel(games, filename):
    df = pd.DataFrame(games)
    df.to_excel(filename, index=False)
    print(f"✅ Exported {len(games)} games to {filename}")

def main():
    print("🎮 Fetching Xbox Game Pass games from TrueAchievements...")
    html = fetch_html(URL)
    games = parse_games(html)
    filename = f"xbox_game_pass_scraped_{datetime.now().strftime('%Y%m%d')}.xlsx"
    export_to_excel(games, filename)

if __name__ == "__main__":
    main()
