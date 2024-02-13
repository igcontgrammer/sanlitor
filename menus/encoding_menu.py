from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot


@dataclass(frozen=True)
class EncodingMenuActionsNames:
    ANSI: Final[str] = "ANSI"
    UTF_8: Final[str] = "UTF-8"
    UTF_8_WITH_BOM: Final[str] = "UTF-8 with BOM"
    UTF_16_BE_BOM: Final[str] = "UTF-16 BE BOM"
    UTF_16_LE_BOM: Final[str] = "UTF-16 LE BOM"
    CONVERT_TO_ANSI: Final[str] = "Convert to ANSI"
    CONVERT_TO_UTF_8: Final[str] = "Convert to UTF-8"
    CONVERT_TO_UTF_8_BOM: Final[str] = "Convert to UTF-8-BOM"
    CONVERT_TO_UTF_16_BE_BOM: Final[str] = "Convert to UTF-16 BE BOM"
    CONVERT_TO_UTF_16_LE_BOM: Final[str] = "Convert to UTF-16 LE BOM"


class EncodingMenu(QMenu):
    _MENU_NAME: Final[str] = "Encoding"

    def __init__(self):
        super().__init__()
        self._encoding_menu = QMenu(self._MENU_NAME)
        self._call_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._encoding_menu

    def _call_menus(self) -> None:
        self._set_ANSI_action()
        pass

    def _set_ANSI_action(self) -> None:
        self._ansi_action = QAction(EncodingMenuActionsNames.ANSI, self)
        self._ansi_action.triggered.connect(self._on_ansi_action)
        self._encoding_menu.addAction(self._ansi_action)

    def _set_UTF_8_action(self) -> None:
        self._utf_8_action = QAction(EncodingMenuActionsNames.UTF_8, self)
        self._utf_8_action.triggered.connect(self._on_utf_8_action)
        self._encoding_menu.addAction(self._utf_8_action)

    @Slot()
    def _on_ansi_action(self) -> None:
        print("on ANSI")
        pass

    @Slot()
    def _on_utf_8_action(self) -> None:
        print("on UTF-8")
        pass
