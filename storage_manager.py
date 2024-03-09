import json
import os
from typing import Final, Dict, List, Optional, Tuple, Union
from constants import FileNames
from paths import Paths

PATH_DEFAULT_FILE: Final[str] = Paths.TEMP_FILES + FileNames.DEFAULT


def get_content() -> Dict[str, Union[List[str], int]]:
    try:
        with open(Paths.STORAGE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    except Exception as e:
        print(e)
        return {}


class StorageManager:
    def __init__(self) -> None:
        self._content: Dict[str, Union[List[str], int]] = get_content()
        self._paths: List[str] = self._content.get("paths", [])  # type: ignore
        self._worked_files: List[str] = list(map(os.path.basename, self._paths))  # type: ignore
        self._last_tab_worked_index: int = self._content.get("lastTabWorked")  # type: ignore

    @property
    def paths(self) -> List[str]:
        return self._paths

    @property
    def worked_files(self) -> List[str]:
        return self._worked_files

    @property
    def last_tab_worked_index(self) -> int:
        return self._last_tab_worked_index

    def path_exists(self, file_name: str) -> bool:
        return any(file_name in path for path in self._paths)

    def save_from_file_name(
        self, file_name: str, content: str
    ) -> Tuple[bool, Optional[str]]:
        path = list(filter(lambda x: os.path.basename(x) == file_name, self._paths))[0]
        try:
            with open(path, "w") as file:
                file.write(content)
            return True, None
        except Exception as e:
            return False, str(e)

    def save_from_path(self, path: str, content: str) -> Tuple[bool, Optional[str]]:
        try:
            with open(path, "w") as file:
                file.write(content)
            return True, None
        except Exception as e:
            return False, str(e)

    def add_path(self, path: str) -> Tuple[bool, Optional[str]]:
        if path in self._paths:
            return False, "This path already exists"
        self._paths.append(path)
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["paths"] = self._paths
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return True, str(fe)
        except Exception as e:
            return False, f"An error occurred: {e}"

    def remove_path(self, path: str) -> Tuple[bool, Optional[str]]:
        if path not in self._paths:
            return False, f"The path {path} does not exist"
        try:
            return True, None
        except FileNotFoundError as fe:
            print(str(fe))
            return False, None
        except Exception as e:
            print(e)
            return False, ""

    def save_all(self, files: List[str]) -> Tuple[bool, Optional[str]]:
        return True, None

    def remove(self, file_name: str) -> Tuple[bool, Optional[str]]:
        exists = any(file_name in path for path in self._paths)
        if not exists:
            return False, "This path does not exists"
        for i in range(len(self._paths)):
            if file_name in self._paths[i]:
                del self._content["paths"][i]  # type: ignore
                break
        try:
            with open(Paths.STORAGE, "w") as storage:
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, str(e)

    def remove_all(self) -> Tuple[int, Optional[str]]:
        self._content["paths"] = []
        try:
            with open(Paths.STORAGE, "w") as storage:
                json.dump(self._content, storage, indent=4)
            return True, None
        except Exception as e:
            return False, str(e)
