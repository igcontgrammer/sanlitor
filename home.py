from typing import Final
from PySide6.QtWidgets import QMainWindow, QTabWidget
from menus.menu import MenuBar
from toolbar import ToolBar
from statusbar import StatusBar
from tab import Tab


MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
MAIN_WINDOW_MIN_HEIGHT: Final[int] = 300
MAIN_WINDOW_MIN_WIDTH: Final[int] = 400
MAIN_WINDOW_DEFAULT_HEIGHT: Final[int] = 600
MAIN_WINDOW_DEFAULT_WIDTH: Final[int] = 1000


class Home(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self._tab = Tab()
        self._tab.build_default_tab()
        self.setCentralWidget(self._tab.get_tab())

    def get_tab(self) -> QTabWidget:
        return self._tab.get_tab()

    def _set_menu(self) -> None:
        self.menu = MenuBar(home=self)

    # TODO: buscar en la memoria, los ultimos tabs que haya abierto el usuario
    def _get_last_opened_tab(self) -> Tab:
        pass

    def _set_toolbar(self) -> None:
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar.get_toolbar)

    def _set_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar)

    def __set_main_window_default_config(self) -> None:
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.__set_default_dimensions()

    def __call_main_widgets(self) -> None:
        self.__set_main_window_default_config()
        self._set_menu()
        self._set_toolbar()
        self._set_status_bar()

    def __set_default_dimensions(self) -> None:
        self.setMinimumHeight(MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(MAIN_WINDOW_MIN_WIDTH)
        self.resize(MAIN_WINDOW_DEFAULT_WIDTH, MAIN_WINDOW_DEFAULT_HEIGHT)
