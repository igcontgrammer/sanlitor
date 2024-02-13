from dataclasses import dataclass
from typing import Final
from common.config_action import ConfigAction
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


@dataclass(frozen=True)
class EditMenuActionsNames:
    UNDO: Final[str] = "Undo"
    REDO: Final[str] = "Redo"
    CUT: Final[str] = "Cut"
    COPY: Final[str] = "Copy"
    PASTE: Final[str] = "Paste"
    SELECT_ALL: Final[str] = "Select All"


@dataclass(frozen=True)
class EditMenuShortcuts:
    UNDO: Final[str] = "Ctrl+Z"
    REDO: Final[str] = "Ctrl+Shift+Z"
    CUT: Final[str] = "Ctrl+X"
    COPY: Final[str] = "Ctrl+C"
    PASTE: Final[str] = "Ctrl+V"
    SELECT_ALL: Final[str] = "Ctrl+A"


class EditMenu(QMenu):
    _MENU_NAME: Final[str] = "Edit"
    config_action = ConfigAction()

    def __init__(self):
        super().__init__()
        self._edit_menu = QMenu(self._MENU_NAME)
        self._call_menus()

    @property
    def get_menu(self) -> QMenu:
        return self._edit_menu

    def _call_menus(self) -> None:
        self._undo_action()
        self._redo_action()
        self._cut_action()
        self._copy_action()
        self._paste_action()
        self._select_all_action()

    def _undo_action(self) -> None:
        undo_action = QAction(EditMenuActionsNames.UNDO, self)
        ConfigAction().config_action(
            action=undo_action,
            shortcut=EditMenuShortcuts.UNDO,
            status_tip="Undo",
            method=self._undo,
        )
        self._edit_menu.addAction(undo_action)

    def _redo_action(self) -> None:
        redo_action = QAction(EditMenuActionsNames.REDO, self)
        ConfigAction().config_action(
            action=redo_action,
            shortcut=EditMenuShortcuts.REDO,
            status_tip="Redo",
            method=self._redo,
        )
        self._edit_menu.addAction(redo_action)

    def _cut_action(self) -> None:
        cut_action = QAction(EditMenuActionsNames.CUT, self)
        ConfigAction().config_action(
            action=cut_action,
            shortcut=EditMenuShortcuts.CUT,
            status_tip="Cut",
            method=self._cut,
        )
        self._edit_menu.addAction(cut_action)

    def _copy_action(self) -> None:
        copy_action = QAction(EditMenuActionsNames.COPY, self)
        ConfigAction().config_action(
            action=copy_action,
            shortcut=EditMenuShortcuts.COPY,
            status_tip="Copy",
            method=self._copy,
        )
        self._edit_menu.addAction(copy_action)

    def _paste_action(self) -> None:
        paste_action = QAction(EditMenuActionsNames.PASTE, self)
        ConfigAction().config_action(
            action=paste_action,
            shortcut=EditMenuShortcuts.PASTE,
            status_tip="Paste",
            method=self._paste,
        )
        self._edit_menu.addAction(paste_action)

    def _select_all_action(self) -> None:
        select_all_action = QAction(EditMenuActionsNames.SELECT_ALL, self)
        ConfigAction().config_action(
            action=select_all_action,
            shortcut=EditMenuShortcuts.SELECT_ALL,
            status_tip="Select All",
            method=self._select_all,
        )
        self._edit_menu.addAction(select_all_action)

    @Slot()
    def _undo(self) -> None:
        print("Undo...")

    @Slot()
    def _redo(self) -> None:
        print("Redo...")

    @Slot()
    def _cut(self) -> None:
        print("Cut...")

    @Slot()
    def _copy(self) -> None:
        print("Copy...")

    @Slot()
    def _paste(self) -> None:
        print("Paste...")

    @Slot()
    def _select_all(self) -> None:
        print("Select All...")
