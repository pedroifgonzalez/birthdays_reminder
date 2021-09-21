"""
    Main file to perform writing operations
"""
import os
import json

DATA_FILE_PATH = (
    f"{os.environ['HOME']+os.path.sep}.birthdays_reminder{os.path.sep}data.json"
)
CONTACTS_PHOTOS_PATH = f"{os.environ['HOME']+os.path.sep}.birthdays_reminder{os.path.sep}contacts{os.path.sep}"


def set_initial_data_settings():
    """Create a json file with initial settings"""
    initial_settings = dict()
    initial_settings["settings"] = dict(photo=True, repeat=False, countdown_days=1)
    initial_settings["contacts"] = {}
    initial_settings["anniversaries"] = {}

    with open(DATA_FILE_PATH, "w") as file:
        json.dump(initial_settings, file)

    os.mkdir(CONTACTS_PHOTOS_PATH)


def add_birthday():
    """Ask data to user in prompt for adding a contact with his birthday"""
    name = input("Type contact's name: ")
    date = input("Type date of birth (YYYY-MM-DD): ")

    with open(DATA_FILE_PATH, "r") as file:
        data = json.load(file)
    with open(DATA_FILE_PATH, "w") as file:
        data["contacts"][name] = date
        json.dump(data, file)


def add_anniversary():
    """Ask data to user in prompt for adding an anniversary"""
    subject = input("Type anniversary's subject: ")
    date = input("Type date: ")

    with open(DATA_FILE_PATH, "r") as file:
        data = json.load(file)
    with open(DATA_FILE_PATH, "w") as file:
        data["anniversaries"][subject] = date
        json.dump(data, file)
