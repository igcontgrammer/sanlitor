from ._menus_constants import HelpMenuActionsNames, HelpMenuShortcuts
from . import QMenu, QAction, Slot, ActionHelper, SectionsNames


class HelpMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._help_menu = QMenu(SectionsNames.HELP)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._help_menu

    def _create_actions(self) -> None:
        self._show_all_commands_action()
        self._documentation_action()
        self._tips_and_tricks_actions()
        self._report_issue_action()
        self._check_for_updates_action()

    def _show_all_commands_action(self) -> None:
        show_all_commands_action = QAction(HelpMenuActionsNames.SHOW_ALL_COMMANDS, self)
        ActionHelper().config(
            action=show_all_commands_action,
            status_tip="Show All Commands",
            shortcut=HelpMenuShortcuts.SHOW_ALL_COMMANDS,
            method=self._show_all_commands,
        )
        self._help_menu.addAction(show_all_commands_action)

    def _documentation_action(self) -> None:
        documentation_action = QAction(HelpMenuActionsNames.DOCUMENTATION, self)
        ActionHelper().config(
            action=documentation_action,
            status_tip="Documentation",
            shortcut="",
            method=self._documentation,
        )
        self._help_menu.addAction(documentation_action)

    def _tips_and_tricks_actions(self) -> None:
        tips_and_tricks_action = QAction(HelpMenuActionsNames.TIPS_AND_TRICKS, self)
        ActionHelper().config(
            action=tips_and_tricks_action,
            status_tip="Tips and tricks",
            shortcut="",
            method=self._tips_and_tricks,
        )

    def _report_issue_action(self) -> None:
        report_issue_action = QAction(HelpMenuActionsNames.REPORT_ISSUE, self)
        ActionHelper().config(
            action=report_issue_action,
            status_tip="Report an issue...",
            shortcut="",
            method=self._report_issue,
        )

    def _check_for_updates_action(self) -> None:
        check_for_update_action = QAction(HelpMenuActionsNames.CHECK_FOR_UPDATES, self)
        ActionHelper().config(
            action=check_for_update_action,
            status_tip="Check for updates...",
            shortcut="",
            method=self._check_for_updates,
        )

    @Slot()
    def _show_all_commands(self) -> None:
        print("Show All Commands")

    @Slot()
    def _documentation(self) -> None:
        print("Documentation")

    @Slot()
    def _tips_and_tricks(self) -> None:
        print("tips and tricks...")

    @Slot()
    def _report_issue(self) -> None:
        print("Report issue...")

    @Slot()
    def _check_for_updates(self) -> None:
        print("Check for updates...")
