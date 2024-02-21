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

    def build_default_tab(self) -> None:
        self._tab.addTab(self._editor, self._DEFAULT_TAB_NAME)
        self._tab.tabCloseRequested.connect(self._tab.removeTab)
        self._tab.setTabsClosable(False)

    def get_tab_name(self) -> str:
        return self._tab.tabText(self.get_current_tab_index())

    def get_tabs_count(self) -> int:
        return self._tab.count()

    def has_tabs(self) -> bool:
        return self._tab.count() > 0

    def is_default(self) -> bool:
        return self._tab.count() == self._DEFAULT_TABS_COUNT

    def change_tab_name(self, index: int, new_name: str) -> None:
        self._tab.setTabText(index, new_name)

    def add_new_tab(self, name: str) -> None:
        self._tab.addTab(self._editor, name)

    def set_content(self, content: str) -> None:
        self._editor.setPlainText(content)

    def get_current_tab_index(self) -> int:
        return self._tab.currentIndex()

    def set_current_tab(self, index: int) -> None:
        self._tab.setCurrentIndex(index)

    def __configurate_default_tab(self) -> None:
        self._tab.setTabsClosable(True)
        self._tab.tabCloseRequested.connect(self.close_tab(index=1))

    def close_tab(self, index: int) -> None:
        print("Closing...")
        self._tab.removeTab(index)
