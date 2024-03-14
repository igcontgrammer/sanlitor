from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QTextDocument
from PySide6.QtWidgets import QInputDialog, QSizePolicy, QToolBar, QWidget

from common.config_action import config
from editor import Editor

from . import QAction, QMenu, SectionsNames, Slot
from ._components._toolbar import ToolBar
from ._menus_constants import SearchMenuActionsNames, SearchMenuShortcuts


class SearchMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        self.setTitle(SectionsNames.SEARCH)
        from home import Home

        self._home: Home = home
        self._editor: Editor = self._home.tab.widget(self._home.tab.currentIndex())
        self._current_index: int = 0
        self._number_of_ocurrences: int = 0
        self._value_to_search: Optional[str] = ""
        self._cursor: Optional[QTextCursor] = None
        self._toolbar: Optional[ToolBar] = None
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

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
            method=self._go_to_next,
        )
        self.addAction(next_action)

    def _back_action(self) -> None:
        back_action = QAction(SearchMenuActionsNames.BACK, self)
        config(
            action=back_action,
            shortcut=SearchMenuShortcuts.BACK,
            status_tip="Search Back",
            method=self._go_to_prev,
        )
        self.addAction(back_action)

    @Slot()
    def _search(self) -> None:
        value, ok = QInputDialog.getText(self._home, "Buscar", "Texto a buscar:")
        if not ok or len(value) == 0:
            return None
        self._value_to_search = value
        self._build_move_between_ocurrences()
        editor = self._home.tab.widget(self._home.tab.currentIndex())
        if not isinstance(editor, Editor):
            return
        self._editor = editor
        content = self._editor.toPlainText()
        self._number_of_ocurrences = content.count(value)
        if self._cursor is None:
            self._cursor = self._editor.textCursor()

    @Slot()
    def _go_to_next(self) -> None:
        if self._current_index + 1 > self._number_of_ocurrences:
            self._current_index = 0
            self._cursor.setPosition(0)
            self._editor.setTextCursor(self._cursor)
        else:
            self._current_index += 1
            self._editor.find(self._value_to_search)

    @Slot()
    def _go_to_prev(self) -> None:
        if self._current_index - 1 < 0:
            self._current_index = self._number_of_ocurrences
            self._cursor.movePosition(QTextCursor.End)
            self._editor.setTextCursor(self._cursor)
        else:
            self._current_index -= 1
            self._editor.find(self._value_to_search, QTextDocument.FindBackward)

    def _build_move_between_ocurrences(self) -> None:
        # creating actions
        prev = QAction("Prev", self._home)
        next = QAction("Next", self._home)
        close = QAction("x", self._home)
        prev.triggered.connect(self._go_to_prev)
        next.triggered.connect(self._go_to_next)
        close.triggered.connect(self._on_close_toolbar)
        actions = [prev, next, close]
        self._toolbar = ToolBar(self._home, actions, is_search_menu=True)
        self._toolbar.show()

    def _on_close_toolbar(self) -> None:
        self._value_to_search = None
        self._current_index = 0
        self._number_of_ocurrences = 0
        self._cursor.removeSelectedText()
        self._editor.setTextCursor(self._cursor)
        self._toolbar.close()

    def _search_in_files(self) -> None:
        print("Search in files...")
