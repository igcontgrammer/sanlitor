from theme import ThemeModes
from PySide6.QtGui import QPixmap, QIcon, QColor
from PySide6.QtCore import Qt


def get_circle(theme: ThemeModes) -> QIcon:
    """A function that returns a white or black circle icon, according to the selected theme

    Args:
        theme: ThemeModes -> Light or Dark

    Returns:
        the QIcon object
    """
    match theme:
        case ThemeModes.LIGHT:
            dark_icon = QPixmap(10, 10)
            dark_icon.fill(QColor(Qt.black))
            icon = QIcon(dark_icon)
            return icon
        case ThemeModes.DARK:
            light_icon = QPixmap(10, 10)
            light_icon.fill(QColor(Qt.white))
            icon = QIcon(light_icon)
            return icon
        case _:
            print("error")
            return None