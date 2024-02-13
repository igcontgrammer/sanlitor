from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Shortcuts:
    NEW: Final[str] = "Ctrl+N"
    OPEN: Final[str] = "Ctrl+O"
    OPEN_FOLDER: Final[str] = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: Final[str] = "Ctrl+R"
    SAVE: Final[str] = "Ctrl+S"
    SAVE_AS: Final[str] = "Ctrl+Shift+S"
    SAVE_ALL: Final[str] = "Ctrl+Shift+A"
    PRINT: Final[str] = ""
    SHOW_TERMINAL: Final[str] = "Ctrl+`"
    CLOSE: Final[str] = "Ctrl+W"
    CLOSE_ALL: Final[str] = "Ctrl+Shift+W"
    EXIT: Final[str] = "Alt+F4"
    

