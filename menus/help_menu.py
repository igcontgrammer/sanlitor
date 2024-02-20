from . import QMenu, QAction, Slot, ActionHelper, SectionsNames


class HelpMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._help_menu = QMenu(SectionsNames.HELP)
        self._create_actions()

    def get_menu(self) -> QMenu:
        return self._help_menu

    def _create_actions(self) -> None:
        self._show_all_commands_action()
        self._documentation_action()

    def _show_all_commands_action(self) -> None:
        show_all_commands_action = QAction("Show All Commands", self)
        ActionHelper().config(
            action=show_all_commands_action,
            status_tip="Show All Commands",
            shortcut="",
            method=self._show_all_commands,
        )
        self._help_menu.addAction(show_all_commands_action)

    def _documentation_action(self) -> None:
        documentation_action = QAction("Documentation", self)
        ActionHelper().config(
            action=documentation_action,
            status_tip="Documentation",
            shortcut="",
            method=self._documentation,
        )
        self._help_menu.addAction(documentation_action)

    @Slot()
    def _show_all_commands(self) -> None:
        print("Show All Commands")

    @Slot()
    def _documentation(self) -> None:
        print("Documentation")
