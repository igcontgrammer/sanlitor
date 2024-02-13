from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


@dataclass(frozen=True)
class SearchMenuActionsNames:
    SEARCH: Final[str] = "Search"
    SEARCH_IN_FILES: Final[str] = "Search in files"
    NEXT: Final[str] = "Search Next"
    BACK: Final[str] = "Search Back"


@dataclass(frozen=True)
class SearchMenuShortcuts:
    SEARCH: Final[str] = "Ctrl+F"
    SEARCH_IN_FILES: Final[str] = "Ctrl+Shift+F"
    NEXT: Final[str] = "F3"
    BACK: Final[str] = "Shift+F3"


class SearchMenu(QMenu):
    _MENU_NAME: Final[str] = "Search"

    def __init__(self):
        super().__init__()
        self._search_menu = QMenu(self._MENU_NAME)
        self._call_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._search_menu

    def _call_menus(self) -> None:
        self._search_action()
        self._search_in_files_action()
        self._next_action()
        self._back_action()

    def _search_action(self) -> None:
        search_action = QAction(SearchMenuActionsNames.SEARCH, self)
        ConfigAction().config_action(
            action=search_action,
            shortcut=SearchMenuShortcuts.SEARCH,
            status_tip="Search",
            method=self.search,
        )
        self._search_menu.addAction(search_action)

    def _search_in_files_action(self) -> None:
        search_in_files_action = QAction(SearchMenuActionsNames.SEARCH_IN_FILES, self)
        ConfigAction().config_action(
            action=search_in_files_action,
            shortcut=SearchMenuShortcuts.SEARCH_IN_FILES,
            status_tip="Search in files",
            method=self.search_in_files,
        )
        self._search_menu.addAction(search_in_files_action)

    def _next_action(self) -> None:
        next_action = QAction(SearchMenuActionsNames.NEXT, self)
        ConfigAction().config_action(
            action=next_action,
            shortcut=SearchMenuShortcuts.NEXT,
            status_tip="Search Next",
            method=self.search_next,
        )
        self._search_menu.addAction(next_action)

    def _back_action(self) -> None:
        back_action = QAction(SearchMenuActionsNames.BACK, self)
        ConfigAction().config_action(
            action=back_action,
            shortcut=SearchMenuShortcuts.BACK,
            status_tip="Search Back",
            method=self.search_back,
        )
        self._search_menu.addAction(back_action)

    @Slot()
    def search(self) -> None:
        print("Search...")

    @Slot()
    def search_in_files(self) -> None:
        print("Search in files...")

    @Slot()
    def search_next(self) -> None:
        print("Search Next...")

    @Slot()
    def search_back(self) -> None:
        print("Search Back...")
