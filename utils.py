import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPixmap

from constants import ThemeModes


def get_extension(file_name: str) -> str:
    return f".{file_name.split('.')[1]}"


def get_extension_from_path(path: str) -> str:
    return os.path.splitext(path)[1]


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def filename_is_valid(filename: str) -> bool:
    for char in filename:
        if char in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]:
            return False
    return True


def has_selected_file(path: str) -> bool:
    return len(path) > 0


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
            dark_icon.fill(QColor(Qt.black))  # type: ignore
            icon = QIcon(dark_icon)
            return icon
        case ThemeModes.DARK:
            light_icon = QPixmap(10, 10)
            light_icon.fill(QColor(Qt.white))  # type: ignore
            icon = QIcon(light_icon)
            return icon
        case _:
            print("error")
            return None  # type: ignore
