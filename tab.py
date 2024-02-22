from typing import Final, List
from editor import Editor
from PySide6.QtWidgets import QTabWidget
from functools import partial

_DEFAULT_TAB_NAME: Final[str] = "Untitled"


class TabManager(QTabWidget):

    def __init__(self):
        super().__init__()
        self._tab = QTabWidget()
        self._editor = Editor().get_editor

    # ************* getters *************

    def get_tab(self) -> QTabWidget:
        return self._tab

    def get_current_tab_index(self) -> int:
        return self._tab.currentIndex()

    def _get_tabs_names(self) -> List[str]:
        tabs_names = []
        for index in range(self._tab.count()):
            tabs_names.append(self._tab.tabText(index))
        return tabs_names

    def get_tabs_count(self) -> int:
        return self._tab.count()

    # ************* setters *************

    def set_content_to_current_tab(self, content: str) -> None:
        self._tab.widget(self.get_current_tab_index()).setPlainText(content)

    # ************* others *************

    def build_default_tab(self) -> None:
        self._tab.addTab(self._editor, _DEFAULT_TAB_NAME)
        self._tab.setTabsClosable(True)
        self._tab.tabCloseRequested.connect(self.on_tab_close_requested)

    # TODO: trabajar en los estados de guardado
    def on_tab_close_requested(self, index: int) -> None:
        if self.get_tabs_count() > 1:
            self._tab.removeTab(index)
            return
        self._tab.setTabText(index, _DEFAULT_TAB_NAME)
        self._editor.clear()

    def add_new_tab(self, tab_name: str, content: str) -> None:
        new_index = self._tab.addTab(Editor().get_new_editor(), tab_name)
        self._tab.setCurrentIndex(new_index)
        self._tab.widget(new_index).setPlainText(content)
        self._tab.tabCloseRequested.connect(self.on_tab_close_requested)

    def tab_name_already_exists(self, tab_name: str) -> bool:
        return tab_name in self._get_tabs_names()

    def change_current_tab_name(self, name: str) -> None:
        self._tab.setTabText(self.get_current_tab_index(), name)

    def close_tab(self, index: int) -> None:
        self._tab.removeTab(index)
