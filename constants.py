from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class OpenFileOptions:
    HERE: int = 0
    NEW_TAB: int = 1
    ALLOWED_OPTIONS: Tuple[int] = (HERE, NEW_TAB)
    CANCEL: int = 2
    OPEN_ANYWAY: int = 0


@dataclass(frozen=True)
class SaveOptions:
    SAVE = 1
    SAVE_AS = 2
    SAVE_ALL = 3
    YES = 0
    NO_SAVE = 1
    CANCEL = 2


@dataclass(frozen=True)
class TabActions:
    CLOSE: int = 0
