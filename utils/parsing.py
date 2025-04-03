import os

# Install dependencies if missing
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    os.system('pip install playwright')
    from playwright.sync_api import sync_playwright
    os.system('python -m playwright install')

try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup

import requests

def parse_cheatsheet(html):
    '''
    Parses the D2PT cheatsheet page and returns a list of hero names
    '''
    soup = BeautifulSoup(html, 'html.parser')
    heroes = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/hero/'):
            hero_name = link['href'].split('/hero/')[1]
            if '/new' in hero_name:
                continue
            else:
                heroes.append(hero_name.lower())
    return heroes

def find_hero_id(heroes):
    '''
    Returns a list of hero IDs for the given hero names using opendota API
    '''
    url = 'https://api.opendota.com/api/heroes'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hero_id = []
        hero_name_to_id = {hero['localized_name'].lower(): hero['id'] for hero in data}
        for hero_name in heroes:
            if hero_name.lower() in hero_name_to_id:
                hero_id.append(hero_name_to_id[hero_name.lower()])
        return hero_id
    else:
        return None

def get_meta_cheatsheet(position):
    '''
    Uses Playwright to scrape rendered HTML from D2PT and returns hero IDs for the position
    '''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"https://dota2protracker.com/cheatsheets/{position}"
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()

    heroes = parse_cheatsheet(html)
    ids = find_hero_id(heroes)
    return ids