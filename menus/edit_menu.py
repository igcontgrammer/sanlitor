from dataclasses import dataclass
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot
from typing import Final
from utils import Utils


@dataclass(frozen=True)
class EditMenuActionsNames:
    UNDO: str = "Undo"
    REDO: str = "Redo"
    CUT: str = "Cut"
    COPY: str = "Copy"
    PASTE: str = "Paste"
    SELECT_ALL: str = "Select All"


@dataclass(frozen=True)
class EditMenuShortcuts:
    UNDO: str = "Ctrl+Z"
    REDO: str = "Ctrl+Shift+Z"
    CUT: str = "Ctrl+X"
    COPY: str = "Ctrl+C"
    PASTE: str = "Ctrl+V"
    SELECT_ALL: str = "Ctrl+A"


class EditMenu(QMenu):
    _MENU_NAME: Final[str] = "Edit"

    def __init__(self):
        super().__init__()
        self._edit_menu = QMenu(self._MENU_NAME)
        self._add_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._edit_menu

    def _add_menus(self) -> None:
        self._edit_menu.addAction(self._undo_action())

    def _undo_action(self) -> QAction:
        undo_action = QAction(EditMenuActionsNames.UNDO, self)
        Utils().config_action(
            action=undo_action,
            shortcut=EditMenuShortcuts.UNDO,
            status_tip="Undo",
            method=self._undo,
        )
        return undo_action

    @Slot()
    def _undo(self) -> None:
        print("Undo...")
