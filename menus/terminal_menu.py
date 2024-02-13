from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


class TerminalMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._terminal_menu = QMenu("Terminal")

    @property
    def get_menu(self) -> QMenu:
        return self._terminal_menu
