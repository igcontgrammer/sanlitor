import sys
from home import Home
from typing import Self
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo


class Main(QApplication):

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super(Main, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, argv):
        super().__init__(argv)
        self.home = Home()
        self.home.show()


if __name__ == "__main__":
    app = Main(sys.argv)
    translator = QTranslator()
    if translator.load(
        QLocale.system(), "", "", QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    ):
        app.installTranslator(translator)
    exit(app.exec())
