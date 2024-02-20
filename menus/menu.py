from PySide6.QtWidgets import QMainWindow
from menus.file_menu import FileMenu
from menus.edit_menu import EditMenu
from menus.search_menu import SearchMenu
from menus.view_menu import ViewMenu
from menus.encoding_menu import EncodingMenu
from menus.language_menu import LanguageMenu
from menus.settings_menu import SettingsMenu
from menus.plugins_menu import PluginsMenu
from menus.terminal_menu import TerminalMenu
from menus.help_menu import HelpMenu
from menus.tools_menus import ToolsMenu


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
        self._menu.addMenu(self._file_menu.get_menu)
        self._menu.addMenu(self._edit_menu.get_menu)
        self._menu.addMenu(self._search_menu.get_menu)
        self._menu.addMenu(self._view_menu.get_menu)
        self._menu.addMenu(self._encoding_menu.get_menu)
        self._menu.addMenu(self._language_menu.get_menu)
        self._menu.addMenu(self._settings_menu.get_menu)
        self._menu.addMenu(self._tools_menu.get_menu)
        self._menu.addAction(self._plugins_menu.get_menu.menuAction())
        self._menu.addMenu(self._terminal_menu.get_menu)
        self._menu.addMenu(self._help_menu.get_menu)
