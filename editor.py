from PySide6.QtWidgets import QTextEdit

"""
TODO: aplicar los estados segun el usuario seleccione
Apply Syntax Highlighting
Fonts
Colors
"""


class Editor(QTextEdit):
    def __init__(self):
        super().__init__()
        self._editor = QTextEdit()

    @property
    def get_editor(self) -> QTextEdit:
        return self._editor
