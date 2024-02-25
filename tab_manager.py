from typing import Final, List
from editor import Editor
from messages import Messages, MessageTypes
from constants import TabActions
from PySide6.QtWidgets import QTabWidget, QTextEdit
from PySide6.QtCore import QCoreApplication as CoreApp, Slot
from PySide6.QtGui import QIcon

_DEFAULT_TAB_NAME: Final[str] = "Untitled"


class TabManager(QTabWidget):

    def __init__(self):
        super().__init__()
        self._tabs = QTabWidget()
        self._editor_manager = Editor()
        self._loaded_files: List[str] = []

    # ************* getters *************

    @property
    def tab(self) -> QTabWidget:
        return self._tabs

    @property
    def editor_manager(self) -> Editor:
        return self._editor_manager

    @property
    def editor_has_changes(self) -> bool:
        return self._editor_manager.has_changes

    @property
    def loaded_files(self) -> List[str]:
        return list(set(self._loaded_files))

    @property
    def current_index(self) -> int:
        return self._tabs.currentIndex()

    @property
    def tabs_count(self) -> int:
        return self._tabs.count()

    @property
    def is_default(self) -> bool:
        return self.tabs_count == 1

    def file_was_opened(self, filename: str) -> bool:
        return filename in self.loaded_files

    # ************* SETTERS *************

    def add_content_to_current_tab(self, content: str) -> None:
        self._tabs.widget(self.current_index).setPlainText(content)

    def set_editor_has_changes(self, value: bool) -> None:
        self._editor_manager.has_changes = value

    def set_is_open_mode(self, value: bool) -> None:
        self._editor_manager.is_open_mode = value

    def move(self, filename: str):
        for i in range(self.tabs_count):
            tab_name = self._tabs.tabText(i)
            if tab_name == filename:
                self._tabs.setCurrentIndex(i)
                break

    def add_to_loaded_files(self, filename: str) -> None:
        self._loaded_files.append(filename)

    def remove_from_loaded_files(self, filename: str) -> None:
        self._loaded_files.remove(filename)

    def build_default_tab(self) -> None:
        self._tabs.addTab(self._editor_manager, _DEFAULT_TAB_NAME)
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self.on_close)

    # TODO: add logic to recognize changes when add new tab
    def add_new_tab(self, name: str, content: str) -> None:
        new_editor_manager = Editor()
        new_editor_manager.has_changes = False
        new_editor_manager.setPlainText(content)
        new_index = self._tabs.addTab(new_editor_manager, name)
        self._tabs.setCurrentIndex(new_index)

    # TODO: create the on save state
    # TODO: falta que al cerrar el tab, se elimine el contenido
    def on_close(self, index: int) -> None:
        if self.editor_has_changes:
            option = self.has_changes_selected_option()
            if option != TabActions.CLOSE:
                return
            if self.is_default:
                self._tabs.setTabIcon(index, QIcon())
                self._tabs.setTabText(index, _DEFAULT_TAB_NAME)
            else:
                self._tabs.removeTab(index)
            return
        filename = self._tabs.tabText(index)
        if filename in self._loaded_files:
            self._loaded_files.remove(filename)
        if self.tabs_count > 1:
            self._tabs.removeTab(index)
            return
        self._tabs.setTabText(
            index, CoreApp.translate("tab_manager", _DEFAULT_TAB_NAME)
        )

    def has_changes_selected_option(self) -> int:
        msg = Messages(
            parent=self,
            content="Hay cambios presentes ¿desea cerrar de todas formas?",
            first_button_title="Cerrar",
            type=MessageTypes.WARNING,
        )
        return msg.run()

    def change_tab_name(self, name: str) -> None:
        self._tabs.setTabText(self.current_index, name)
