from typing import Final, List
from editor import Editor
from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import QCoreApplication as coreapp

_DEFAULT_TAB_NAME: Final[str] = "Untitled"


class TabManager(QTabWidget):

    def __init__(self):
        super().__init__()
        self._tab = QTabWidget()
        self._editor = Editor().editor
        self._loaded_files: List[str] = []

    # ************* getters *************

    @property
    def tab(self) -> QTabWidget:
        return self._tab

    def get_loaded_files(self) -> List[str]:
        return list(set(self._loaded_files))

    def get_current_tab_index(self) -> int:
        return self._tab.currentIndex()

    def get_tabs_count(self) -> int:
        return self._tab.count()

    # ************* setters *************

    def set_content_to_current_tab(self, content: str) -> None:
        self._tab.widget(self.get_current_tab_index()).setPlainText(content)

    # ************* others *************

    def move_to_tab(self, filename: str):
        for i in range(self._tab.count()):
            tab_name = self._tab.tabText(i)
            if tab_name == filename:
                self._tab.setCurrentIndex(i)
                break

    def add_to_loaded_files(self, filename: str) -> None:
        self._loaded_files.append(filename)

    def remove_from_loaded_files(self, filename: str) -> None:
        self._loaded_files.remove(filename)

    def build_default_tab(self) -> None:
        self._tab.addTab(self._editor, _DEFAULT_TAB_NAME)
        self._tab.setTabsClosable(True)
        self._tab.tabCloseRequested.connect(self.on_tab_close_requested)

    def add_new_tab(self, tab_name: str, content: str) -> None:
        new_index = self._tab.addTab(Editor().get_new_editor(), tab_name)
        self._tab.setCurrentIndex(new_index)
        self._tab.widget(new_index).setPlainText(content)
        self._tab.tabCloseRequested.connect(self.on_tab_close_requested)

    # TODO: trabajar en los estados de guardado
    def on_tab_close_requested(self, index: int) -> None:
        if self.get_tabs_count() > 1:
            self._tab.removeTab(index)
            return
        self._tab.setTabText(index, coreapp.translate("tab_manager", _DEFAULT_TAB_NAME))
        self._editor.clear()

    def change_current_tab_name(self, name: str) -> None:
        self._tab.setTabText(self.get_current_tab_index(), name)
