from typing import Final
from editor import Editor
from PySide6.QtWidgets import QTabWidget


class Tab(QTabWidget):
    _DEFAULT_TAB_NAME: Final[str] = "Untitled"
    _DEFAULT_TABS_COUNT: Final[int] = 1

    def __init__(self):
        super().__init__()
        self._tab = QTabWidget()
        self._editor = Editor().get_editor
        self.__configurate_default_tab()

    def get_tab(self) -> QTabWidget:
        return self._tab

    def get_tabs_count(self) -> int:
        return self._tab.count()

    def has_tabs(self) -> bool:
        return self._tab.count() > 0

    def is_default(self) -> bool:
        return self._tab.count() == self._DEFAULT_TABS_COUNT

    def change_tab_name(self, index: int, new_name: str) -> None:
        self._tab.setTabText(index, new_name)

    def add_new_tab(self, tab_name: str) -> None:
        self._tab.addTab(self, tab_name)

    def set_content(self, content: str) -> None:
        self._editor.setPlainText(content)

    def __configurate_default_tab(self) -> None:
        self._tab.addTab(self._editor, self._DEFAULT_TAB_NAME)
        self._tab.setTabsClosable(True)
        self._tab.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index: int) -> None:
        if self.is_default():
            self._editor.clear()
            self.change_tab_name(0, self._DEFAULT_TAB_NAME)
            return
        self._tab.removeTab(index)
