"""
    Main file to perform writing operations
"""
import os
import json

DATA_FILE_PATH = f"{os.environ['HOME']+os.path.sep}.birthdays_reminder/data.json"

def set_initial_data_settings():
    """Create a json file with initial settings
    """
    initial_settings = dict()
    initial_settings['settings'] = dict(photo=True, repeat=False,  countdown_days=1)
    initial_settings['contacts'] = {}

    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(initial_settings, file)


def add_birthday():
    name = input("Type contact's name: ")
    date = input("Type date of birth (YYYY-MM-DD): ")

    with open(DATA_FILE_PATH, 'r') as file:
        data = json.load(file)
    with open(DATA_FILE_PATH, 'w') as file:
        data['contacts'][name] = date
        json.dump(data, file)