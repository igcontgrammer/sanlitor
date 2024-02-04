from PySide6 import QtWidgets as qwt, QtCore as qtc, QtGui as gui


class Utils:

    @staticmethod
    def config_action(
        action: gui.QAction, status_tip: str, shortcut: str, method: object
    ) -> None:
        action.setStatusTip(status_tip)
        action.setShortcut(shortcut)
        action.triggered.connect(method)
        pass
