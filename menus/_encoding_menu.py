from common.config_action import config

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import EncodingMenuActionsNames


class EncodingMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.setTitle(SectionsNames.ENCODING)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

    def _create_actions(self) -> None:
        self._set_ANSI_action()
        self._set_UTF_8_action()
        self.addSeparator()
        self._convert_to_ANSI()
        self._convert_to_UTF_8()

    def _set_ANSI_action(self) -> None:
        set_ansi_action = QAction(EncodingMenuActionsNames.ANSI, self)
        config(
            action=set_ansi_action,
            status_tip="Set ANSI encoding",
            shortcut="",
            method=self.set_ANSI,
        )
        self.addAction(set_ansi_action)

    def _set_UTF_8_action(self) -> None:
        set_UTF_8_action = QAction(EncodingMenuActionsNames.UTF_8, self)
        config(
            action=set_UTF_8_action,
            status_tip="Set UTF-8 encoding",
            shortcut="",
            method=self.set_UTF_8,
        )
        self.addAction(set_UTF_8_action)

    def _convert_to_ANSI(self) -> None:
        convert_to_ANSI_action = QAction(EncodingMenuActionsNames.CONVERT_TO_ANSI, self)
        config(
            action=convert_to_ANSI_action,
            status_tip="Convert to ANSI",
            shortcut="",
            method=self.convert_to_ANSI,
        )
        self.addAction(convert_to_ANSI_action)

    def _convert_to_UTF_8(self) -> None:
        convert_to_UTF_8_action = QAction(
            EncodingMenuActionsNames.CONVERT_TO_UTF_8, self
        )
        config(
            action=convert_to_UTF_8_action,
            status_tip="Convert to UTF-8",
            shortcut="",
            method=self.convert_to_UTF_8,
        )
        self.addAction(convert_to_UTF_8_action)

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
