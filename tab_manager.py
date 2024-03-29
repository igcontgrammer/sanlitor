import os
from pathlib import Path
from typing import List, Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QTabWidget

from constants import FileNames, TabActions
from editor import Editor
from extensions import get_extensions_list
from messages import Messages, MessageTypes, show_system_error_message
from utils import get_extension, has_selected


class Tab(QTabWidget):
    def __init__(self, home):
        super().__init__()
        from home import Home

        self._home: Home = home
        self._has_on_close = None
        self._editor = Editor()
        self._loaded_files: List[str] = []
        self._build_on_startup()

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
    def home(self):
        return self._home

    @property
    def loaded_files(self) -> List[str]:
        return self._loaded_files

    @property
    def has_tabs(self) -> bool:
        return self.count() > 0

    @property
    def has_one_tab(self) -> bool:
        return self.count() == 1

    @property
    def has_new_tabs(self) -> bool:
        return len(self._loaded_files) > 0

    def set_default(self, index: int) -> None:
        self.setTabIcon(index, QIcon())
        self.setTabText(index, FileNames.DEFAULT)

    def set_normal(self, name: Optional[str] = None) -> None:
        self.setTabIcon(self.currentIndex(), QIcon())
        if name is not None:
            self.setTabText(self.currentIndex(), name)

    def already_opened(self, file_name: str) -> bool:
        return file_name in self._loaded_files

    def tabs_has_changes(self) -> bool:
        for i in range(self.count()):
            editor = self.widget(i)
            if not isinstance(editor, Editor):
                return False
            if editor.has_changes:
                return True
        return False

    def _build_on_startup(self) -> None:
        has_worked = len(self._home.storage_manager.paths) > 0
        if not has_worked:
            self.build_default_tab()
            return
        any_exists = False
        paths_removed_or_moved: List[Path] = []
        for path in self._home.storage_manager.paths:
            if not os.path.exists(path):
                paths_removed_or_moved.append(path)
                continue
            any_exists = True
            try:
                with open(path, "r") as file:
                    content = file.read()
                    self.new_from_already_exists(path.name, content)
            except Exception as e:
                print(e)
                show_system_error_message(
                    self._home,
                    f"Tuvimos problemas con la siguiente ubicación: \n\n{path}. \n\nPor favor revise si el archivo "
                    f"existe o si tiene permisos para leerlo.",
                )
                return
        if len(paths_removed_or_moved) > 0:
            content = ""
            for i, moved in enumerate(paths_removed_or_moved):
                if i == 7:
                    content += "..."
                    break
                else:
                    content += f"{os.path.basename(moved)}\n"
            msg = Messages(
                parent=self._home,
                content="Los siguientes archivos no existen o fueron movidos:\n\n"
                        + content,
                first_button_title="De acuerdo",
                message_type=MessageTypes.WARNING,
            )
            msg.run()
        if not any_exists:
            self.build_default_tab()

    def add_content_to_current_tab(self, content: str) -> None:
        editor = self.widget(self.currentIndex())
        if not isinstance(editor, Editor):
            raise TypeError("editor is not an Editor object")
        editor.setPlainText(content)

    def set_editor_has_changes(self, value: bool) -> None:
        self._editor.has_changes = value

    def set_is_open_mode(self, value: bool) -> None:
        self._editor.is_open_mode = value

    def move(self, file_name: str) -> None:  # type: ignore
        for i in range(self.count()):
            if file_name == self.tabText(i):
                self.setCurrentIndex(i)
                break

    def add_to_loaded_files(self, file_name: str) -> None:
        self._loaded_files.append(file_name)

    def remove_from_loaded_files(self, file_name: str) -> None:
        self._loaded_files.remove(file_name)

    def build_default_tab(self) -> None:
        self.addTab(self._editor, FileNames.DEFAULT)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_close)
        if FileNames.DEFAULT not in self._loaded_files:
            self._loaded_files.append(FileNames.DEFAULT)

    def new(self) -> None:
        file = QFileDialog.getSaveFileName(
            parent=self._home,
            caption="Guardar archivo",
            dir=os.path.expanduser("~"),
            filter=get_extensions_list(),
        )
        path = file[0]
        if has_selected(path):
            return None
        status = self._home.storage_manager.add(path)
        if status[0] is False:
            print(f"error: {status[1]}")
            return None
        file_name = os.path.basename(path)
        editor = Editor()
        editor.has_changes = False
        index = self.addTab(editor, file_name)
        if self._has_on_close is None:
            self.tabCloseRequested.connect(self.on_close)
            self._has_on_close = True
        self.setTabsClosable(True)
        self.setCurrentIndex(index)
        if file_name not in self._loaded_files:
            self._loaded_files.append(file_name)

    def new_from_tree(self, path: str) -> None:
        pass

    def new_from_already_exists(self, file_name: str, content: str) -> None:
        extension = get_extension(file_name)
        editor = Editor()
        editor.set_syntax(extension)
        editor.setPlainText(content)
        editor.has_changes = False
        self.addTab(editor, file_name)
        if self._has_on_close is None:
            self.tabCloseRequested.connect(self.on_close)
            self._has_on_close = True
        self.setTabsClosable(True)

    def on_close(self, index: int) -> None:
        editor = self.widget(index)
        if not isinstance(editor, Editor):
            msg = Messages(
                parent=self,
                content="Ocurrió un error inesperado al cerrar el archivo",
                first_button_title="De acuerdo",
                message_type=MessageTypes.CRITICAL,
            )
            msg.run()
            return
        file_name = self.tabText(index)
        if editor.has_changes:
            msg = Messages(
                parent=self,
                content="Este archivo tiene cambios. ¿Desea cerrar de todas formas?",
                first_button_title="Cerrar",
                message_type=MessageTypes.QUESTION,
            )
            option = msg.run()
            if option != TabActions.CLOSE:
                msg.close()
                return
            if self.has_one_tab:
                if file_name == FileNames.DEFAULT:
                    self.setTabIcon(index, QIcon())
                    self.setTabText(index, FileNames.DEFAULT)
                    return
                else:
                    remove_status = self._home.storage_manager.remove(file_name)
                    if remove_status[0] is False:
                        msg = Messages(
                            parent=self._home,
                            content="Tuvimos problemas para cerrar correctamente este archivo. Inténtelo de nuevo.",
                            first_button_title="De acuerdo",
                            message_type=MessageTypes.CRITICAL,
                        )
                        msg.run()
                        return
                self.setTabIcon(index, QIcon())
                self.setTabText(index, FileNames.DEFAULT)
                editor.clear()
                editor.has_changes = False
            else:
                self.removeTab(index)
                editor.has_changes = False
                remove_status = self._home.storage_manager.remove(file_name)
                if remove_status[0] is False:
                    msg = Messages(
                        parent=self._home,
                        content="Tuvimos problemas para cerrar correctamente este archivo. Inténtelo de nuevo.",
                        first_button_title="De acuerdo",
                        message_type=MessageTypes.CRITICAL,
                    )
                    msg.run()
                    return
        else:
            if self.has_one_tab:
                if file_name == FileNames.DEFAULT:
                    self.setTabText(index, FileNames.DEFAULT)
                else:
                    self.setTabText(index, FileNames.DEFAULT)
                    editor.clear()
                    editor.has_changes = False
                    self._home.storage_manager.remove(file_name)
            else:
                self.removeTab(index)
                editor.has_changes = False
                self._home.storage_manager.remove(file_name)
        editor.clear()
        editor.has_changes = False
        self.setTabIcon(index, QIcon())

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
