import os
from typing import Final, List, Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QTabWidget

from constants import TabActions
from editor import Editor
from extensions import get_extensions_list
from messages import Messages, MessageTypes
from paths import Paths

_DEFAULT_TAB_NAME: Final[str] = "Untitled.txt"


class Tab(QTabWidget):
    def __init__(self, home):
        super().__init__()
        from home import Home

        self._home: Home = home
        self._has_on_close = None
        self._editor = Editor()
        self._loaded_files: List[str] = []
        self._closed_files: List[str] = []
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
    def worked_files(self) -> List[str]:
        return list(set(self._loaded_files))

    @worked_files.setter
    def worked_files(self, value: List[str]):
        self._loaded_files = value

    @property
    def opened_new_files(self) -> bool:
        return len(self._loaded_files) > 0

    @property
    def closed_files(self) -> List[str]:
        return list(set(self._closed_files))

    @property
    def has_closed_files(self) -> bool:
        return len(self._closed_files) > 0

    @property
    def is_default(self) -> bool:
        es_def = "Untitled" in self.tabText(self.currentIndex())
        print(f"es def?: {es_def}")
        return self.count() == 1

    @property
    def home(self):
        return self._home

    def tabs_has_changes(self) -> bool:
        for i in range(self.count()):
            editor = self.widget(i)
            if not isinstance(editor, Editor):
                print("editor is not an Editor object")
                return False
            if editor.has_changes:
                return True
        return False

    def _build_on_startup(self) -> None:
        has_worked = len(self._home.storage_manager.paths) > 0
        if not has_worked:
            self.build_default_tab()
            return
        for path in self._home.storage_manager.paths:
            file_name = os.path.basename(path)
            try:
                with open(path, "r") as file:
                    content = file.read()
                    self.new_from_startup(file_name, content)
            except Exception as e:
                print(e)
                break

    def already_opened(self, file_name: str) -> bool:
        return file_name in self.worked_files

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
        self.addTab(self._editor, _DEFAULT_TAB_NAME)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_close)
        if _DEFAULT_TAB_NAME not in self._loaded_files:
            self._loaded_files.append(_DEFAULT_TAB_NAME)

    # TODO: siempre se creará un archivo nuevo, obteniendo el path de este al ser guardado
    def new(self) -> None:
        file = QFileDialog.getSaveFileName(
            parent=self._home,
            caption="Guardar archivo",
            dir=os.path.expanduser("~"),
            filter=get_extensions_list(),
        )
        path = file[0]
        if len(path) == 0:
            print("no se quiso agregar o guardar ningun archivo")
            return None
        status = self._home.storage_manager.add_path(path)
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

    def new_from_startup(self, file_name: str, content: str) -> None:
        editor = Editor()
        editor.setPlainText(content)
        editor.has_changes = False
        self.addTab(editor, file_name)
        if self._has_on_close is None:
            self.tabCloseRequested.connect(self.on_close)
            self._has_on_close = True
        self.setTabsClosable(True)

    def on_close(self, index: int) -> None:
        print(f"index recibido: {index}")
        # TODO: si se cierra el tab, se elimina del storage
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
            if self.count() == 1:
                if file_name == _DEFAULT_TAB_NAME:
                    self.setTabIcon(index, QIcon())
                    self.setTabText(index, _DEFAULT_TAB_NAME)
                    return
                else:
                    remove_status = self._home.storage_manager.remove(file_name)
                    # TODO: el error es que el PATH no existe
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
                self.setTabText(index, _DEFAULT_TAB_NAME)
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
            if self.count() == 1:
                self.setTabText(index, _DEFAULT_TAB_NAME)
            else:
                self.removeTab(index)
                editor.has_changes = False
                self._home.storage_manager.remove(file_name)
        editor.clear()
        editor.has_changes = False
        self.setTabIcon(index, QIcon())

        # editor = self.widget(index)
        # if not isinstance(editor, Editor):
        #     msg = Messages(
        #         parent=self,
        #         self
        #         content="Ocurrió un error para cerrar el tab.",
        #         first_button_title="De acuerdo",
        #         message_type=MessageTypes.CRITICAL,
        #     )
        #     msg.run()
        #     return None
        # file_name = self.tabText(index)
        # if editor.has_changes:
        #     self.close_on_has_changes(editor, index, file_name)
        # if file_name in self._loaded_files:
        #     self._loaded_files.remove(file_name)
        #     self._closed_files.append(file_name)
        # if self.count() > 1:
        #     self.removeTab(index)
        #     self._closed_files.append(file_name)
        #     return
        # self.setTabText(index, _DEFAULT_TAB_NAME)
        # editor.clear()
        # self.setTabIcon(index, QIcon())

    def close_on_has_changes(self, editor: Editor, index: int, file_name: str) -> None:
        pass
        # option = self.has_changes_selected_option()
        # if option != TabActions.CLOSE:
        #     return
        # if self.is_default:
        #     editor.clear()
        #     self.setTabIcon(index, QIcon())
        #     self.setTabText(index, _DEFAULT_TAB_NAME)
        #     editor.has_changes = False
        #     if file_name in self._loaded_files:
        #         self._loaded_files.remove(file_name)
        #         self._closed_files.append(file_name)
        #     return
        # else:
        #     self.removeTab(index)
        #     editor.has_changes = False
        #     self._loaded_files.remove(file_name)
        #     self._closed_files.append(file_name)
        #     return

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
