from typing import Final
from PySide6.QtWidgets import QMainWindow
from menus.menu_bar import MenuBar
from toolbar import ToolBar
from editor import Editor
from statusbar import StatusBar


class Home(QMainWindow):
    _MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"
    _MAIN_WINDOW_MIN_HEIGHT: Final[int] = 300
    _MAIN_WINDOW_MIN_WIDTH: Final[int] = 400
    _MAIN_WINDOW_DEFAULT_HEIGHT: Final[int] = 600
    _MAIN_WINDOW_DEFAULT_WIDTH: Final[int] = 1000

    def __init__(self):
        super().__init__()
        self._set_main_window_config()
        self._call_main_widgets()

    def _set_main_window_config(self) -> None:
        self.setWindowTitle(self._MAIN_WINDOW_TITLE)
        self._set_dimensions()

    def _set_dimensions(self) -> None:
        self.setMinimumHeight(self._MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(self._MAIN_WINDOW_MIN_WIDTH)
        self.resize(self._MAIN_WINDOW_DEFAULT_WIDTH, self._MAIN_WINDOW_DEFAULT_HEIGHT)

    def _call_main_widgets(self) -> None:
        self._set_main_window_config()
        self.menu = MenuBar(home=self)
        self._set_toolbar()
        self._set_editor()
        self._set_status_bar()

    def _set_toolbar(self) -> None:
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar.get_toolbar)

    def _set_editor(self) -> None:
        self.editor = Editor()
        self.setCentralWidget(self.editor.get_editor)

    def _set_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar)
