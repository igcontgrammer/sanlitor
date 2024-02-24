from PySide6.QtWidgets import QTextEdit, QScrollBar, QTabWidget
from PySide6.QtCore import Slot
from theme import ThemeModes
from utils import get_circle

"""
TODO: aplicar los estados segun el usuario seleccione
Apply Syntax Highlighting
Fonts
Colors
Changes events
"""


class EditorManager(QTextEdit):
    def __init__(self):
        super().__init__()
        self._editor = QTextEdit()
        self._has_changes = False
        self._scroll_bar = QScrollBar(self)
        self.__configurate()

    # ************* GETTERS *************

    @property
    def editor(self) -> QTextEdit:
        return self._editor

    @property
    def has_changes(self) -> bool:
        return self._has_changes

    # ************* OTHERS *************

    def __configurate(self) -> None:
        self._editor.setUndoRedoEnabled(True)
        self._editor.setAcceptRichText(True)
        self._editor.setVerticalScrollBar(self._scroll_bar)
        self._editor.textChanged.connect(self._on_change)

    @Slot()
    def _on_change(self) -> None:
        self._has_changes = True
        tab = self._editor.parentWidget().parentWidget()
        if isinstance(tab, QTabWidget):
            index = tab.currentIndex()
            tab.setTabIcon(index, get_circle(theme=ThemeModes.LIGHT))
            pass
