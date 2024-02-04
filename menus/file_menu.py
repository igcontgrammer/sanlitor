from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui
from typing import Final
from enum import Enum
from utils import Utils


class FileMenuActionsNames(Enum):
    OPEN = "Open"
    NEW = "New"
    EDIT = "Edit"
    SAVE = "Save"
    SAVE_ALL = "Save all"
    RENAME = "Rename"
    CLOSE_CURRENT_FILE = "Close Current File"
    CLOSE_ALL_FILES = "Close all files"
    CLOSE_ALL_LEFT_FILE = "Close all left files"
    CLOSE_ALL_RIGHT_FILE = "Close all right files"
    PRINT = "Print"
    RESTORE_LAST_CLOSED_FILE = "Restore last closed file"
    OPEN_ALL_RECENT_FILES = "Open all recent files"
    EXIT = "Exit"


class FileMenuActionsShortcuts(Enum):
    OPEN = "Ctrl+O"
    NEW = "Ctrl+N"
    EDIT = "Ctrl+E"
    SAVE = "Ctrl+S"
    SAVE_ALL = "Ctrl+Shift+S"
    RENAME = "Ctrl+R"
    CLOSE_CURRENT_FILE = "Ctrl+W"
    CLOSE_ALL_FILES = "Ctrl+Shift+W"


class FileMenu(qwt.QMenu):
    _MENU_NAME: Final[str] = "File"

    def __init__(self) -> None:
        super().__init__()
        self._file_menu = qwt.QMenu(self._MENU_NAME)
        self.add_menus()
        pass

    @property
    def get_menu(self) -> qwt.QMenu:
        return self._file_menu

    def add_menus(self) -> None:
        self._file_menu.addAction(self.open_file_action())
        self._file_menu.addAction(self.new_file_action())
        self._file_menu.addAction(self.edit_file_action())
        self._file_menu.addAction(self.save_file_action())
        self._file_menu.addAction(self.save_all_files_action())
        pass

    # ************* actions *************

    def open_file_action(self) -> gui.QAction:
        open_file_action = gui.QAction(FileMenuActionsNames.OPEN.value, self)
        Utils().config_action(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuActionsShortcuts.OPEN.value,
            method=self.open_file,
        )
        return open_file_action

    def new_file_action(self) -> gui.QAction:
        new_file_action = gui.QAction(FileMenuActionsNames.NEW.value, self)
        Utils().config_action(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuActionsShortcuts.NEW.value,
            method=self.new_file,
        )
        return new_file_action

    def edit_file_action(self) -> gui.QAction:
        edit_file_action = gui.QAction(FileMenuActionsNames.EDIT.value, self)
        Utils().config_action(
            action=edit_file_action,
            status_tip="Edit a file",
            shortcut=FileMenuActionsShortcuts.EDIT.value,
            method=self.edit_file,
        )
        return edit_file_action

    def save_file_action(self) -> gui.QAction:
        save_file_action = gui.QAction(FileMenuActionsNames.SAVE.value, self)
        Utils().config_action(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuActionsShortcuts.SAVE.value,
            method=self.save_file,
        )
        return save_file_action

    def save_all_files_action(self) -> gui.QAction:
        save_all_files_action = gui.QAction(FileMenuActionsNames.SAVE_ALL.value, self)
        Utils().config_action(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuActionsShortcuts.SAVE_ALL.value,
            method=self.save_all_files,
        )
        return save_all_files_action

    # ************* functions *************

    @qtc.Slot()
    def open_file(self) -> None:
        print("Opening a file...")
        pass

    @qtc.Slot()
    def new_file(self) -> None:
        print("Creating a new file...")
        pass

    @qtc.Slot()
    def edit_file(self) -> None:
        print("Editing a file...")
        pass

    @qtc.Slot()
    def save_file(self) -> None:
        print("Saving a file...")
        pass

    @qtc.Slot()
    def save_all_files(self) -> None:
        print("Saving all files...")
        pass
