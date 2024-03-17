import os
from dataclasses import dataclass
from typing import Final, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget

from constants import AppMode, SaveOptions, ThemeModes
from editor import Editor
from menus.menu import MenuBar
from messages import Messages, MessageTypes
from statusbar import StatusBar
from storage_manager import StorageManager, save_from_path
from tab_manager import Tab

_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"


@dataclass(frozen=True)
class _DefaultDimension:
    MAIN_WINDOW_MIN_HEIGHT: int = 300
    MAIN_WINDOW_MIN_WIDTH: int = 400
    MAIN_WINDOW_DEFAULT_HEIGHT: int = 600
    MAIN_WINDOW_DEFAULT_WIDTH: int = 1000


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self._splitter = QSplitter(Qt.Horizontal)  # type: ignore
        self._storage_manager = StorageManager()
        self._mode = self._storage_manager.app_mode
        self._tab = Tab(home=self)
        self._theme_mode = ThemeModes.LIGHT
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self.load_central()

    @property
    def tab(self) -> Tab:
        return self._tab

    @property
    def theme_mode(self) -> ThemeModes:
        return self._theme_mode

    @property
    def mode(self) -> int:
        return self._mode

    @mode.setter
    def mode(self, value: int) -> None:
        self._mode = value

    @property
    def last_tab_worked_index(self) -> int:
        return self._storage_manager.last_tab_worked_index

    @property
    def storage_manager(self):
        return self._storage_manager

    def load_central(self) -> None:
        mode = self._storage_manager.app_mode
        if mode == AppMode.DEFAULT:
            self.change_central(AppMode.DEFAULT)
        elif mode == AppMode.TREE:
            from tree import Tree

            path = self._storage_manager.folder_selected
            if path is None:
                # TODO: si no existe o fue eliminado, que hacer?
                self.change_central(AppMode.DEFAULT)
            else:
                tree = Tree(self, path)
                self.change_central(AppMode.TREE, tree.get())  # type: ignore
        elif mode == AppMode.SEARCH_IN_FILES:
            pass
        elif mode == AppMode.REFERENCES:
            pass
        else:
            self.change_central(AppMode.DEFAULT)

    def change_central(self, mode: int, widget: Optional[QWidget] = None) -> None:
        if mode != AppMode.DEFAULT and widget is not None:
            self._splitter.addWidget(widget)
            self._splitter.addWidget(self._tab)
            self.setCentralWidget(self._splitter)
        else:
            self.setCentralWidget(self._tab)

    def closeEvent(self, event: QCloseEvent) -> None:
        any_changes = self.tab.tabs_has_changes()
        option = None
        if any_changes:
            msg = Messages(
                parent=self,
                content="Hay cambios sin guardar ¿desea guardar todo?",
                first_button_title="Guardar",
                message_type=MessageTypes.QUESTION,
            )
            msg.add_button("No guardar")
            option = msg.run()
            if option != SaveOptions.SAVE and option != SaveOptions.NO_SAVE:
                event.ignore()
                msg.close()
                return
        if option == SaveOptions.NO_SAVE:
            super().closeEvent(event)
            return
        if self._tab.has_new_tabs or option == SaveOptions.YES:
            for path in self._storage_manager.paths:
                file_name = os.path.basename(path)
                for i in range(self._tab.count()):
                    if file_name != self._tab.tabText(i):
                        continue
                    editor = self._tab.widget(i)
                    if not isinstance(editor, Editor):
                        print("editor is not an instance of Editor")
                        return None
                    content = editor.toPlainText()
                    ok, error_msg = save_from_path(path, content)
                    if not ok:
                        msg = Messages(
                            parent=self,
                            content=error_msg,
                            first_button_title="De acuerdo",
                            message_type=MessageTypes.CRITICAL,
                        )
                        msg.run()
                        break
                    self._tab.set_normal(file_name)
                    editor.has_changes = False
        ok, error_msg = self._storage_manager.update_mode(self._mode)
        if not ok:
            print(error_msg)
        super().closeEvent(event)

    def _add_menu(self) -> None:
        self.menu = MenuBar(home=self)

    def _add_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar())

    def __set_main_window_default_config(self) -> None:
        self.setWindowTitle(_MAIN_WINDOW_TITLE)
        self.__set_default_dimensions()

    def __call_main_widgets(self) -> None:
        self.__set_main_window_default_config()
        self._add_menu()
        self._add_status_bar()

    def __set_default_dimensions(self) -> None:
        self.setMinimumHeight(_DefaultDimension.MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(_DefaultDimension.MAIN_WINDOW_MIN_WIDTH)
        self.resize(
            _DefaultDimension.MAIN_WINDOW_DEFAULT_WIDTH,
            _DefaultDimension.MAIN_WINDOW_DEFAULT_HEIGHT,
        )
