import datetime
import pathlib
import json
from typing import List

from notifypy import Notify
from main import (DATA_FILE_PATH, CONTACTS_PHOTOS_PATH)

CONGRATS_MESSAGE = "Say congrats!!"

def get_settings() -> dict:
    """
    Return a settings dictionary from data json file
    """
    with open(DATA_FILE_PATH, "r") as file:
        settings = json.load(file)["settings"]

    return settings


def get_birthdays_by_date(date: str) -> List:
    """Returns a list of contacts names whose birthdays are on a specific date

    Args:
        date (str): a date formatted in YYYY-MM-DD

    Returns:
        List: a list with contacts names
    """
    birthdays_list = []

    with open(DATA_FILE_PATH, "r") as file:
        contacts = json.load(file)["contacts"]

    for name, date_of_birth in contacts.items():
        if date_of_birth == date:
            birthdays_list.append(name)

    return birthdays_list

def get_anniversaries_by_date(date: str) -> List:
    """Returns a list of anniversaries on a specific date

    Args:
        date (str): a date formatted in YYYY-MM-DD

    Returns:
        List: a list with anniversaries
    """
    anniversaries_list = []

    with open(DATA_FILE_PATH, "r") as file:
        anniversaries = json.load(file)["anniversaries"]

    for subject, anniversary_date in anniversaries.items():
        anniversary_month_and_day = anniversary_date.split("-")[1:]
        date_month_and_day = date.split("-")[1:]
        if anniversary_month_and_day == date_month_and_day:
            anniversaries_list.append(subject)

    return anniversaries_list

def notify(*args, **kwargs):
    notification = Notify(*args, **kwargs)
    notification.send()


def get_birthdays_by_countdown_days(countdown_days: int) -> List:
    """Returns a list of names with n days remaining for their birthdays

    Args:
        countdown_days (int): days remaining for the birthday

    Returns:
        List: a list with contacts names
    """
    birthdays_list = []

    with open(DATA_FILE_PATH, "r") as file:
        contacts = json.load(file)["contacts"]

    today_date = datetime.date.today()

    for name, date_of_birth in contacts.items():

        date_str_list = date_of_birth.split("-")
        date_int_list = list(map(int, date_str_list))
        date = datetime.date(today_date.year, *date_int_list[1:])

        difference = date - today_date

        if difference.days == countdown_days:
            birthdays_list.append(name)

    return birthdays_list

def get_anniversaries_by_countdown_days(countdown_days: int) -> List:
    """Returns a list of anniversaries with n days remaining

    Args:
        countdown_days (int): days remaining for the anniversary

    Returns:
        List: a list with anniversaries
    """
    anniversaries_list = []

    with open(DATA_FILE_PATH, "r") as file:
        anniversaries = json.load(file)["anniversaries"]

    today_date = datetime.date.today()

    for subject, anniversary_date in anniversaries.items():

        date_str_list = anniversary_date.split("-")
        date_int_list = list(map(int, date_str_list))
        date = datetime.date(today_date.year, *date_int_list[1:])

        difference = date - today_date

        if difference.days == countdown_days:
            subject += f' No: {today_date.year - date_int_list[0]}'
            anniversaries_list.append(subject)

    return anniversaries_list


def check_birthdays():
    """
    Check for birthdays in data json file and notify according to settings
    """
    settings = get_settings()
    countdown_days = settings.get("countdown_days")
    photo = settings.get('photo')

    today_date = datetime.date.today()

    if countdown_days:
        birthdays = get_birthdays_by_countdown_days(countdown_days)
    else:
        birthdays = get_birthdays_by_date(str(today_date))

    if birthdays:
        for name in birthdays:
            title = f"Birthday of {name}"
            if countdown_days:
                message = (
                    f"{countdown_days} day{'s' if countdown_days>1 else ''} remaining"
                )
            else:
                message = CONGRATS_MESSAGE
            
            notification_options = dict(
                default_notification_application_name="Birthday Reminder",
                default_notification_title=title,
                default_notification_message=message,
            )

            if photo:
                default_notification_icon = f"{CONTACTS_PHOTOS_PATH}{name.lower()}.png"
                if pathlib.Path(default_notification_icon).exists():
                    notification_options.update({"default_notification_icon": default_notification_icon})            
            try:
                notify(**notification_options)
            except Exception:
                pass

def check_anniversaries():
    """
    Check for anniversaries in data json file and notify according to settings
    """
    settings = get_settings()
    countdown_days = settings.get("countdown_days")

    today_date = datetime.date.today()

    if countdown_days:
        anniversaries = get_anniversaries_by_countdown_days(countdown_days)
    else:
        anniversaries = get_anniversaries_by_date(str(today_date))
    
    if anniversaries:
        for subject in anniversaries:
            title = subject
            if countdown_days:
                message = (
                    f"{countdown_days} day{'s' if countdown_days>1 else ''} remaining"
                )
            else:
                message = CONGRATS_MESSAGE
            
            notification_options = dict(
                default_notification_application_name="Anniversary Reminder",
                default_notification_title=title,
                default_notification_message=message,
            )

            try:
                notify(**notification_options)
            except Exception:
                pass

if __name__ == "__main__":
    check_birthdays()
    check_anniversaries()