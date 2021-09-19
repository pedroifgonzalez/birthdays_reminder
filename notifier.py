import datetime
import json
from typing import List

from notifypy import Notify
from main import DATA_FILE_PATH


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


def check_birthdays():
    """
    Check for birthdays in data json file and notify according to settings
    """
    settings = get_settings()
    countdown_days = settings.get("countdown_days")

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
                message = "Say congrats"

            notify(
                default_notification_application_name="Birthday Reminder",
                default_notification_title=title,
                default_notification_message=message,
            )


if __name__ == "__main__":
    check_birthdays()