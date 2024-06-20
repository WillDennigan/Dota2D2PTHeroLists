import os
import json
import logging
from utils.parsing import get_meta_cheatsheet
from __init__ import __version__
os.system('mkdir C:\\DotaMetaLogs\\')
logging.basicConfig(level=logging.INFO,
                    filename=r'C:\DotaMetaLogs\log.log')

def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_live_updates_config(json_data):
    '''
    Updates the hero_grid_config.json with the hero IDs for each position
    '''
    categories = [
        {
            "category_name": "Safelane",
            "x_position": 0.0,
            "y_position": 0.0,
            "width": 378.0,
            "height": 333.0,
            "hero_ids": get_meta_cheatsheet('pos-1')
        },
        {
            "category_name": "Midlane",
            "x_position": 398.000000,
            "y_position": 0.000000,
            "width": 378.0,
            "height": 333.0,
            "hero_ids": get_meta_cheatsheet('pos-2')
        },
        {
            "category_name": "Offlane",
            "x_position": 796.000000,
            "y_position": 0.000000,
            "width": 378.0,
            "height": 333.0,
            "hero_ids": get_meta_cheatsheet('pos-3')
        },
        {
            "category_name": "Soft Support",
            "x_position": 171.000000,
            "y_position": 340.000000,
            "width": 378.0,
            "height": 333.0,
            "hero_ids": get_meta_cheatsheet('pos-4')
        },
        {
            "category_name": "Hard Support",
            "x_position": 609.000000,
            "y_position": 340.000000,
            "width": 378.0,
            "height": 333.0,
            "hero_ids": get_meta_cheatsheet('pos-5')
        }
    ]
    
    updated = False
    for config in json_data['configs']:
        if config['config_name'] == "Live Updates":
            config['categories'] = categories
            updated = True
            break
    
    if not updated:
        new_config = {
            "config_name": "Live Updates",
            "categories": categories
        }
        json_data['configs'].append(new_config)
    
    return json_data

def find_hero_grid_config_path():
    '''
    Searches for hero_grid_config.json in all drives for a Windows installation of Steam
    '''
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in drives:
        steam_userdata_path = os.path.join(drive, 'Program Files (x86)', 'Steam', 'userdata')
        if not os.path.exists(steam_userdata_path):
            steam_userdata_path = os.path.join(drive, 'Steam', 'userdata')
            if not os.path.exists(steam_userdata_path):
                continue
        
        logging.info(f"Searching for hero_grid_config.json in {steam_userdata_path}")
        
        for root, dirs, files in os.walk(steam_userdata_path):
            if 'hero_grid_config.json' in files and '570' in root.split(os.sep):
                found_path = os.path.join(root, 'hero_grid_config.json')
                logging.info(f"Found hero_grid_config.json at {found_path}")
                return found_path

    return None

if __name__ == '__main__':
    logging.info(f"Running live update script version: {__version__}")
    hero_grid_config_path = find_hero_grid_config_path()
    if hero_grid_config_path:
        logging.info(f"Found hero_grid_config.json at {hero_grid_config_path}")
        hero_grid_config = read_json(hero_grid_config_path)
        updated_config = add_live_updates_config(hero_grid_config)
        write_json(updated_config, hero_grid_config_path)
        logging.info(f"Hero IDs added to {hero_grid_config_path} under 'Live Updates'")
    else:
        logging.error("Could not find hero_grid_config.json on any drive")
