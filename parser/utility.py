import json
import logging


def save_list_of_apartments(apartments: list, file_path: str) -> None:
    """Save an apartment list into a json file."""

    with open(file_path, mode="a") as json_file:
        json_file.write(json.dumps(apartments, indent=4))


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


