import json
import logging
import os


APARTMENT_FILE_PATH = os.path.relpath("apartment_data.json")


def save_list_of_apartments(apartments: list) -> None:
    """Save an apartment list into a json file."""

    with open(APARTMENT_FILE_PATH, mode="w") as afp:
        json.dump(apartments, afp)


def get_all_apartments() -> list[dict]:
    with open(APARTMENT_FILE_PATH, encoding="utf-8") as afp:
        return json.load(afp)


def suppress(exception: Exception, error_msg: str):
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
