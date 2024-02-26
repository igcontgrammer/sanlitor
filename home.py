from typing import Final, Self

from PySide6.QtWidgets import QMainWindow

from menus.menu import MenuBar
from statusbar import StatusBar
from tab_manager import Tab
from theme import ThemeModes
from toolbar import ToolBar

_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
_MAIN_WINDOW_MIN_HEIGHT: Final[int] = 300
_MAIN_WINDOW_MIN_WIDTH: Final[int] = 400
_MAIN_WINDOW_DEFAULT_HEIGHT: Final[int] = 600
_MAIN_WINDOW_DEFAULT_WIDTH: Final[int] = 1000


class Home(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super(Home, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        # for now is light by default
        self._tab = Tab()
        self._theme_mode = ThemeModes.LIGHT
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self._tab.build_default_tab()
        self.setCentralWidget(self._tab)

    @property
    def tab_manager(self) -> Tab:
        return self._tab

    @property
    def theme_mode(self) -> ThemeModes:
        return self._theme_mode

    def _add_menu(self) -> None:
        self.menu = MenuBar(home=self)

    # TODO: buscar en la memoria, los ultimos tabs que haya abierto el usuario
    def _get_last_opened_tab(self) -> Tab:
        pass

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
        self.setMinimumHeight(_MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(_MAIN_WINDOW_MIN_WIDTH)
        self.resize(_MAIN_WINDOW_DEFAULT_WIDTH, _MAIN_WINDOW_DEFAULT_HEIGHT)
