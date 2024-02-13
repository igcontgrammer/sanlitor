from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


class SettingsMenu(QMenu):
    _MENU_NANE: Final[str] = "Settings"

    def __init__(self):
        super().__init__()
        self._settings_menu = QMenu(self._MENU_NANE)

    @property
    def get_menu(self) -> QMenu:
        return self._settings_menu
