from typing import Final, List

from PySide6.QtCore import QCoreApplication as CoreApp
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTabWidget

from constants import TabActions
from editor import Editor
from messages import Messages, MessageTypes

_DEFAULT_TAB_NAME: Final[str] = "Untitled"


class Tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self._editor = Editor()
        self._loaded_files: List[str] = []

    @property
    def editor_manager(self) -> Editor:
        return self._editor

    @property
    def editor_has_changes(self) -> bool:
        return self._editor.has_changes

    @property
    def loaded_files(self) -> List[str]:
        return list(set(self._loaded_files))

    @property
    def current_index(self) -> int:
        return self.currentIndex()

    @property
    def tabs_count(self) -> int:
        return self.count()

    @property
    def is_default(self) -> bool:
        return self.tabs_count == 1

    def file_was_opened(self, filename: str) -> bool:
        return filename in self.loaded_files

    def add_content_to_current_tab(self, content: str) -> None:
        editor = self.widget(self.current_index)
        if not isinstance(editor, Editor):
            raise TypeError("editor is not an Editor object")
        editor.setPlainText(content)

    def set_editor_has_changes(self, value: bool) -> None:
        self._editor.has_changes = value

    def set_is_open_mode(self, value: bool) -> None:
        self._editor.is_open_mode = value

    def move(self, filename: str):
        for i in range(self.tabs_count):
            tab_name = self.tabText(i)
            if tab_name == filename:
                self.setCurrentIndex(i)
                break

    def add_to_loaded_files(self, filename: str) -> None:
        self._loaded_files.append(filename)

    def remove_from_loaded_files(self, filename: str) -> None:
        self._loaded_files.remove(filename)

    def build_default_tab(self) -> None:
        self.addTab(self._editor, _DEFAULT_TAB_NAME)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_close)

    def add_new_tab(self, name: str, content: str) -> None:
        new_editor = Editor()
        new_editor.setPlainText(content)
        new_editor.has_changes = False
        new_index = self.addTab(new_editor, name)
        self.setCurrentIndex(new_index)

    # TODO: create the on save state
    def on_close(self, index: int) -> None:
        child_editor = self.widget(index)
        if not isinstance(child_editor, Editor):
            raise TypeError("editor is not an Editor object")
        if child_editor.has_changes:
            option = self.has_changes_selected_option()
            if option != TabActions.CLOSE:
                return
            if self.is_default:
                self.setTabIcon(index, QIcon())
                self.setTabText(index, _DEFAULT_TAB_NAME)
                child_editor.clear()
            else:
                self.removeTab(index)
            return
        filename = self.tabText(index)
        if filename in self._loaded_files:
            self._loaded_files.remove(filename)
        if self.tabs_count > 1:
            self.removeTab(index)
            return
        self.setTabText(index, CoreApp.translate("tab_manager", _DEFAULT_TAB_NAME))
        child_editor.clear()
        self.setTabIcon(index, QIcon())

    def has_changes_selected_option(self) -> int:
        msg = Messages(
            parent=self,
            content="Hay cambios presentes ¿desea cerrar de todas formas?",
            first_button_title="Cerrar",
            type=MessageTypes.WARNING,
        )
        return msg.run()

    def change_tab_name(self, name: str) -> None:
        self.setTabText(self.current_index, name)
