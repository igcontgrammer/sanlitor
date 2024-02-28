import os
from dataclasses import dataclass
from typing import Final, List

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow

from editor import Editor
from menus.menu import MenuBar
from statusbar import StatusBar
from storage_manager import get_opened_files, has_opened_tabs, save_opened_file
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
        self._tab = Tab()
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
    def loaded_files(self) -> List[str]:
        return self.tab_manager.loaded_files

    def _build_tabs_on_startup(self) -> None:
        if has_opened_tabs():
            opened_files = get_opened_files()
            for filename in opened_files:
                with open(_TEMP_FILES_PATH + filename, "r") as file:
                    content = file.read()
                    editor = Editor()
                    editor.setPlainText(content)
                    editor.has_changes = False
                    self._tab.addTab(editor, filename)
        else:
            self._tab.build_default_tab()
        self.setCentralWidget(self._tab)

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            opened_files = get_opened_files()
            for i in range(self.tab_manager.tabs_count):
                editor = self.tab_manager.widget(i)
                if not isinstance(editor, Editor):
                    raise TypeError("editor is not an Editor object")
                filename = self.tab_manager.tabText(i)
                content = editor.toPlainText()
                with open(_TEMP_FILES_PATH + filename, "w") as file:
                    file.write(content)
                if filename not in opened_files:
                    self.save_last_opened_files(filename)
        except IOError:
            print(f"Error al guardar el archivo: {file}")
        except TypeError as te:
            print(f"Error: {te}")
        return super().closeEvent(event)

    def save_last_opened_files(self, filename: str) -> None:
        save_opened_file(filename)

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
