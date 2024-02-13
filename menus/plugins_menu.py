from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


class PluginsMenu(QMenu):
    _MENU_NAME: Final[str] = "Plugins"

    def __init__(self):
        super().__init__()
        self._plugin_menu = QMenu(self._MENU_NAME)

    @property
    def get_menu(self) -> QMenu:
        return self._plugin_menu
