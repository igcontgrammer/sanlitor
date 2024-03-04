from common.config_action import config

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import TerminalMenuActionsNames, TerminalMenuShortcuts


class TerminalMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.setTitle(SectionsNames.TERMINAL)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

    def _create_actions(self) -> None:
        self._add_new_terminal_action()
        self._split_terminal_action()

    def _add_new_terminal_action(self) -> None:
        new_terminal = QAction(TerminalMenuActionsNames.NEW_TERMINAL, self)
        config(
            new_terminal,
            TerminalMenuShortcuts.NEW_TERMINAL,
            "",
            self._new_terminal,
        )
        self.addAction(new_terminal)

    def _split_terminal_action(self) -> None:
        split_terminal = QAction("Split Terminal", self)
        config(
            split_terminal,
            TerminalMenuShortcuts.SPLIT_TERMINAL,
            "",
            self._split_terminal,
        )
        self.addAction(split_terminal)

    @Slot()
    def _new_terminal(self) -> None:
        print("new terminal")

    @Slot()
    def _split_terminal(self) -> None:
        print("split terminal")
