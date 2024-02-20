from PySide6.QtGui import QAction


class ActionHelper:
    @staticmethod
    def config(action: QAction, status_tip: str, shortcut: str, method: object) -> None:
        action.setStatusTip(status_tip)
        action.setShortcut(shortcut)
        action.triggered.connect(method)
