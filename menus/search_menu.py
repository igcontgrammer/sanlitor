from typing import Final
from enum import Enum
from utils import Utils
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


class SearchMenuActionsNames(Enum):
    SEARCH = "Search"
    SEARCH_IN_FILES = "Search in files"
    NEXT = "Search Next"
    BACK = "Search Back"


class SearchMenuShortcuts(Enum):
    SEARCH = "Ctrl+F"
    SEARCH_IN_FILES = "Ctrl+Shift+F"
    NEXT = "F3"
    BACK = "Shift+F3"


class SearchMenu(QMenu):
    _MENU_NAME: Final[str] = "Search"

    def __init__(self):
        super().__init__()
        self._search_menu = QMenu(self._MENU_NAME)
        self._add_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._search_menu

    def _add_menus(self) -> None:
        self._search_menu.addAction(self._search_action())
        # self._search_menu.addAction(self._search_in_files_action())
        # self._search_menu.addAction(self._next_action())
        # self._search_menu.addAction(self._back_action())

    # ************* actions *************

    def _search_action(self) -> QAction:
        search_action = QAction(SearchMenuActionsNames.SEARCH.value, self)
        Utils().config_action(
            action=search_action,
            shortcut=SearchMenuShortcuts.SEARCH.value,
            status_tip="Search",
            method=self.search,
        )
        return search_action

    # ************* slots *************

    @Slot()
    def search(self) -> None:
        print("Search...")
