import json
import os
from typing import Dict, List, Optional, Union

from paths import Paths


def _content() -> Dict[str, Union[List[str], int]]:
    with open(Paths.STORAGE, "r") as file:
        return json.load(file)


class StorageManager:
    def __init__(self) -> None:
        self._content = _content()
        self._files_worked: List[str] = self._content.get("filesWorkedOn")
        self._files_saved: List[str] = self._content.get("savedFiles")
        self._has_opened_tabs: bool = len(self._files_worked) > 0
        self._last_tab_worked_index: int = self._content.get("lastTabWorkedIndex")

    @property
    def opened_files(self) -> List[str]:
        return self._files_worked

    @property
    def has_opened_tabs(self) -> bool:
        return self._has_opened_tabs

    @property
    def last_tab_worked_index(self) -> int:
        return self._last_tab_worked_index

    def is_registered(self, file_name: str) -> bool:
        return file_name in self._files_saved

    def update_last_tab_worked_index(self, index: int) -> None:
        with open(Paths.STORAGE, "w") as file:
            self._content["lastTabWorkedIndex"] = index
            json.dump(self._content, file, indent=4)

    def add_new_opened_files(self, new_files: List[str], index: int) -> None:
        for new_file in new_files:
            self._files_worked.append(new_file)
        with open(Paths.STORAGE, "w") as file:
            self._content["filesWorkedOn"] = self._files_worked
            self._content["lastTabWorkedIndex"] = index
            json.dump(self._content, file, indent=4)

    def delete_files(self, files: List[str]) -> None:
        for file in files:
            # se elimina de los archivos trabajados, para impedir la creación de los tabs iniciales
            if file in self._files_worked:
                self._files_worked.remove(file)
            # se elimina de los archivos temporales, liberando así memoria según lo que vaya necesitando el usuario
            if os.path.exists(Paths.TEMP_FILES + file):
                os.remove(Paths.TEMP_FILES + file)
            print(f"absolut path: {os.path.abspath(file)}")
        try:
            with open(Paths.STORAGE, "w") as file:
                self._content["filesWorkedOn"] = self._files_worked
                json.dump(self._content, file, indent=4)
        except Exception as e:
            print(f"exception at delete_files: {e}")

    def get_last_files_worked(self) -> List[str]:
        """Get the last tabs that were opened by the user"""
        return self._files_worked

    def get_saved_files(self) -> List[str]:
        """Get the last tabs that were opened by the user"""
        return self._files_saved

    def save_changes(
        self,
        *,
        file_name: Optional[str] = None,
        value: Optional[str] = None,
        path: Optional[str] = None,
    ) -> bool:
        content: Dict[str, List[str]] = {}
        try:
            if path is not None:
                self._files_saved.append(path)
                content["savedFiles"] = self._files_saved
                with open(Paths.STORAGE, "w") as write_file:
                    json.dump(content, write_file, indent=4)
                    return True
            elif file_name is not None and value is not None:
                for file in self._files_saved:
                    if os.path.basename(file) == file_name:
                        with open(file, "w") as write_file:
                            write_file.write(value)
                            return True
            else:
                raise ValueError("filename and value or path must be provided")
        except ValueError as ve:
            print(f"exception at save_changes: {ve}")
            return False
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"exception at save_changes: {e}")
            return False
        except Exception as e:
            print(f"exception at save_changes: {e}")
            return False
