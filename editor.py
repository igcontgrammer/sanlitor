from PySide6.QtCore import Slot
from PySide6.QtWidgets import QScrollBar, QTabWidget, QTextEdit

from theme import ThemeModes
from utils import get_circle


class Editor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self._has_changes = False
        self._is_open_mode = False
        self._scroll_bar = QScrollBar(self)
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

    @Slot()
    def _on_change(self) -> None:
        # when open a file and placing content to the editor, doesn't count as change
        if self.is_open_mode:
            return
        self.has_changes = True
        parent = self.parentWidget()
        if parent is not None:
            related_tab = parent.parentWidget()
            if isinstance(related_tab, QTabWidget):
                related_tab.setTabIcon(
                    related_tab.currentIndex(), get_circle(theme=ThemeModes.LIGHT)
                )
            else:
                raise TypeError("tab is not a QTabWidget")

    def __configurate(self) -> None:
        self.textChanged.connect(self._on_change)
        self.setUndoRedoEnabled(True)
        self.setAcceptRichText(True)
        self.setVerticalScrollBar(self._scroll_bar)
