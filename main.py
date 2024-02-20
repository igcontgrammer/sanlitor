import sys
from home import Home
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo


class Main(QApplication):
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
