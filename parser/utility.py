import json


def save_list_of_apartments(apartments: list, file_path: str) -> None:
    """Save an apartment list into a json file."""

    with open(file_path, mode="a") as json_file:
        json_file.write(json.dumps(apartments, indent=4))


