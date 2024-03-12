from common.config_action import config
from . import QAction, QMenu, SectionsNames, Slot
from PySide6.QtWidgets import QInputDialog, QPushButton, QToolBar
from PySide6.QtGui import QTextCursor
from ._menus_constants import SearchMenuActionsNames, SearchMenuShortcuts
from PySide6.QtCore import QSize

"""
Features:
    - Search
    - Search in files
    - Search Next
    - Search Back
"""


class SearchMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        from home import Home

        self._home: Home = home
        self.setTitle(SectionsNames.SEARCH)
        self._create_actions()
        self._build_toolbar()

    @property
    def menu(self) -> QMenu:
        return self

    def _build_toolbar(self) -> None:
        toolbar = QToolBar(self._home)
        next_action = QAction("Next", toolbar)
        prev_action = QAction("Prev", toolbar)
        toolbar.addAction(next_action)
        toolbar.addAction(prev_action)
        self._home.addToolBar(toolbar)

    def _show_toolbar(self) -> None:
        self._home.toolbar.show()

    def _hide_toolbar(self) -> None:
        self._home.toolbar.hide()

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
            method=self._search,
        )
        self.addAction(search_action)

    def _search_in_files_action(self) -> None:
        search_in_files_action = QAction(SearchMenuActionsNames.SEARCH_IN_FILES, self)
        config(
            action=search_in_files_action,
            shortcut=SearchMenuShortcuts.SEARCH_IN_FILES,
            status_tip="Search in files",
            method=self._search_in_files,
        )
        self.addAction(search_in_files_action)

    def _next_action(self) -> None:
        next_action = QAction(SearchMenuActionsNames.NEXT, self)
        config(
            action=next_action,
            shortcut=SearchMenuShortcuts.NEXT,
            status_tip="Search Next",
            method=self._search_next,
        )
        self.addAction(next_action)

    def _back_action(self) -> None:
        back_action = QAction(SearchMenuActionsNames.BACK, self)
        config(
            action=back_action,
            shortcut=SearchMenuShortcuts.BACK,
            status_tip="Search Back",
            method=self._search_back,
        )
        self.addAction(back_action)

    @Slot()
    def _search(self) -> None:
        value, ok = QInputDialog.getText(self._home, "Buscar", "Texto a buscar:")
        if not ok or len(value) == 0:
            return None
        self._show_toolbar()
        # construir el toolbar con sus botones de next y prev
        # 1) obtener el numero de ocurrencias
        editor = self._home.tab.editor
        content = editor.toPlainText()
        number_of_ocurrences = content.count(value)
        # 2) buscar la primera ocurrencia
        cursor = editor.textCursor()
        ok = editor.find(value)
        print(f"ok: {ok}")
        print(f"anchor: {cursor.anchor()}")
        print(f"position: {cursor.position()}")
        print(f"selectionStart: {cursor.selectionStart()}")

    def _search_in_files(self) -> None:
        print("Search in files...")

    @Slot()
    def _search_next(self) -> None:
        print("Search Next...")

    @Slot()
    def _search_back(self) -> None:
        print("Search Back...")

    @Slot()
    def _go_to_next(self) -> None:
        pass

    @Slot()
    def _go_to_prev(self) -> None:
        pass
