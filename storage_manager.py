import json
import os
from typing import Dict, List, Optional, Tuple, Union

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

    @property
    def saved_files(self) -> List[str]:
        return self._files_saved

    def is_registered(self, file_name: str) -> bool:
        return file_name in self._files_saved

    def update_last_tab_worked_index(self, index: int) -> None:
        try:
            with open(Paths.STORAGE, "w") as file:
                self._content["lastTabWorkedIndex"] = index
                json.dump(self._content, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            print(f"exception at update_last_tab_worked_index: {fe}")
            return
        except Exception as e:
            print(f"exception at update_last_tab_worked_index: {e}")
            return

    def add_new_opened_files(self, new_files: List[str], index: int) -> None:
        for new_file in new_files:
            self._files_worked.append(new_file)
        try:
            with open(Paths.STORAGE, "w") as file:
                self._content["filesWorkedOn"] = self._files_worked
                self._content["lastTabWorkedIndex"] = index
                json.dump(self._content, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            print(f"exception at add_new_opened_files: {fe}")
            return
        except Exception as e:
            print(f"exception at add_new_opened_files: {e}")
            return

    def delete_files(self, files: List[str]) -> None:
        for file in files:
            if file in self._files_worked:
                self._files_worked.remove(file)
            if os.path.exists(Paths.TEMP_FILES + file):
                os.remove(Paths.TEMP_FILES + file)
        try:
            with open(Paths.STORAGE, "w") as file:
                self._content["filesWorkedOn"] = self._files_worked
                json.dump(self._content, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            print(f"exception at delete_files: {fe}")
        except Exception as e:
            print(f"exception at delete_files: {e}")

    def get_last_files_worked(self) -> List[str]:
        """Get the last tabs that were opened by the user"""
        return self._files_worked

    def get_saved_files(self) -> List[str]:
        """Get the last tabs that were opened by the user"""
        return self._files_saved

    def get_content_from_file(self, path: str) -> Optional[str]:
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError as fe:
            print(f"exception at get_content_from_file: {fe}")
            return None
        except Exception as e:
            print(f"exception at get_content_from_file: {e}")
            return None

    def save_changes(
        self,
        *,
        file_name: Optional[str] = None,
        value: Optional[str] = None,
        path: Optional[str] = None,
        old_file_name: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        try:
            if path is not None and old_file_name is not None:
                if old_file_name in self._files_saved:
                    index_old_saved_file = self._files_saved.index(old_file_name)
                    self._files_saved[index_old_saved_file] = path
                else:
                    self._files_saved.append(path)
                if old_file_name in self._files_worked:
                    index_old_opened_files = self._files_worked.index(old_file_name)
                    self._files_worked[index_old_opened_files] = os.path.basename(path)
                else:
                    self._files_worked.append(os.path.basename(path))
                # TODO: el problema es, que cuando el usuario selecciona otra ubicacion, no se escribe el archivo en temp files
                os.rename(Paths.TEMP_FILES + old_file_name, path)
                with open(Paths.STORAGE, "w") as write_file:
                    self._content["savedFiles"] = self._files_saved
                    self._content["filesWorkedOn"] = self._files_worked
                    json.dump(self._content, write_file, indent=4)
                # index_old_opened_files = self._files_worked.index(old_file_name)
                # self._files_saved[index_old_saved_file] = path
                # self._files_saved[index_old_saved_file] = path
                # self._files_worked[index_old_opened_files] = os.path.basename(path)
                # os.rename(Paths.TEMP_FILES + old_file_name, path)
                # with open(Paths.STORAGE, "w") as write_file:
                #     self._content["savedFiles"] = self._files_saved
                #     self._content["filesWorkedOn"] = self._files_worked
                #     json.dump(self._content, write_file, indent=4)
                return True, None
            elif file_name is not None and value is not None:
                for file in self._files_saved:
                    if os.path.basename(file) == file_name:
                        with open(file, "w") as write_file:
                            write_file.write(value)
                            return True, None
            else:
                raise ValueError("filename and value or path must be provided")
        except ValueError as ve:
            print(f"exception at save_changes: {ve}")
            return False, str(ve)
        except (FileNotFoundError, json.JSONDecodeError) as fe:
            return False, str(fe)
        except Exception as e:
            return False, str(e)
