import json
import os
from typing import List


_DIR = os.path.dirname(__file__)
_STORAGE_ROUTE = _DIR + "/storage/files.json"

"""
- File Exists
- File is Saved
- Save
- Save All
"""


def is_registered(filename: str) -> bool:
    try:
        with open(_STORAGE_ROUTE, "r") as file:
            content = json.load(file)
            paths = content["registeredFiles"]
            for path in paths:
                if os.path.basename(path) == filename:
                    return True
            return False
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False


def has_opened_tabs() -> bool:
    with open(_STORAGE_ROUTE, "r") as file:
        content = json.load(file)
        opened_files = content["openedFiles"]
        return len(opened_files) > 0


def get_opened_tabs() -> List[str]:
    with open(_STORAGE_ROUTE, "r") as file:
        content = json.load(file)
        opened_files = content["openedFiles"]
        return opened_files


def save_from_path(path: str) -> bool:
    try:
        with open(_STORAGE_ROUTE, "r") as file:
            content = json.load(file)
            saved_files = content["registeredFiles"]
            saved_files.append(path)
            content["registered_files"] = saved_files
            with open(_STORAGE_ROUTE, "w") as file:
                json.dump(content, file, indent=4)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def save_opened_file(filename: str) -> None:
    opened_files: List[str]
    try:
        with open(_STORAGE_ROUTE, "r") as file:
            content = json.load(file)
            opened_files = content["openedFiles"]
            with open(_STORAGE_ROUTE, "w") as file:
                opened_files.append(filename)
                content["openedFiles"] = opened_files
                json.dump(content, file, indent=4)
    except Exception as ex:
        print(f"exception: {ex}")


def save_from_already_exists(filename: str, lala: str) -> bool:
    try:
        with open(_STORAGE_ROUTE, "r") as file:
            content = json.load(file)
            paths = content["registeredFiles"]
            for path in paths:
                if os.path.basename(path) == filename:
                    with open(path, "w") as file:
                        file.write(lala)
                        return True
        return False
    except Exception as e:
        print(f"error: {e}")
        return False
