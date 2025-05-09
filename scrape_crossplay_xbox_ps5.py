import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

# Disable SSL warnings (only safe for public scraping)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://crossplaygames.com/crossplay?p1=xbox-sx&p2=playstation-5"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_crossplay_titles():
    response = requests.get(URL, headers=HEADERS, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = []

    for li in soup.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag and a_tag['href'].startswith("https://crossplaygames.com/games/"):
            title = a_tag.text.strip()
            link = a_tag['href']
            titles.append({
                "Title": title,
                "Link": link
            })

    return titles

def export_to_excel(titles):
    df = pd.DataFrame(titles)
    filename = f"xbox_ps5_crossplay_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Exported {len(df)} crossplay titles to {filename}")

def main():
    print("🔄 Fetching crossplay data from crossplaygames.com...")
    titles = fetch_crossplay_titles()
    export_to_excel(titles)

if __name__ == "__main__":
    main()
