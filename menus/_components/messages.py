from dataclasses import dataclass
from typing import Final
from enum import Enum, auto
from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtCore import QCoreApplication as coreapp


def set_common(
    msg: QMessageBox, title: str, content: str, first_option_title: str
) -> None:
    """
    A function that sets common features of the message dialog like the title,
    content and the first button, that commonly is used to confirmation
    """
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Cancel)
    msg.setText(content)
    msg.addButton(
        coreapp.translate("messages", first_option_title), QMessageBox.AcceptRole
    )


def system_error(parent: QWidget) -> None:
    QMessageBox.critical(
        parent,
        coreapp.translate("messages", MessageConstants.SYSTEM_ERROR_TITLE),
        coreapp.translate("messages", MessageConstants.SYSTEM_ERROR_MESSAGE),
    )
    # TODO: enviar este error a un sistema de reportes?


@dataclass(frozen=True)
class MessageConstants:
    SYSTEM_ERROR_TITLE: Final[str] = "Error"
    SYSTEM_ERROR_MESSAGE: Final[str] = (
        "Ocurrió un error inesperado en el sistema. Por favor inténtelo de nuevo."
    )
    SYSTEM_WARNING_TITLE: Final[str] = "Advertencia"


class MessageOptions(Enum):
    OK = auto()


class Message(QMessageBox):

    def __init__(self):
        super().__init__()
