import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Slot
from home import Home


class Main(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.home = Home()
        self.home.show()


if __name__ == "__main__":
    app = Main(sys.argv)
    exit(app.exec())
