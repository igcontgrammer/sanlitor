from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget


class ToolBar(QToolBar):
    def __init__(self, home, actions: List[QAction], **kwargs):
        super().__init__()
        from home import Home

        if isinstance(home, Home):
            self._home = home
        self._actions = actions
        self._default_config()
        self._is_search_menu = kwargs["is_search_menu"] or False
        self._add_actions()
        self.hide()

    def show(self) -> None:
        self.setVisible(True)

    def hide(self) -> None:
        self.setVisible(False)

    def _add_actions(self) -> None:
        if self._is_search_menu:
            self.addWidget(self._get_spacer())
        for action in self._actions:
            self.addAction(action)

    def _get_spacer(self) -> QWidget:
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setAttribute(Qt.WA_TransparentForMouseEvents)
        return spacer

    def _default_config(self) -> None:
        self.setFloatable(False)
        self.setMovable(False)
        self._home.addToolBar(self)
