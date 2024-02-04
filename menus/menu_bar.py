from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui
from menus.file_menu import FileMenu
from menus.edit_menu import EditMenu


class MenuBar(qwt.QMenuBar):

    def __init__(self, home: qwt.QMainWindow):
        super().__init__()
        self._menu = home.menuBar()
        self._file_menu = FileMenu()
        self._edit_menu = EditMenu()
        self.add_and_show_menus()
        # edit menu
        # search menu
        # view menu
        # terminal menu
        # configuration menu
        # help menu
        # self.set_menus()
        pass

    def add_and_show_menus(self) -> None:
        self._menu.addMenu(self._file_menu.get_menu)
        self._menu.addMenu(self._edit_menu.get_menu)
        pass
