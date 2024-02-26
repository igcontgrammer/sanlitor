from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional

from PySide6.QtCore import QCoreApplication as coreapp
from PySide6.QtWidgets import QMessageBox, QWidget


class MessageTypes(Enum):
    WARNING = auto()
    CRITICAL = auto()
    QUESTION = auto()


_COMMON_MESSAGE_TITLES: Dict[int, str] = {1: "Advertencia", 2: "Error", 3: "Aviso"}


@dataclass(frozen=True)
class MessageConstants:
    SYSTEM_ERROR_TITLE: str = "Error"
    SYSTEM_ERROR_MESSAGE: str = (
        "Ocurrió un error inesperado en el sistema. Por favor inténtelo de nuevo."
    )
    SYSTEM_WARNING_TITLE: str = "Advertencia"


class Messages(QMessageBox):
    def __init__(
        self,
        parent: QWidget,
        content: str,
        first_button_title: str,
        type: MessageTypes,
        title: Optional[str] = "",
    ):
        super().__init__()
        self._parent = parent
        self._message = QMessageBox(self._parent)
        self._message.setWindowTitle(
            coreapp.translate(
                "messages",
                _COMMON_MESSAGE_TITLES[type.value] if title is None else title,
            )
        )
        self._message.setStandardButtons(QMessageBox.Cancel)
        self._message.setText(content)
        self._message.addButton(
            coreapp.translate("messages", first_button_title), QMessageBox.AcceptRole
        )
        self._message.button(QMessageBox.Cancel).setText(
            coreapp.translate("messages", "Cancelar")
        )
        match type:
            case MessageTypes.CRITICAL:
                self._message.setIcon(QMessageBox.Critical)
            case MessageTypes.WARNING:
                self._message.setIcon(QMessageBox.Warning)
            case MessageTypes.QUESTION:
                self._message.setIcon(QMessageBox.Question)

    def run(self) -> int:
        return self._message.exec_()

    def add_button(self, description: str) -> None:
        self._message.addButton(
            coreapp.translate("messages", description), QMessageBox.AcceptRole
        )


def system_error(parent: QWidget) -> None:
    QMessageBox.critical(
        parent,
        coreapp.translate("messages", MessageConstants.SYSTEM_ERROR_TITLE),
        coreapp.translate("messages", MessageConstants.SYSTEM_ERROR_MESSAGE),
    )
    # TODO: enviar este error a un sistema de reportes?
