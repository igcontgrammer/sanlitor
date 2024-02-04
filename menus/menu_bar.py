from PySide6.QtWidgets import QMainWindow
from menus.file_menu import FileMenu
from menus.edit_menu import EditMenu
from menus.search_menu import SearchMenu


class MenuBar(QMainWindow):

    def __init__(self, home: QMainWindow):
        super().__init__()
        self._menu = home.menuBar()
        self._file_menu = FileMenu()
        self._edit_menu = EditMenu()
        self._search_menu = SearchMenu()
        self._add_and_show_menus()
        # edit menu
        # search menu
        # view menu
        # terminal menu
        # configuration menu
        # help menu
        # self.set_menus()

    def _add_and_show_menus(self) -> None:
        self._menu.addMenu(self._file_menu.get_menu)
        self._menu.addMenu(self._edit_menu.get_menu)
        self._menu.addMenu(self._search_menu.get_menu)
        pass
