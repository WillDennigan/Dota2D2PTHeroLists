import os
import requests
try:
    from bs4 import BeautifulSoup
except:
    os.system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup

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
    Returns a list of hero IDs for the given position using D2PT cheatsheet
    '''
    url = f"https://dota2protracker.com/cheatsheets/{position}"
    response = requests.get(url)
    if response.status_code == 200:
        heroes = parse_cheatsheet(response.text)
        ids = find_hero_id(heroes)
        return ids
    else:
        return None