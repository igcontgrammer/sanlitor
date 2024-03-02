import os
from typing import Final, List, Optional

from PySide6.QtCore import QCoreApplication as CoreApp
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTabWidget

from constants import TabActions
from editor import Editor
from messages import Messages, MessageTypes, show_system_error_message
from paths import Paths

_DEFAULT_TAB_NAME: Final[str] = "Untitled.txt"


class Tab(QTabWidget):
    def __init__(self, home):
        super().__init__()
        self._home = home
        self._has_on_close = None
        self._editor = Editor()
        self._loaded_files: List[str] = []
        self._closed_files: List[str] = []
        self._build_tabs_on_startup()

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

    @loaded_files.setter
    def loaded_files(self, value: List[str]):
        self._loaded_files = value

    @property
    def has_loaded_files(self) -> bool:
        return len(self._loaded_files) > 0

    @property
    def closed_files(self) -> List[str]:
        return list(set(self._closed_files))

    @property
    def has_closed_files(self) -> bool:
        return len(self._closed_files) > 0

    @property
    def is_default(self) -> bool:
        return self.count() == 1

    @property
    def home(self):
        return self._home

    def _build_tabs_on_startup(self) -> None:
        from home import Home

        self._home: Home
        storage_manager = self._home.storage_manager
        if not storage_manager.has_opened_tabs:
            self.build_default_tab()
        else:
            # TODO: hacer una validacion de existencia de archivo antes de arrancar esto
            for file_name in storage_manager.opened_files:
                is_temp = not any(
                    os.path.basename(file_name) in file
                    for file in storage_manager.saved_files
                )
                if is_temp:
                    with open(Paths.TEMP_FILES + file_name, "r") as file:
                        content = file.read()
                        self.new(file_name, True, content)
                else:
                    for path_saved in storage_manager.saved_files:
                        if file_name == os.path.basename(path_saved):
                            with open(path_saved, "r") as file:
                                content = file.read()
                                self.new(file_name, True, content)
            self.setCurrentIndex(storage_manager.last_tab_worked_index)

    def already_opened(self, file_name: str) -> bool:
        return file_name in self.loaded_files

    def add_content_to_current_tab(self, content: str) -> None:
        editor = self.widget(self.currentIndex())
        if not isinstance(editor, Editor):
            raise TypeError("editor is not an Editor object")
        editor.setPlainText(content)

    def set_editor_has_changes(self, value: bool) -> None:
        self._editor.has_changes = value

    def set_is_open_mode(self, value: bool) -> None:
        self._editor.is_open_mode = value

    def move(self, file_name: str):
        for i in range(self.count()):
            if self.tabText(i) == file_name:
                self.setCurrentIndex(i)
                break

    def add_to_loaded_files(self, file_name: str) -> None:
        self._loaded_files.append(file_name)

    def remove_from_loaded_files(self, file_name: str) -> None:
        self._loaded_files.remove(file_name)

    def build_default_tab(self) -> None:
        self.addTab(self._editor, _DEFAULT_TAB_NAME)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_close)

    def new(
        self, file_name: str, is_from_opened: bool, content: Optional[str] = None
    ) -> None:
        editor = Editor()
        editor.setPlainText("" if content is None else content)
        editor.has_changes = False
        index = self.addTab(editor, file_name)
        if not is_from_opened:
            self.setCurrentIndex(index)
            self._loaded_files.append(file_name)
        if self._has_on_close is None:
            self.tabCloseRequested.connect(self.on_close)
            self._has_on_close = True
        self.setTabsClosable(True)

    def on_close(self, index: int) -> None:
        editor = self.widget(index)
        if not isinstance(editor, Editor):
            msg = Messages(
                parent=self,
                content="Ocurrió un error para cerrar el tab.",
                first_button_title="De acuerdo",
                message_type=MessageTypes.CRITICAL,
            )
            msg.run()
            return None
        file_name = self.tabText(index)
        if editor.has_changes:
            self.close_on_has_changes(editor, index, file_name)
        if file_name in self._loaded_files:
            self._loaded_files.remove(file_name)
            self._closed_files.append(file_name)
        if self.count() > 1:
            self.removeTab(index)
            self._closed_files.append(file_name)
            return
        self.setTabText(index, CoreApp.translate("tab_manager", _DEFAULT_TAB_NAME))
        editor.clear()
        self.setTabIcon(index, QIcon())

    def close_on_has_changes(self, editor: Editor, index: int, file_name: str) -> None:
        option = self.has_changes_selected_option()
        if option != TabActions.CLOSE:
            return
        if self.is_default:
            editor.clear()
            self.setTabIcon(index, QIcon())
            self.setTabText(index, _DEFAULT_TAB_NAME)
            editor.has_changes = False
            if file_name in self._loaded_files:
                self._loaded_files.remove(file_name)
                self._closed_files.append(file_name)
            return
        else:
            self.removeTab(index)
            editor.has_changes = False
            self._loaded_files.remove(file_name)
            self._closed_files.append(file_name)
            return

    def has_changes_selected_option(self) -> int:
        msg = Messages(
            parent=self,
            content="Hay cambios presentes ¿desea cerrar de todas formas?",
            first_button_title="Cerrar",
            message_type=MessageTypes.WARNING,
        )
        return msg.run()

    def change_tab_name(self, name: str) -> None:
        self.setTabText(self.currentIndex(), name)
