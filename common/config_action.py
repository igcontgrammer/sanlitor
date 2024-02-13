from PySide6.QtGui import QAction


class ConfigAction:
    @staticmethod
    def config_action(
        action: QAction, status_tip: str, shortcut: str, method: object
    ) -> None:
        action.setStatusTip(status_tip)
        action.setShortcut(shortcut)
        action.triggered.connect(method)
