from typing import Final
from menus.menu import MenuBar
from toolbar import ToolBar
from statusbar import StatusBar
from tab_manager import TabManager
from PySide6.QtWidgets import QMainWindow


_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
_MAIN_WINDOW_MIN_HEIGHT: Final[int] = 300
_MAIN_WINDOW_MIN_WIDTH: Final[int] = 400
_MAIN_WINDOW_DEFAULT_HEIGHT: Final[int] = 600
_MAIN_WINDOW_DEFAULT_WIDTH: Final[int] = 1000


class Home(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self._tab_manager = TabManager()
        self._tab_manager.build_default_tab()
        self.setCentralWidget(self._tab_manager.tab)

    @property
    def tab_manager(self) -> TabManager:
        return self._tab_manager

    def _set_menu(self) -> None:
        self.menu = MenuBar(home=self)

    # TODO: buscar en la memoria, los ultimos tabs que haya abierto el usuario
    def _get_last_opened_tab(self) -> TabManager:
        pass

    def _set_toolbar(self) -> None:
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar.get_toolbar())

    def _set_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar())

    def __set_main_window_default_config(self) -> None:
        self.setWindowTitle(_MAIN_WINDOW_TITLE)
        self.__set_default_dimensions()

    def __call_main_widgets(self) -> None:
        self.__set_main_window_default_config()
        self._set_menu()
        self._set_toolbar()
        self._set_status_bar()

    def __set_default_dimensions(self) -> None:
        self.setMinimumHeight(_MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(_MAIN_WINDOW_MIN_WIDTH)
        self.resize(_MAIN_WINDOW_DEFAULT_WIDTH, _MAIN_WINDOW_DEFAULT_HEIGHT)
