import json
import os
from typing import Dict, Final, List, Optional, Tuple, Union

from constants import VALID_MODES, FileNames
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


def save_from_path(path: str, content: str) -> Tuple[bool, Optional[str]]:
    try:
        with open(path, "w") as file:
            file.write(content)
        return True, None
    except Exception as e:
        return False, str(e)


class StorageManager:
    def __init__(self) -> None:
        self._content: Dict[str, Union[List[str], int]] = get_content()
        self._paths: List[str] = self._content.get("paths", [])  # type: ignore
        self._worked_files: List[str] = list(map(os.path.basename, self._paths))  # type: ignore
        # get the path of the last folder selected
        self._folder_selected = self._content.get("folderSelected") or None  # type: ignore
        self._last_tab_worked_index: int = self._content.get("lastTabWorked")  # type: ignore
        self._app_mode: int = self._content.get("appMode")  # type: ignore

    @property
    def paths(self) -> List[str]:
        return self._paths

    @property
    def worked_files(self) -> List[str]:
        return self._worked_files

    @property
    def app_mode(self) -> int:
        return self._app_mode

    @app_mode.setter
    def app_mode(self, value: int) -> None:
        self._app_mode = value

    @property
    def last_tab_worked_index(self) -> int:
        return self._last_tab_worked_index

    @property
    def folder_selected(self) -> Optional[str]:
        return self._folder_selected  # type: ignore

    def path_exists(self, file_name: str) -> bool:
        return any(file_name in path for path in self._paths)

    def file_exists(self, file_name: str) -> bool:
        return file_name in self._worked_files

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

    def add(self, path: str) -> Tuple[bool, Optional[str]]:
        if path in self._paths:
            return False, "This path already exists"
        self._paths.append(path)
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["paths"] = self._paths
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, f"An error occurred: {e}"

    def add_folder(self, path: str) -> Tuple[bool, Optional[str]]:
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["folderSelected"] = path  # type: ignore
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, f"An error occurred: {e}"

    def update_mode(self, mode: int) -> Tuple[bool, Optional[str]]:
        if mode not in VALID_MODES:
            return False, "Invalid app mode"
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["appMode"] = mode
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, str(e)

    def rename(self, old_file_name: str, new_name: str) -> Tuple[bool, Optional[str]]:
        path = list(
            filter(lambda x: os.path.basename(x) == old_file_name, self._paths)
        )[0]
        new_path = path.replace(old_file_name, new_name)
        try:
            os.rename(path, new_path)
            for i, p in enumerate(self._paths):
                if path == p:
                    self._paths[i] = new_path
                    break
            self._content["paths"] = self._paths
            with open(Paths.STORAGE, "w") as storage:
                json.dump(self._content, storage, indent=4)
            return True, None
        except FileNotFoundError as fnf:
            print(fnf)
            return False, str(fnf)
        except Exception as e:
            print(e)
            return False, str(e)

    def remove(self, file_name: str) -> Tuple[bool, Optional[str]]:
        exists = any(file_name in path for path in self._paths)
        if not exists:
            return False, "This path does not exists"
        for i, path in enumerate(self._paths):
            if file_name in path:
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
