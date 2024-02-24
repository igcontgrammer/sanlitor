from typing import Final, List
from editor import EditorManager
from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import QCoreApplication as coreapp
from messages import Messages, MessageTypes
from constants import TabsActions

_DEFAULT_TAB_NAME: Final[str] = "Untitled"


class TabManager(QTabWidget):

    def __init__(self):
        super().__init__()
        self._tab = QTabWidget()
        self._editor_manager = EditorManager()
        self._loaded_files: List[str] = []

    # ************* getters *************

    @property
    def tab(self) -> QTabWidget:
        return self._tab

    @property
    def editor_has_changes(self) -> bool:
        return self._editor_manager.has_changes

    def get_loaded_files(self) -> List[str]:
        return list(set(self._loaded_files))

    def file_was_opened(self, filename: str) -> bool:
        return filename in self.get_loaded_files()

    def get_current_tab_index(self) -> int:
        return self._tab.currentIndex()

    def get_tabs_count(self) -> int:
        return self._tab.count()

    # ************* SETTERS *************

    def set_content_to_current_tab(self, content: str) -> None:
        self._tab.widget(self.get_current_tab_index()).setPlainText(content)

    # ************* OTHERS *************

    def move(self, filename: str):
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
        self._tab.addTab(self._editor_manager.editor, _DEFAULT_TAB_NAME)
        self._tab.setTabsClosable(True)
        self._tab.tabCloseRequested.connect(self.on_close_tab)

    # TODO: aplicar la logica de los cambios al agregar un nuevo tab
    def add_new_tab(self, name: str, content: str) -> None:
        # * Para usar correctamente el @classmethod, en una linea se debe declarar
        new_manager = EditorManager()
        new_index = self._tab.addTab(new_manager.editor, name)
        self._tab.setCurrentIndex(new_index)
        self._tab.widget(new_index).setPlainText(content)
        self._tab.tabCloseRequested.connect(self.on_close_tab)

    # TODO: create the on save state
    # TODO: esta cerrando aunque presione X en el mensaje
    def on_close_tab(self, index: int) -> None:
        if self.editor_has_changes:
            option = self.has_changes_selected_option()
            if option == TabsActions.CLOSE:
                has_more_tabs = self.get_tabs_count() > 1
                (
                    self._tab.removeTab(index)
                    if has_more_tabs
                    else self._tab.setTabText(
                        index, coreapp.translate("tab_manager", _DEFAULT_TAB_NAME)
                    )
                )
                return
        filename = self._tab.tabText(index)
        if filename in self._loaded_files:
            self._loaded_files.remove(filename)
        if self.get_tabs_count() > 1:
            self._tab.removeTab(index)
            return
        self._tab.setTabText(index, coreapp.translate("tab_manager", _DEFAULT_TAB_NAME))

    def has_changes_selected_option(self) -> int:
        msg = Messages(
            parent=self,
            content="Hay cambios presentes ¿desea cerrar de todas formas?",
            first_button_title="Cerrar",
            type=MessageTypes.WARNING,
        )
        return msg.run()

    def change_current_tab_name(self, name: str) -> None:
        self._tab.setTabText(self.get_current_tab_index(), name)
