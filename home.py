import os
from dataclasses import dataclass
from typing import Final

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow

from editor import Editor
from menus.menu import MenuBar
from statusbar import StatusBar
from storage_manager import StorageManager
from tab_manager import Tab
from theme import ThemeModes
from toolbar import ToolBar

_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
_TEMP_FILES_PATH = os.path.dirname(__file__) + "/temp_files/"


@dataclass(frozen=True)
class HomeDefaultDimensions:
    MAIN_WINDOW_MIN_HEIGHT: int = 300
    MAIN_WINDOW_MIN_WIDTH: int = 400
    MAIN_WINDOW_DEFAULT_HEIGHT: int = 600
    MAIN_WINDOW_DEFAULT_WIDTH: int = 1000


class Home(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Home, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.storage_manager = StorageManager()
        self._tab = Tab(home=self)
        self._theme_mode = ThemeModes.LIGHT
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self._build_tabs_on_startup()

    @property
    def tab_manager(self) -> Tab:
        return self._tab

    @property
    def theme_mode(self) -> ThemeModes:
        return self._theme_mode

    @property
    def last_tab_worked_index(self) -> int:
        return self.storage_manager.last_tab_worked_index

    # TODO: pasarlo a tab manager porque le compete a esa clase
    def _build_tabs_on_startup(self) -> None:
        tab_manager = self._tab
        if self.storage_manager.has_opened_tabs:
            for filename in self.storage_manager.opened_files:
                with open(_TEMP_FILES_PATH + filename, "r") as read_file:
                    content = read_file.read()
                    tab_manager.new(filename, True, content)
                tab_manager.setCurrentIndex(self.storage_manager.last_tab_worked_index)
        else:
            tab_manager.build_default_tab()
        self.setCentralWidget(tab_manager)

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            has_new_opened_files = len(self._tab.loaded_files) > 0
            if not has_new_opened_files:
                any_changes = False
                for i in range(self._tab.tabs_count):
                    editor = self._tab.widget(i)
                    if not isinstance(editor, Editor):
                        raise TypeError("editor is not an Editor object")
                    if not editor.has_changes:
                        continue
                    any_changes = True
                    file_name = self._tab.tabText(i)
                    content = editor.toPlainText()
                    # todo: esto cambiarlo despues a storage manager, aqui solo se prueba que funcione
                    with open(_TEMP_FILES_PATH + file_name, "w") as file:
                        file.write(content)
                if any_changes is False:
                    self.storage_manager.update_last_tab_worked_index(self._tab.current_index)
                    return
            else:
                # TODO: recoger el ultimo tab en el que trabajó
                opened_files = self.storage_manager.opened_files
                if any(file in opened_files for file in self._tab.loaded_files):
                    return
                self.storage_manager.add_new_opened_files(self._tab.loaded_files, self._tab.current_index)
                for file_name in self._tab.loaded_files:
                    for i in range(self._tab.tabs_count):
                        if self._tab.tabText(i) == file_name:
                            editor = self._tab.widget(i)
                            if not isinstance(editor, Editor):
                                raise TypeError("editor is not an Editor object")
                            content = editor.toPlainText()
                            with open(_TEMP_FILES_PATH + file_name, "w") as file:
                                file.write(content)
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            return super().closeEvent(event)

    def _add_menu(self) -> None:
        self.menu = MenuBar(home=self)

    def _add_toolbar(self) -> None:
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar.get_toolbar())

    def _add_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar())

    def __set_main_window_default_config(self) -> None:
        self.setWindowTitle(_MAIN_WINDOW_TITLE)
        self.__set_default_dimensions()

    def __call_main_widgets(self) -> None:
        self.__set_main_window_default_config()
        self._add_menu()
        self._add_toolbar()
        self._add_status_bar()

    def __set_default_dimensions(self) -> None:
        self.setMinimumHeight(HomeDefaultDimensions.MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(HomeDefaultDimensions.MAIN_WINDOW_MIN_WIDTH)
        self.resize(
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_WIDTH,
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_HEIGHT,
        )
