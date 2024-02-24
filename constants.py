from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class OpenFileOptions:
    HERE: Final[int] = 0
    NEW_TAB: Final[int] = 1
    OVERWRITE: Final[int] = 0
