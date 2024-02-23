from ._menus_constants import EditMenuActionsNames, EditMenuShortcuts
from . import QMenu, QAction, Slot, ActionHelper, SectionsNames


class EditMenu(QMenu):
    config_action = ActionHelper()

    def __init__(self):
        super().__init__()
        self._edit_menu = QMenu(SectionsNames.EDIT)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._edit_menu

    def _create_actions(self) -> None:
        self._undo_action()
        self._redo_action()
        self._cut_action()
        self._copy_action()
        self._paste_action()
        self._select_all_action()

    def _undo_action(self) -> None:
        undo_action = QAction(EditMenuActionsNames.UNDO, self)
        ActionHelper().config(
            action=undo_action,
            shortcut=EditMenuShortcuts.UNDO,
            status_tip="Undo",
            method=self._undo,
        )
        self._edit_menu.addAction(undo_action)

    def _redo_action(self) -> None:
        redo_action = QAction(EditMenuActionsNames.REDO, self)
        ActionHelper().config(
            action=redo_action,
            shortcut=EditMenuShortcuts.REDO,
            status_tip="Redo",
            method=self._redo,
        )
        self._edit_menu.addAction(redo_action)

    def _cut_action(self) -> None:
        cut_action = QAction(EditMenuActionsNames.CUT, self)
        ActionHelper().config(
            action=cut_action,
            shortcut=EditMenuShortcuts.CUT,
            status_tip="Cut",
            method=self._cut,
        )
        self._edit_menu.addAction(cut_action)

    def _copy_action(self) -> None:
        copy_action = QAction(EditMenuActionsNames.COPY, self)
        ActionHelper().config(
            action=copy_action,
            shortcut=EditMenuShortcuts.COPY,
            status_tip="Copy",
            method=self._copy,
        )
        self._edit_menu.addAction(copy_action)

    def _paste_action(self) -> None:
        paste_action = QAction(EditMenuActionsNames.PASTE, self)
        ActionHelper().config(
            action=paste_action,
            shortcut=EditMenuShortcuts.PASTE,
            status_tip="Paste",
            method=self._paste,
        )
        self._edit_menu.addAction(paste_action)

    def _select_all_action(self) -> None:
        select_all_action = QAction(EditMenuActionsNames.SELECT_ALL, self)
        ActionHelper().config(
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
