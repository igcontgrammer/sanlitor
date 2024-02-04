from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui
from typing import Final
from menus.menu_bar import MenuBar


class Home(qwt.QMainWindow):
    _MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
    _MAIN_WINDOW_MIN_HEIGHT: Final[int] = 300
    _MAIN_WINDOW_MIN_WIDTH: Final[int] = 400
    _MAIN_WINDOW_DEFAULT_HEIGHT: Final[int] = 600
    _MAIN_WINDOW_DEFAULT_WIDTH: Final[int] = 1000

    def __init__(self):
        super().__init__()
        self.set_main_window_config()
        self.menu = MenuBar(home=self)
        # create toolbar
        # create central widget (text editor)
        # status bar (at the bottom)

    def set_main_window_config(self):
        self.setWindowTitle(self._MAIN_WINDOW_TITLE)
        self.set_dimensions()

    def set_dimensions(self) -> None:
        self.setMinimumHeight(self._MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(self._MAIN_WINDOW_MIN_WIDTH)
        self.resize(self._MAIN_WINDOW_DEFAULT_WIDTH, self._MAIN_WINDOW_DEFAULT_HEIGHT)
        pass
