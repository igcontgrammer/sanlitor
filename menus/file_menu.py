from dataclasses import dataclass
from typing import Final
from utils import Utils
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


@dataclass(frozen=True)
class FileMenuActionsNames:
    NEW: str = "New"
    OPEN: str = "Open..."
    OPEN_FOLDER: str = "Open Folder..."
    RELOAD_FROM_DISK: str = "Reload from disk"
    SAVE: str = "Save"
    SAVE_AS: str = "Save As..."
    SAVE_COPY_AS: str = "Save a Copy As..."
    SAVE_ALL: str = "Save All"
    RENAME: str = "Rename..."
    CLOSE: str = "Close"
    CLOSE_ALL: str = "Close All"
    PRINT: str = "Print"
    EXIT: str = "Exit"


@dataclass(frozen=True)
class FileMenuActionsShortcuts:
    NEW: str = "Ctrl+N"
    OPEN: str = "Ctrl+O"
    OPEN_FOLDER: str = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: str = "Ctrl+R"
    SAVE: str = "Ctrl+S"
    SAVE_AS: str = "Ctrl+S"
    SAVE_ALL: str = "Ctrl+Shift+S"
    CLOSE: str = "Ctrl+W"
    CLOSE_ALL: str = "Ctrl+Shift+W"
    EXIT: str = "Alt+F4"


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
        open_file_action = QAction(FileMenuActionsNames.OPEN, self)
        Utils().config_action(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuActionsShortcuts.OPEN,
            method=self._open_file,
        )
        return open_file_action

    def _new_file_action(self) -> QAction:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        Utils().config_action(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuActionsShortcuts.NEW,
            method=self._new_file,
        )
        return new_file_action

    def _save_file_action(self) -> QAction:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        Utils().config_action(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuActionsShortcuts.SAVE,
            method=self._save_file,
        )
        return save_file_action

    def _save_all_files_action(self) -> QAction:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        Utils().config_action(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuActionsShortcuts.SAVE_ALL,
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
