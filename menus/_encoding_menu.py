from ._menus_constants import EncodingMenuActionsNames
from . import QMenu, QAction, Slot, ActionHelper, SectionsNames


class EncodingMenu(QMenu):

    def __init__(self):
        super().__init__()
        self._encoding_menu = QMenu(SectionsNames.ENCODING)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._encoding_menu

    def _create_actions(self) -> None:
        self._set_ANSI_action()
        self._set_UTF_8_action()
        self._encoding_menu.addSeparator()
        self._convert_to_ANSI()
        self._convert_to_UTF_8()

    def _set_ANSI_action(self) -> None:
        set_ansi_action = QAction(EncodingMenuActionsNames.ANSI, self)
        ActionHelper().config(
            action=set_ansi_action,
            status_tip="Set ANSI encoding",
            shortcut="",
            method=self.set_ANSI,
        )
        self._encoding_menu.addAction(set_ansi_action)

    def _set_UTF_8_action(self) -> None:
        set_UTF_8_action = QAction(EncodingMenuActionsNames.UTF_8, self)
        ActionHelper().config(
            action=set_UTF_8_action,
            status_tip="Set UTF-8 encoding",
            shortcut="",
            method=self.set_UTF_8,
        )
        self._encoding_menu.addAction(set_UTF_8_action)

    def _convert_to_ANSI(self) -> None:
        convert_to_ANSI_action = QAction(EncodingMenuActionsNames.CONVERT_TO_ANSI, self)
        ActionHelper().config(
            action=convert_to_ANSI_action,
            status_tip="Convert to ANSI",
            shortcut="",
            method=self.convert_to_ANSI,
        )
        self._encoding_menu.addAction(convert_to_ANSI_action)

    def _convert_to_UTF_8(self) -> None:
        convert_to_UTF_8_action = QAction(
            EncodingMenuActionsNames.CONVERT_TO_UTF_8, self
        )
        ActionHelper().config(
            action=convert_to_UTF_8_action,
            status_tip="Convert to UTF-8",
            shortcut="",
            method=self.convert_to_UTF_8,
        )
        self._encoding_menu.addAction(convert_to_UTF_8_action)

    @Slot()
    def set_ANSI(self) -> None:
        print("Setting ANSI encoding")
        pass

    @Slot()
    def set_UTF_8(self) -> None:
        print("Setting UTF-8 encoding")
        pass

    @Slot()
    def convert_to_ANSI(self) -> None:
        print("Converting to ANSI")
        pass

    @Slot()
    def convert_to_UTF_8(self) -> None:
        print("Converting to UTF-8")
        pass
