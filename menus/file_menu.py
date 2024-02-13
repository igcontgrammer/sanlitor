from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


@dataclass(frozen=True)
class FileMenuActionsNames:
    NEW: Final[str] = "New"
    OPEN: Final[str] = "Open..."
    OPEN_FOLDER: Final[str] = "Open Folder..."
    RELOAD_FROM_DISK: Final[str] = "Reload from disk"
    SAVE: Final[str] = "Save"
    SAVE_AS: Final[str] = "Save As..."
    SAVE_COPY_AS: Final[str] = "Save a Copy As..."
    SAVE_ALL: Final[str] = "Save All"
    RENAME: Final[str] = "Rename..."
    CLOSE: Final[str] = "Close"
    CLOSE_ALL: Final[str] = "Close All"
    PRINT: Final[str] = "Print"
    EXIT: Final[str] = "Exit"


@dataclass(frozen=True)
class FileMenuActionsShortcuts:
    NEW: Final[str] = "Ctrl+N"
    OPEN: Final[str] = "Ctrl+O"
    OPEN_FOLDER: Final[str] = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: Final[str] = "Ctrl+R"
    SAVE: Final[str] = "Ctrl+S"
    SAVE_AS: Final[str] = "Ctrl+S"
    SAVE_ALL: Final[str] = "Ctrl+Shift+S"
    CLOSE: Final[str] = "Ctrl+W"
    CLOSE_ALL: Final[str] = "Ctrl+Shift+W"
    EXIT: Final[str] = "Alt+F4"


class FileMenu(QMenu):
    _MENU_NAME: Final[str] = "File"

    def __init__(self):
        super().__init__()
        self._file_menu = QMenu(self._MENU_NAME)
        self._call_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._file_menu

    def _call_menus(self) -> None:
        self._open_file_action()
        self._new_file_action()
        self._save_file_action()
        self._save_as_action()
        self._save_all_files_action()
        self._close_file_action()
        self._close_all_files_action()
        self._print_action()
        self._exit_action()

    def _open_file_action(self) -> None:
        open_file_action = QAction(FileMenuActionsNames.OPEN, self)
        ConfigAction().config_action(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuActionsShortcuts.OPEN,
            method=self._open_file,
        )
        self._file_menu.addAction(open_file_action)

    def _new_file_action(self) -> None:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        ConfigAction().config_action(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuActionsShortcuts.NEW,
            method=self._new_file,
        )
        self._file_menu.addAction(new_file_action)

    def _save_file_action(self) -> None:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        ConfigAction().config_action(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuActionsShortcuts.SAVE,
            method=self._save_file,
        )
        self._file_menu.addAction(save_file_action)

    def _save_as_action(self) -> None:
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        ConfigAction().config_action(
            action=save_as_action,
            status_tip="Save a file as...",
            shortcut=FileMenuActionsShortcuts.SAVE_AS,
            method=self._save_file,
        )
        self._file_menu.addAction(save_as_action)

    def _save_all_files_action(self) -> None:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        ConfigAction().config_action(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuActionsShortcuts.SAVE_ALL,
            method=self._save_all_files,
        )
        self._file_menu.addAction(save_all_files_action)

    def _close_file_action(self) -> None:
        close_file_action = QAction(FileMenuActionsNames.CLOSE, self)
        ConfigAction().config_action(
            action=close_file_action,
            status_tip="Close a file",
            shortcut=FileMenuActionsShortcuts.CLOSE,
            method=self._edit_file,
        )
        self._file_menu.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        ConfigAction().config_action(
            action=close_all_files_action,
            status_tip="Close all files",
            shortcut=FileMenuActionsShortcuts.CLOSE_ALL,
            method=self._edit_file,
        )
        self._file_menu.addAction(close_all_files_action)

    def _print_action(self) -> None:
        print_action = QAction(FileMenuActionsNames.PRINT, self)
        ConfigAction().config_action(
            action=print_action,
            status_tip="Print a file",
            shortcut="",
            method=self._print_file,
        )
        self._file_menu.addAction(print_action)

    def _exit_action(self) -> None:
        exit_action = QAction(FileMenuActionsNames.EXIT, self)
        ConfigAction().config_action(
            action=exit_action,
            status_tip="Exit the application",
            shortcut=FileMenuActionsShortcuts.EXIT,
            method=self._exit_application,
        )
        self._file_menu.addAction(exit_action)

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

    @Slot()
    def _print_file(self) -> None:
        print("Printing a file...")
        pass

    @Slot()
    def _exit_application(self) -> None:
        print("Exiting the application...")
        pass
