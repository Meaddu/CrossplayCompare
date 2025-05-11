# === scrapers/ps_plus.py ===
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.pushsquare.com/guides/all-ps-plus-games"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_ps_plus_data():
    response = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for li in soup.select('li[data-system]'):
        a_tag = li.find('a', href=True)
        if not a_tag:
            continue
        title = a_tag.text.strip()
        link = "https://www.pushsquare.com" + a_tag['href']
        platforms = ', '.join(span.text.strip() for span in li.select('span.pill'))
        data.append({"Title": title, "Platforms": platforms, "Link": link})

    df = pd.DataFrame(data)
    df.to_csv("outputs/playstation_plus_catalog.csv", index=False)
    return df