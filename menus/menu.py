from PySide6.QtWidgets import QMainWindow
from menus._file_menu import FileMenu
from menus._edit_menu import EditMenu
from menus._search_menu import SearchMenu
from menus._view_menu import ViewMenu
from menus._encoding_menu import EncodingMenu
from menus._language_menu import LanguageMenu
from menus._settings_menu import SettingsMenu
from menus._plugins_menu import PluginsMenu
from menus._terminal_menu import TerminalMenu
from menus._help_menu import HelpMenu
from menus._tools_menus import ToolsMenu


class MenuBar(QMainWindow):

    def __init__(self, home: QMainWindow):
        super().__init__()
        self._menu = home.menuBar()
        self._file_menu = FileMenu(home=home)
        self._edit_menu = EditMenu()
        self._search_menu = SearchMenu()
        self._view_menu = ViewMenu()
        self._encoding_menu = EncodingMenu()
        self._language_menu = LanguageMenu()
        self._settings_menu = SettingsMenu()
        self._tools_menu = ToolsMenu()
        self._plugins_menu = PluginsMenu()
        self._terminal_menu = TerminalMenu()
        self._help_menu = HelpMenu()
        self._add_menus()

    def _add_menus(self) -> None:
        self._menu.addMenu(self._file_menu.menu)
        self._menu.addMenu(self._edit_menu.menu)
        self._menu.addMenu(self._search_menu.menu)
        self._menu.addMenu(self._view_menu.menu)
        self._menu.addMenu(self._encoding_menu.menu)
        self._menu.addMenu(self._language_menu.menu)
        self._menu.addMenu(self._settings_menu.menu)
        self._menu.addMenu(self._tools_menu.menu)
        self._menu.addAction(self._plugins_menu.menu.menuAction())
        self._menu.addMenu(self._terminal_menu.menu)
        self._menu.addMenu(self._help_menu.menu)
