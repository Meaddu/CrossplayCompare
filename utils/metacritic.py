# utils/metacritic.py
# Fetches Metacritic score from direct URL with updated HTML structure

import requests
from bs4 import BeautifulSoup
import time
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://www.metacritic.com/game/"

def slugify(title):
    """
    Converts a game title to a URL-friendly slug.
    E.g., "It Takes Two" -> "it-takes-two"
    """
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'\s+', '-', title.strip())
    return title

def get_metacritic_score(title):
    """
    Fetches Metacritic score from the direct game URL.
    Returns integer score or None.
    """
    try:
        print(f"Looking up score for: {title}")
        slug = slugify(title)
        url = BASE_URL + slug
        print(f"Trying URL: {url}")

        response = requests.get(url, headers=HEADERS, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Updated selector based on your screenshot
        score_tag = soup.select_one("div.c-siteReviewScore span")
        if score_tag:
            score = score_tag.text.strip()
            print(f"Score found: {score}")
            return int(score)
        else:
            print("No score found on page.")
            return None

    except Exception as e:
        print(f"Error fetching score for {title}: {e}")
        return None
