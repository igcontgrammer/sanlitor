from PySide6.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self._status_bar = QStatusBar()
        self._set_default_settings()

    @property
    def get_status_bar(self) -> QStatusBar:
        return self._status_bar

    def _set_default_settings(self) -> None:
        self._status_bar.showMessage("Ready")
