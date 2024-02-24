from ._menus_constants import ToolsMenuActionsNames
from . import QMenu, QAction, Slot, SectionsNames
from common.config_action import config


class ToolsMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._tools_menu = QMenu(SectionsNames.TOOLS)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._tools_menu

    def _create_actions(self) -> None:
        self._base_64_encode_action()
        self._base_64_decode_action()

    def _base_64_encode_action(self) -> None:
        base_64_encode = QAction(ToolsMenuActionsNames.BASE_64_ENCODE, self)
        config(
            action=base_64_encode,
            shortcut="",
            status_tip="Base 64 Encode",
            method=self._base_64_encode,
        )
        self._tools_menu.addAction(base_64_encode)

    def _base_64_decode_action(self) -> None:
        base_64_decode = QAction(ToolsMenuActionsNames.BASE_64_DECODE, self)
        config(
            action=base_64_decode,
            shortcut="",
            status_tip="Base 64 Decode",
            method=self._base_64_decode,
        )
        self._tools_menu.addAction(base_64_decode)

    @Slot()
    def _base_64_encode(self) -> None:
        print("Base 64 Encode")

    @Slot()
    def _base_64_decode(self) -> None:
        print("Base 64 Decode")
