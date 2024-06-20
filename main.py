import os
import json
import requests
from bs4 import BeautifulSoup

def get_mid_meta_cheatsheet():
    url = "https://dota2protracker.com/cheatsheets/pos-2"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
def parse_cheatsheet(html):
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
    url = 'https://api.opendota.com/api/heroes'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hero_id = {}
        for hero in data:
            if hero['localized_name'].lower() in heroes:
                hero_id[hero['localized_name'].lower()] = hero['id']
        return hero_id
    else:
        return None
    
def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_live_updates_config(json_data, hero_ids):
    updated = False
    for config in json_data['configs']:
        if config['config_name'] == "Live Updates":
            config['categories'][0]['hero_ids'] = list(hero_ids.values())
            updated = True
            break
    
    if not updated:
        new_config = {
            "config_name": "Live Updates",
            "categories": [
                {
                    "category_name": "Midlane",
                    "x_position": 0.0,
                    "y_position": 0.0,
                    "width": 627.0,
                    "height": 236.0,
                    "hero_ids": list(hero_ids.values())
                }
            ]
        }
        json_data['configs'].append(new_config)
    
    return json_data

def find_hero_grid_config_path():
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in drives:
        steam_userdata_path = os.path.join(drive, 'Program Files (x86)', 'Steam', 'userdata')
        if not os.path.exists(steam_userdata_path):
            steam_userdata_path = os.path.join(drive, 'Steam', 'userdata')
            if not os.path.exists(steam_userdata_path):
                continue
        
        print(f"Searching for hero_grid_config.json in {steam_userdata_path}")
        
        for root, dirs, files in os.walk(steam_userdata_path):
            if 'hero_grid_config.json' in files and '570' in root.split(os.sep):
                found_path = os.path.join(root, 'hero_grid_config.json')
                print(f"Found hero_grid_config.json at {found_path}")
                return found_path

    return None

if __name__ == '__main__':
    html = get_mid_meta_cheatsheet()
    if html:
        heroes = parse_cheatsheet(html)
        hero_ids = find_hero_id(heroes)
        if hero_ids:
            hero_grid_config_path = find_hero_grid_config_path()
            if hero_grid_config_path:
                hero_grid_config = read_json(hero_grid_config_path)
                updated_config = add_live_updates_config(hero_grid_config, hero_ids)
                write_json(updated_config, hero_grid_config_path)
                print(f"Hero IDs added to {hero_grid_config_path} under 'Live Updates'")
            else:
                print("Could not find hero_grid_config.json on any drive")
        else:
            print("Failed to fetch hero IDs")
    else:
        print("Failed to fetch cheatsheet")
