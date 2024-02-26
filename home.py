from dataclasses import dataclass
from typing import Final, Self, Tuple

from PySide6.QtWidgets import QMainWindow

from menus.menu import MenuBar
from statusbar import StatusBar
from tab_manager import Tab
from theme import ThemeModes
from toolbar import ToolBar

_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"


@dataclass(frozen=True)
class HomeDefaultDimensions:
    MAIN_WINDOW_MIN_HEIGHT: int = 300
    MAIN_WINDOW_MIN_WIDTH: int = 400
    MAIN_WINDOW_DEFAULT_HEIGHT: int = 600
    MAIN_WINDOW_DEFAULT_WIDTH: int = 1000


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
        self._geometry = self.geometry()
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self._tab.build_default_tab()
        self.setCentralWidget(self._tab)

    @property
    def tab_manager(self) -> Tab:
        return self._tab

    def x(self) -> int:
        return self._geometry.x() + (self._geometry.width() // 2)

    def y(self) -> int:
        return self._geometry.y() + (self._geometry.height() // 2)

    @property
    def center_coordinates(self) -> Tuple[int]:
        return (self.x(), self.y())

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
        self.setMinimumHeight(HomeDefaultDimensions.MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(HomeDefaultDimensions.MAIN_WINDOW_MIN_WIDTH)
        self.resize(
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_WIDTH,
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_HEIGHT,
        )
