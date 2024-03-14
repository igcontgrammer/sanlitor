from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout

from editor import Editor


class Dialog(QDialog):
    def __init__(self, parent: Editor):
        super().__init__()
        self._parent = parent
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

    def add_button(self, content: str) -> None:
        button = QPushButton(content, self)
        self._layout.addWidget(button)
