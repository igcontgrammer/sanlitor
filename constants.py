from dataclasses import dataclass
from enum import Enum, auto


class AppMode(Enum):
    DEFAULT = auto()
    TREE = auto()
    SEARCH_IN_FILES = auto()
    REFERENCES = auto()


@dataclass(frozen=True)
class FileNames:
    DEFAULT: str = "Untitled.txt"


@dataclass(frozen=True)
class OpenFileOptions:
    HERE: int = 0
    NEW_TAB: int = 1
    ALLOWED_OPTIONS = (HERE, NEW_TAB)
    CANCEL: int = 2
    OPEN_ANYWAY: int = 0


@dataclass(frozen=True)
class SaveOptions:
    SAVE = 0
    SAVE_AS = 2
    SAVE_ALL = 3
    YES = 0
    NO_SAVE = 1
    CANCEL = 2


@dataclass(frozen=True)
class TabActions:
    CLOSE: int = 0


# theme modes
class ThemeModes(Enum):
    LIGHT = auto()
    DARK = auto()
