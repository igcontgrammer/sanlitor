from typing import Final

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QPlainTextEdit, QScrollBar, QTabWidget

from constants import ThemeModes
from extensions import Extensions
from syntax import PythonSyntaxFactory
from utils import get_circle

TAB_SIZE: Final[str] = "   "


class Editor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self._has_changes = False
        self._is_open_mode = False
        self._scroll_bar = QScrollBar(self)
        # font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        # self.setFont(font)
        self.setDocument(self.document())
        self.__configurate()

    @property
    def has_changes(self) -> bool:
        return self._has_changes

    @has_changes.setter
    def has_changes(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("value must be boolean")
        self._has_changes = value

    @property
    def is_open_mode(self) -> bool:
        return self._is_open_mode

    @is_open_mode.setter
    def is_open_mode(self, value: bool) -> None:
        self._is_open_mode = value

    def set_syntax(self, extension: str) -> None:
        match extension:
            case Extensions.PLAIN_TEXT:
                self.highlighter = None
            case Extensions.PYTHON:
                print("la extension es Python")
                self.highlighter = PythonSyntaxFactory().set_syntax(self.document())
            case _:
                pass

    @Slot()
    def on_change(self) -> None:
        if self.is_open_mode:
            return
        self.has_changes = True
        parent = self.parentWidget()
        if parent is None:
            print("nothing to check")
            return
        related_tab = parent.parentWidget()
        if isinstance(related_tab, QTabWidget):
            related_tab.setTabIcon(
                related_tab.currentIndex(), get_circle(theme=ThemeModes.LIGHT)
            )
        else:
            raise TypeError("tab is not a QTabWidget")

    def keyPressEvent(self, event: QKeyEvent):  # type: ignore
        if event.key() == Qt.Key_Tab:  # type: ignore
            self.insertPlainText(TAB_SIZE)
        else:
            super(Editor, self).keyPressEvent(event)

    def __configurate(self) -> None:
        self.textChanged.connect(self.on_change)
        self.setUndoRedoEnabled(True)
        self.setVerticalScrollBar(self._scroll_bar)
