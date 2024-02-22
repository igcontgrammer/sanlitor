from .._menus_constants import MessageTypes
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication as coreapp


class Messages(QMessageBox):
    def __init__(self, parent, context: str, message: str, type: MessageTypes):
        super().__init__()
        self._parent = parent
        self._context = context
        self._message = message
        self._type = type

    def show(self) -> None:
        match self._type:
            case MessageTypes.WARNING:
                pass
            case MessageTypes.QUESTION:
                pass
            case MessageTypes.CRITICAL:
                QMessageBox.critical(
                    self._parent,
                    coreapp.translate(self._context, "Error"),
                    coreapp.translate(self._context, self._message),
                )
            case _:
                print("otro...")
