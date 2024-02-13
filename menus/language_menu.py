from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot

"""
TODO: Se ordena alfabéticamente. Por ej la letra J tendrá: Java, Javascript. C: C#,C, C++
"""


class LanguageMenu(QMenu):
    _MENU_NAME: Final[str] = "Language"

    def __init__(self):
        super().__init__()
        self._language_menu = QMenu(self._MENU_NAME)

    @property
    def get_menu(self) -> QMenu:
        return self._language_menu
