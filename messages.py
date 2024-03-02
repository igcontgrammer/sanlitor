from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from PySide6.QtCore import QCoreApplication as CoreApp
from PySide6.QtWidgets import QMessageBox, QWidget


@dataclass(frozen=True)
class CommonMessageTitles:
    WARNING = "Advertencia"
    ERROR = "Error"
    QUESTION = "Aviso"


class MessageTypes(Enum):
    WARNING = auto()
    CRITICAL = auto()
    QUESTION = auto()


def show_system_error_message(parent: QWidget, content: Optional[str] = None) -> None:
    msg = Messages(
        parent=parent,
        content=content if content is not None else "",
        first_button_title=CoreApp.translate("messages", "De acuerdo"),
        message_type=MessageTypes.CRITICAL,
    )
    msg.setWindowTitle(CommonMessageTitles.ERROR)
    msg.setStandardButtons(QMessageBox.Cancel)
    msg.button(QMessageBox.Cancel).setText(CoreApp.translate("messages", "Cancelar"))
    msg.run()


def get_title(message_type: MessageTypes):
    match message_type:
        case MessageTypes.CRITICAL:
            return CommonMessageTitles.ERROR
        case MessageTypes.WARNING:
            return CommonMessageTitles.WARNING
        case MessageTypes.QUESTION:
            return CommonMessageTitles.QUESTION


class Messages(QMessageBox):
    def __init__(
        self,
        parent: QWidget,
        content: str,
        first_button_title: str,
        message_type: MessageTypes,
        title: Optional[str] = "",
    ):
        super().__init__()
        self._parent = parent
        self._content = content
        self._message = QMessageBox(self._parent)
        self._message.setWindowTitle(
            CoreApp.translate(
                "messages", get_title(message_type) if title is None else title
            )
        )
        self._message.setStandardButtons(QMessageBox.Cancel)
        self._message.setText(self._content)
        self._message.addButton(
            CoreApp.translate("messages", first_button_title), QMessageBox.AcceptRole
        )
        self._message.button(QMessageBox.Cancel).setText(
            CoreApp.translate("messages", "Cancelar")
        )
        match message_type:
            case MessageTypes.CRITICAL:
                self._message.setIcon(QMessageBox.Critical)
            case MessageTypes.WARNING:
                self._message.setIcon(QMessageBox.Warning)
            case MessageTypes.QUESTION:
                self._message.setIcon(QMessageBox.Question)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value

    def run(self) -> int:
        return self._message.exec_()

    def add_button(self, description: str) -> None:
        self._message.addButton(
            CoreApp.translate("messages", description), QMessageBox.AcceptRole
        )
