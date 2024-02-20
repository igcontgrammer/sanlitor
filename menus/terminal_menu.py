from . import QMenu, QAction, Slot, ConfigAction, SectionsNames


class TerminalMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._terminal_menu = QMenu(SectionsNames.TERMINAL)
        self._create_actions()

    @property
    def get_menu(self) -> QMenu:
        return self._terminal_menu

    def _create_actions(self) -> None:
        self._add_new_terminal_action()
        self._split_terminal_action()

    def _add_new_terminal_action(self) -> None:
        new_terminal = QAction("New Terminal", self)
        ConfigAction().config_action(
            new_terminal,
            "Ctrl+Shift+T",
            "",
            self._new_terminal,
        )
        self._terminal_menu.addAction(new_terminal)

    def _split_terminal_action(self) -> None:
        split_terminal = QAction("Split Terminal", self)
        ConfigAction().config_action(
            split_terminal,
            "Ctrl+Shift+D",
            "",
            self._split_terminal,
        )
        self._terminal_menu.addAction(split_terminal)

    @Slot()
    def _new_terminal(self) -> None:
        print("new terminal")

    @Slot()
    def _split_terminal(self) -> None:
        print("split terminal")
