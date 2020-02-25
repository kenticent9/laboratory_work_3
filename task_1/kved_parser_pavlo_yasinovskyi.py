"""Read a json file, gets desired info by a given class code and writes it
to a new json file."""
import json


def read_data(file_name: str) -> dict:
    """Returns data read from a json file."""
    with open(file_name, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)

    return data


def get_info(data: dict, class_code: str) -> tuple:
    """Returns desired info by a given class code."""
    info = None
    for section in data["sections"][0]:
        for division in section["divisions"]:
            for group in division["groups"]:
                for my_class in group["classes"]:
                    if my_class["classCode"] == class_code:
                        info = (my_class["className"],
                                group["groupName"], len(group["classes"]),
                                division["divisionName"],
                                len(division["groups"]),
                                section["sectionName"],
                                len(section["divisions"]))

    return info


def format_data(unformatted_data: tuple) -> dict:
    """Raw data to json."""
    return {
        "name": unformatted_data[0],
        "type": "class",
        "parent": {
            "name": unformatted_data[1],
            "type": "group",
            "num_children": unformatted_data[2],
            "parent": {
                "name": unformatted_data[3],
                "type": "division",
                "num_children": unformatted_data[4],
                "parent": {
                    "name": unformatted_data[5],
                    "type": "section",
                    "num_children": unformatted_data[6]
                }
            }
        }
    }


def write_data(data: dict, file_name: str) -> None:
    """Writes formatted data to a new json file."""
    with open(file_name, "w+", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
        # ensure_ascii=False so cyrillic characters are displayed properly


if __name__ == "__main__":
    READ_FILE = "kved.json"
    WRITE_FILE = "kved_results.json"
    DATA = read_data(READ_FILE)
    DESIRED_INFO = get_info(DATA, input("Enter a desired class code: "))
    try:
        FORMATTED_DATA = format_data(DESIRED_INFO)
        write_data(FORMATTED_DATA, WRITE_FILE)
        print("Your file is ready.")
    except TypeError:
        print("Class with such code does not exist.")
