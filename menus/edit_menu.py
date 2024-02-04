from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui
from typing import Final
from enum import Enum
from utils import Utils


class EditMenuActionsNames(Enum):
    UNDO = "Undo"
    REDO = "Redo"
    CUT = "Cut"
    COPY = "Copy"
    PASTE = "Paste"
    SELECT_ALL = "Select all"


class EditMenuShortcuts(Enum):
    UNDO = "Ctrl+Z"
    REDO = "Ctrl+Shift+Z"
    CUT = "Ctrl+X"
    COPY = "Ctrl+C"
    PASTE = "Ctrl+V"
    SELECT_ALL = "Ctrl+A"


class EditMenu(qwt.QMenu):
    _MENU_NAME: Final[str] = "Edit"

    def __init__(self):
        super().__init__()
        self._edit_menu = qwt.QMenu(self._MENU_NAME)
        self.add_menus()

    @property
    def get_menu(self) -> qwt.QMenu:
        return self._edit_menu

    def add_menus(self) -> None:
        self._edit_menu.addAction(self.undo_action())
        pass

    def undo_action(self) -> gui.QAction:
        undo_action = gui.QAction(EditMenuActionsNames.UNDO.value, self)
        Utils().config_action(
            action=undo_action,
            shortcut=EditMenuShortcuts.UNDO.value,
            status_tip="Undo",
            method=self.undo,
        )
        return undo_action

    @qtc.Slot()
    def undo(self) -> None:
        print("Undo...")
        pass
