"""
    Main file to perform writing operations
"""
import os
import json

DATA_FILE_PATH = f"{os.environ['HOME']+os.path.sep}.birthdays_reminder/data.json"

def set_initial_data_settings(path=DATA_FILE_PATH):
    initial_settings = dict()
    initial_settings['settings'] = dict(photo=True, repeat=False,  countdown_days=1)
    initial_settings['contacts'] = {}

    with open(path, 'w') as file:
        json.dump(initial_settings, file)