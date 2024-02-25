from dataclasses import dataclass
from typing import Final, Tuple


@dataclass(frozen=True)
class OpenFileOptions:
    HERE: Final[int] = 0
    NEW_TAB: Final[int] = 1
    ALLOWED_OPTIONS: Tuple[int] = (HERE, NEW_TAB)
    CANCEL: Final[int] = 2


@dataclass(frozen=True)
class TabActions:
    CLOSE: Final[int] = 0
