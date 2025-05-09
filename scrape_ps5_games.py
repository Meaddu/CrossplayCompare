import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

# Suppress SSL warnings (site uses HTTPS but doesn't serve a strict cert chain)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL for the full PS Plus catalog from PushSquare
URL = "https://www.pushsquare.com/guides/all-ps-plus-games"

# HTTP headers to mimic a standard browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_ps_plus_titles():
    """
    Fetches the list of PlayStation Plus catalog games from PushSquare.

    Returns:
        List[Dict]: A list of dictionaries with Title, Platforms, and Link.
    """
    try:
        response = requests.get(URL, headers=HEADERS, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Request failed:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    li_elements = soup.select('li[data-system]')

    titles = []

    for li in li_elements:
        a_tag = li.find('a', href=True)
        if not a_tag:
            continue

        title = a_tag.text.strip()
        link = "https://www.pushsquare.com" + a_tag['href']
        platforms = ', '.join(span.text.strip() for span in li.select('span.pill'))

        titles.append({
            "Title": title,
            "Platforms": platforms,
            "Link": link
        })

    return titles

def export_to_excel(titles):
    """
    Exports the list of games to an Excel file.

    Args:
        titles (List[Dict]): List of game entries to export.
    """
    if not titles:
        print("No data to export.")
        return

    df = pd.DataFrame(titles)
    filename = f"playstation_plus_catalog_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Exported {len(df)} records to {filename}")

def main():
    """
    Main entry point for scraping and exporting PS Plus catalog.
    """
    titles = fetch_ps_plus_titles()
    export_to_excel(titles)

if __name__ == "__main__":
    main()
