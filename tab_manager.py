from typing import Final, List, Optional

from PySide6.QtCore import QCoreApplication as CoreApp
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTabWidget

from constants import TabActions
from editor import Editor
from messages import Messages, MessageTypes

_DEFAULT_TAB_NAME: Final[str] = "Untitled.txt"


class Tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self._editor = Editor()
        self._loaded_files: List[str] = []

    @property
    def editor(self) -> Editor:
        return self._editor

    @property
    def editor_has_changes(self) -> bool:
        return self._editor.has_changes

    @editor_has_changes.setter
    def editor_has_changes(self, value: bool) -> None:
        self._editor.has_changes = value

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

    def already_opened(self, filename: str) -> bool:
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

    def new(self, filename: str, content: Optional[str] = None) -> None:
        new_editor = Editor()
        new_editor.setPlainText("" if content is None else content)
        new_editor.has_changes = False
        new_index = self.addTab(new_editor, filename)
        self.setCurrentIndex(new_index)
        self._loaded_files.append(filename)

    # TODO: create the on save state
    def on_close(self, index: int) -> None:
        filename = self.tabText(index)
        editor = self.widget(index)
        if not isinstance(editor, Editor):
            raise TypeError("editor is not an Editor object")
        if editor.has_changes:
            option = self.has_changes_selected_option()
            if option != TabActions.CLOSE:
                return
            if self.is_default:
                editor.clear()
                self.setTabIcon(index, QIcon())
                self.setTabText(index, _DEFAULT_TAB_NAME)
                editor.has_changes = False
                if filename in self._loaded_files:
                    self._loaded_files.remove(filename)
                return
            else:
                self.removeTab(index)
                editor.has_changes = False
                self._loaded_files.remove(filename)
                return
        if filename in self._loaded_files:
            self._loaded_files.remove(filename)
        if self.tabs_count > 1:
            self.removeTab(index)
            return
        self.setTabText(index, CoreApp.translate("tab_manager", _DEFAULT_TAB_NAME))
        editor.clear()
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
