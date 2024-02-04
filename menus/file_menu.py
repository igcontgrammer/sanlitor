from typing import Final
from enum import Enum
from utils import Utils
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


class FileMenuActionsNames(Enum):
    NEW = "New"
    OPEN = "Open..."
    OPEN_FOLDER = "Open Folder..."
    RELOAD_FROM_DISK = "Reaload from disk"
    SAVE = "Save"
    SAVE_AS = "Save As..."
    SAVE_COPY_AS = "Save a Copy As..."
    SAVE_ALL = "Save All"
    RENAME = "Rename..."
    CLOSE = "Close"
    CLOSE_ALL = "Close All"
    PRINT = "Print"
    EXIT = "Exit"


class FileMenuActionsShortcuts(Enum):
    NEW = "Ctrl+N"
    OPEN = "Ctrl+O"
    OPEN_FOLDER = "Ctrl+Shift+O"
    RELOAD_FROM_DISK = "Ctrl+R"
    SAVE = "Ctrl+S"
    SAVE_AS = "Ctrl+S"
    SAVE_ALL = "Ctrl+Shift+S"
    CLOSE = "Ctrl+W"
    CLOSE_ALL = "Ctrl+Shift+W"
    EXIT = "Alt+F4"


class FileMenu(QMenu):
    _MENU_NAME: Final[str] = "File"

    def __init__(self):
        super().__init__()
        self._file_menu = QMenu(self._MENU_NAME)
        self._add_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._file_menu

    def _add_menus(self) -> None:
        self._file_menu.addAction(self._open_file_action())
        self._file_menu.addAction(self._new_file_action())
        self._file_menu.addAction(self._save_file_action())
        self._file_menu.addAction(self._save_all_files_action())
        pass

    # ************* actions *************

    def _open_file_action(self) -> QAction:
        open_file_action = QAction(FileMenuActionsNames.OPEN.value, self)
        Utils().config_action(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuActionsShortcuts.OPEN.value,
            method=self._open_file,
        )
        return open_file_action

    def _new_file_action(self) -> QAction:
        new_file_action = QAction(FileMenuActionsNames.NEW.value, self)
        Utils().config_action(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuActionsShortcuts.NEW.value,
            method=self._new_file,
        )
        return new_file_action

    def _save_file_action(self) -> QAction:
        save_file_action = QAction(FileMenuActionsNames.SAVE.value, self)
        Utils().config_action(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuActionsShortcuts.SAVE.value,
            method=self._save_file,
        )
        return save_file_action

    def _save_all_files_action(self) -> QAction:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL.value, self)
        Utils().config_action(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuActionsShortcuts.SAVE_ALL.value,
            method=self._save_all_files,
        )
        return save_all_files_action

    # ************* functions *************

    @Slot()
    def _open_file(self) -> None:
        print("Opening a file...")
        pass

    @Slot()
    def _new_file(self) -> None:
        print("Creating a new file...")
        pass

    @Slot()
    def _edit_file(self) -> None:
        print("Editing a file...")
        pass

    @Slot()
    def _save_file(self) -> None:
        print("Saving a file...")
        pass

    @Slot()
    def _save_all_files(self) -> None:
        print("Saving all files...")
        pass
