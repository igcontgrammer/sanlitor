from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from PySide6.QtWidgets import QMessageBox, QWidget


@dataclass(frozen=True)
class ButtonDescription:
    OK: str = "De acuerdo"
    CANCEL: str = "Cancelar"


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
        first_button_title=ButtonDescription.OK,
        message_type=MessageTypes.CRITICAL,
    )
    msg.setWindowTitle(CommonMessageTitles.ERROR)
    msg.setStandardButtons(QMessageBox.Cancel)  # type: ignore
    msg.button(QMessageBox.Cancel).setText("Cancelar")  # type: ignore
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
        self._message.setWindowTitle(message_type if title is None else title)  # type: ignore
        self._message.setStandardButtons(QMessageBox.Cancel)  # type: ignore
        self._message.setText(self._content)  # type: ignore
        self._message.addButton(first_button_title, QMessageBox.AcceptRole)  # type: ignore
        self._message.button(QMessageBox.Cancel).setText("Cancelar")  # type: ignore
        match message_type:  # type: ignore
            case MessageTypes.CRITICAL:  # type: ignore
                self._message.setIcon(QMessageBox.Critical)  # type: ignore
            case MessageTypes.WARNING:  # type: ignore
                self._message.setIcon(QMessageBox.Warning)  # type: ignore
            case MessageTypes.QUESTION:  # type: ignore
                self._message.setIcon(QMessageBox.Question)  # type: ignore

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value

    def run(self) -> int:
        return self._message.exec_()

    def add_button(self, description: str) -> None:
        self._message.addButton(description, QMessageBox.AcceptRole)  # type: ignore
