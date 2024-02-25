from theme import ThemeModes
from PySide6.QtWidgets import QTextEdit, QScrollBar, QTabWidget
from PySide6.QtCore import Slot
from utils import get_circle


class Editor(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_changes = False
        self._is_open_mode = False
        self._scroll_bar = QScrollBar(self)
        self.__configurate()

    # ************* GETTERS AND SETTERS *************

    def __repr__(self) -> str:
        return super().__repr__()

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

    @Slot()
    def on_change(self) -> None:
        self.has_changes = True
        parent = self.parentWidget()
        if parent is not None:
            tab = parent.parentWidget()
            if isinstance(tab, QTabWidget) and not self.is_open_mode:
                tab.setTabIcon(tab.currentIndex(), get_circle(theme=ThemeModes.LIGHT))

    def __configurate(self) -> None:
        self.textChanged.connect(self.on_change)
        self.setUndoRedoEnabled(True)
        self.setAcceptRichText(True)
        self.setVerticalScrollBar(self._scroll_bar)
