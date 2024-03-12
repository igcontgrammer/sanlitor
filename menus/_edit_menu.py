from common.config_action import config

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import EditMenuActionsNames, EditMenuShortcuts


class EditMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        from home import Home
        from tab_manager import Tab

        self._home: Home = home
        self._tab: Tab = self._home.tab
        self.setTitle(SectionsNames.EDIT)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

    def _create_actions(self) -> None:
        self._undo_action()
        self._redo_action()
        self._select_all_action()

    def _undo_action(self) -> None:
        undo_action = QAction(EditMenuActionsNames.UNDO, self)
        config(
            action=undo_action,
            shortcut=EditMenuShortcuts.UNDO,
            status_tip="Undo",
            method=self._undo,
        )
        self.addAction(undo_action)

    def _redo_action(self) -> None:
        redo_action = QAction(EditMenuActionsNames.REDO, self)
        config(
            action=redo_action,
            shortcut=EditMenuShortcuts.REDO,
            status_tip="Redo",
            method=self._redo,
        )
        self.addAction(redo_action)

    def _select_all_action(self) -> None:
        select_all_action = QAction(EditMenuActionsNames.SELECT_ALL, self)
        config(
            action=select_all_action,
            shortcut=EditMenuShortcuts.SELECT_ALL,
            status_tip="Select All",
            method=self._select_all,
        )
        self.addAction(select_all_action)

    @Slot()
    def _undo(self) -> None:
        editor = self._tab.editor
        editor.undo()

    @Slot()
    def _redo(self) -> None:
        editor = self._tab.editor
        editor.redo()

    @Slot()
    def _select_all(self) -> None:
        editor = self._tab.editor
        editor.selectAll()
