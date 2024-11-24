import json
import logging
import os
import yaml
from parser.apartment import Apartment


FILE_PATH_APARTMENT = os.path.relpath("apartment_data.json")
FILE_PATH_CONFIG = os.path.relpath("config.yaml")


def clear_list_of_apartments_before_execute():
    with open(FILE_PATH_APARTMENT, mode="w") as afp:
        afp.write("[]")


def save_list_of_apartments(apartments: list) -> None:
    """Save an apartment list into a JSON file by appending to an existing list."""

    if os.path.exists(FILE_PATH_APARTMENT):
        with open(FILE_PATH_APARTMENT) as afp:
            try:
                existing_data = json.load(afp)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(apartments)

    with open(FILE_PATH_APARTMENT, mode="w") as afp:
        json.dump(existing_data, afp)


def get_all_apartments() -> list[Apartment]:
    with open(FILE_PATH_APARTMENT) as afp:
        return json.load(afp)


def suppress(exception: tuple[Exception], error_msg: str):
    """A decorator to catch exceptions, log a message, and return None."""

    def decorator(func):

        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                logging.error(f"{error_msg}: {e}")
                return None

        return new_func

    return decorator


def load_config():
    with open(FILE_PATH_CONFIG) as config_file:
        return yaml.safe_load(config_file)
