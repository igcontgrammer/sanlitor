from ._menus_constants import SearchMenuActionsNames, SearchMenuShortcuts
from . import QMenu, QAction, Slot, SectionsNames
from common.config_action import config


class SearchMenu(QMenu):

    def __init__(self):
        super().__init__()
        self._search_menu = QMenu(SectionsNames.SEARCH)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._search_menu

    def _create_actions(self) -> None:
        self._search_action()
        self._search_in_files_action()
        self._next_action()
        self._back_action()

    def _search_action(self) -> None:
        search_action = QAction(SearchMenuActionsNames.SEARCH, self)
        config(
            action=search_action,
            shortcut=SearchMenuShortcuts.SEARCH,
            status_tip="Search",
            method=self.search,
        )
        self._search_menu.addAction(search_action)

    def _search_in_files_action(self) -> None:
        search_in_files_action = QAction(SearchMenuActionsNames.SEARCH_IN_FILES, self)
        config(
            action=search_in_files_action,
            shortcut=SearchMenuShortcuts.SEARCH_IN_FILES,
            status_tip="Search in files",
            method=self.search_in_files,
        )
        self._search_menu.addAction(search_in_files_action)

    def _next_action(self) -> None:
        next_action = QAction(SearchMenuActionsNames.NEXT, self)
        config(
            action=next_action,
            shortcut=SearchMenuShortcuts.NEXT,
            status_tip="Search Next",
            method=self.search_next,
        )
        self._search_menu.addAction(next_action)

    def _back_action(self) -> None:
        back_action = QAction(SearchMenuActionsNames.BACK, self)
        config(
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
