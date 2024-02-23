from .._menus_constants import MessageTypes
from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtCore import QCoreApplication as coreapp


class Messages(QMessageBox):
    def __init__(self, parent: QWidget, context: str, message: str, type: MessageTypes):
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

    @staticmethod
    def system_error(parent: QWidget, exception_message: str = "") -> None:
        QMessageBox.critical(
            parent,
            coreapp.translate("messages", "Error"),
            coreapp.translate(
                "messages", "Ocurrió un error inesperado. Por favor inténtelo de nuevo."
            ),
        )
        # TODO: enviar este error a un sistema de reportes?
        if len(exception_message.strip()) > 0:
            print("sending to system reports...")

    def __repr__(self) -> str:
        return f"Messages(parent={self._parent}, context={self._context}, message={self._message}, type={self._type})"
