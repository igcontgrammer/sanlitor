from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileIconProvider, QToolBar

"""
    Toolbar actions:
    - New
    - Open Folder
    - Save
    - Save All
    - Close
    - Close All
    - Print
    - Show Terminal
"""


class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self._toolbar = QToolBar("Toolbar")
        self._set_default_settings()
        self._set_actions()

    def get_toolbar(self) -> QToolBar:
        return self._toolbar

    def _set_default_settings(self) -> None:
        self._toolbar.setMovable(False)
        self._toolbar.setFloatable(False)

    def _set_actions(self) -> None:
        self._new_action()
        self._open_action()
        self._save_action()
        # self._toolbar.addAction(icons.icon(QFileIconProvider.File), "Open Folder")
        # self._toolbar.addAction(self._open_action())
        # self._toolbar.addAction(self._save_action())
        # self._toolbar.addAction(self._save_all_action())
        # self._toolbar.addAction(self._close_action())
        # self._toolbar.addAction(self._close_all_action())
        # self._toolbar.addAction(self._print_action())
        # self._toolbar.addAction(self.addSeparator())
        # self._toolbar.addAction(self._cut_action())

    def _new_action(self) -> None:
        file_icon = QFileIconProvider()
        new_action = self._toolbar.addAction(
            file_icon.icon(QFileIconProvider.File), "New"
        )
        new_action.triggered.connect(self._new)

    def _open_action(self) -> None:
        folder_icon = QFileIconProvider()
        open_action = self._toolbar.addAction(
            folder_icon.icon(QFileIconProvider.Folder), "Open Folder"
        )
        open_action.triggered.connect(self._open)

    def _save_action(self) -> None:
        save_icon = QFileIconProvider()
        save_action = self._toolbar.addAction(
            save_icon.icon(QFileIconProvider.Computer), "Save"
        )
        save_action.triggered.connect(self._save)

    def _save_all_action(self) -> None:
        save_all_action = QAction("Save All", self)
        save_all_action.triggered.connect(self._save_all)

    def _close_action(self) -> None:
        close_action = QAction("Close", self)
        close_action.triggered.connect(self._close)

    def _close_all_action(self) -> None:
        close_all_action = QAction("Close All", self)
        close_all_action.triggered.connect(self._close_all)

    def _print_action(self) -> None:
        print_action = QAction("Print", self)
        print_action.triggered.connect(self._print)

    def _cut_action(self) -> None:
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self._cut)

    @Slot()
    def _new(self) -> None:
        print("New from toolbar...")

    @Slot()
    def _open(self) -> None:
        print("Open from toolbar...")

    @Slot()
    def _save(self) -> None:
        print("Save from toolbar...")

    @Slot()
    def _save_all(self) -> None:
        print("Save all from toolbar...")

    @Slot()
    def _close(self) -> None:
        print("Close from toolbar...")

    @Slot()
    def _close_all(self) -> None:
        print("Close all from toolbar...")

    @Slot()
    def _print(self) -> None:
        print("Print from toolbar...")

    @Slot()
    def _cut(self) -> None:
        print("Cut from toolbar...")
