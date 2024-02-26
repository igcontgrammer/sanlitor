from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class OpenFileOptions:
    HERE: int = 0
    NEW_TAB: int = 1
    ALLOWED_OPTIONS: Tuple[int, int] = (HERE, NEW_TAB)
    CANCEL: int = 2


@dataclass(frozen=True)
class TabActions:
    CLOSE: int = 0
