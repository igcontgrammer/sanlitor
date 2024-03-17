import json
import os
from pathlib import Path
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


def save_from_path(path: Path, content: str) -> Tuple[bool, Optional[str]]:
    try:
        with open(path, "w") as file:
            file.write(content)
        return True, None
    except Exception as e:
        return False, str(e)


class StorageManager:
    def __init__(self) -> None:
        self._content: Dict[str, Union[List[str], int]] = get_content()
        self._paths = [Path(p) for p in self._content["paths"]]
        self._worked_files: List[str] = [p.name for p in self._paths if p.exists()]
        folder_selected = self._content["folderSelected"] or ""
        self._folder_selected = Path(folder_selected) if folder_selected else None
        self._last_tab_worked_index: int = self._content["lastTabWorked"]
        self._app_mode: int = self._content["appMode"]

    @property
    def paths(self) -> List[Path]:
        return self._paths

    @property
    def folder_selected(self) -> Optional[Path]:
        return self._folder_selected

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

    def file_exists(self, file_name: str) -> bool:
        return any(path.name == file_name for path in self._paths)

    def save_from_file_name(
            self, file_name: str, content: str
    ) -> Tuple[bool, Optional[str]]:
        path: Path = list(filter(lambda x: x.name == file_name, self._paths))[0]
        try:
            with open(path, "w") as file:
                file.write(content)
            return True, None
        except FileNotFoundError as fnf:
            return False, str(fnf)
        except Exception as e:
            return False, str(e)

    def get_path_from_file_name(self, file_name: str) -> Optional[Path]:
        for path in self._paths:
            if path.name == file_name:
                return path
        return None

    def add(self, path: str) -> Tuple[bool, Optional[str]]:
        if Path(path) in self._paths:
            return False, "This path already exists"
        self._paths.append(Path(path))
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["paths"] = [str(path) for path in self._paths]
                json.dump(self._content, storage, indent=4)
            return True, None
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, f"An error occurred: {e}"

    def add_folder(self, path: Path) -> Tuple[bool, Optional[str]]:
        try:
            with open(Paths.STORAGE, "w") as storage:
                self._content["folderSelected"] = str(path)  # type: ignore
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
        path: Path = list(filter(lambda x: x.name == old_file_name, self._paths))[0]
        new_path = path.with_name(new_name)
        try:
            os.rename(path, new_path)
            for i, p in enumerate(self._paths):
                if str(path) == str(p):
                    self._paths[i] = new_path
                    break
            self._content["paths"] = [str(path) for path in self._paths]
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
        exists = any(path.name == file_name for path in self._paths)
        if not exists:
            return False, "This path does not exists"
        for i, path in enumerate(self._paths):
            if path.name == file_name:
                del self._paths[i]
                break
        self._content["paths"] = [str(path) for path in self._paths]
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
