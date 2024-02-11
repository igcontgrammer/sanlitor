from PySide6.QtWidgets import QTextEdit


class Editor(QTextEdit):
    def __init__(self):
        super().__init__()
        self._editor = QTextEdit()

    @property
    def get_editor(self) -> QTextEdit:
        return self._editor
