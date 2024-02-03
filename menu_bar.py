from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui
from typing import Final


class MenuBar(qwt.QMenuBar):
    _FILE_SECTION_NAME: Final[str] = "File"
    _EDIT_SECTION_NAME: Final[str] = "Edit"
    _SEARCH_SECTION_NAME: Final[str] = "Search"
    _VIEW_SECTION_NAME: Final[str] = "View"
    _TERMINAL_SECTION_NAME: Final[str] = "Terminal"
    _CONFIGURATION_SECTION_NAME: Final[str] = "Configuration"
    _HELP_SECTION_NAME: Final[str] = "Help"

    def __init__(self, main_window: qwt.QMainWindow):
        super().__init__()
        self._menu_bar = main_window.menuBar()
        self.set_menus()

    def set_menus(self) -> None:
        self.get_file_menu().show()
        self.get_edit_menu().show()
        self.get_search_menu().show()
        self.get_view_menu().show()
        self.get_terminal_menu().show()
        self.get_configuration_menu().show()
        self.get_help_menu().show()
        pass

    def get_file_menu(self) -> qwt.QMenu:
        file_menu = self._menu_bar.addMenu(self._FILE_SECTION_NAME)
        new_file_action = self.get_new_file_action()
        open_file_action = self.get_open_file_action()
        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        return file_menu

    def get_edit_menu(self) -> qwt.QMenu:
        edit_menu = self._menu_bar.addMenu(self._EDIT_SECTION_NAME)
        edit_file_action = self.get_edit_file_action()
        edit_menu.addAction(edit_file_action)
        return edit_menu

    def get_search_menu(self) -> qwt.QMenu:
        search_menu = self._menu_bar.addMenu(self._SEARCH_SECTION_NAME)
        return search_menu

    def get_view_menu(self) -> qwt.QMenu:
        view_menu = self._menu_bar.addMenu(self._VIEW_SECTION_NAME)
        return view_menu

    def get_terminal_menu(self) -> qwt.QMenu:
        terminal_menu = self._menu_bar.addMenu(self._TERMINAL_SECTION_NAME)
        return terminal_menu

    def get_configuration_menu(self) -> qwt.QMenu:
        configuration_menu = self._menu_bar.addMenu(self._CONFIGURATION_SECTION_NAME)
        return configuration_menu

    def get_help_menu(self) -> qwt.QMenu:
        help_menu = self._menu_bar.addMenu(self._HELP_SECTION_NAME)
        return help_menu

    # *********** actions ***********

    def get_new_file_action(self) -> gui.QAction:
        new_file_action = gui.QAction("New", self)
        new_file_action.setStatusTip("Create a new file")
        new_file_action.triggered.connect(self.new_file)
        return new_file_action

    def get_open_file_action(self) -> gui.QAction:
        open_file_action = gui.QAction("Open", self)
        open_file_action.setStatusTip("Open a new file")
        open_file_action.triggered.connect(self.open_file)
        return open_file_action

    def get_edit_file_action(self) -> gui.QAction:
        edit_file_action = gui.QAction("Edit", self)
        edit_file_action.setStatusTip("Edit a file")
        edit_file_action.triggered.connect(self.edit_file)
        return edit_file_action

    # *********** slots *************

    @qtc.Slot()
    def open_file(self) -> None:
        print("Opening file...")
        # abrir la ventana de windows para abrir un archivo
        pass

    @qtc.Slot()
    def new_file(self) -> None:
        print("Creating new file...")
        # abrir la ventana de windows para seleccionar la carpeta donde desea alojar el archivo
        pass

    @qtc.Slot()
    def edit_file(self) -> None:
        print("Editing a file")
        pass
