from dataclasses import dataclass


@dataclass(frozen=True)
class Shortcuts:
    NEW: str = "Ctrl+N"
    OPEN: str = "Ctrl+O"
    OPEN_FOLDER: str = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: str = "Ctrl+R"
    SAVE: str = "Ctrl+S"
    SAVE_AS: str = "Ctrl+Shift+S"
    SAVE_ALL: str = "Ctrl+Shift+A"
    PRINT: str = ""
    SHOW_TERMINAL: str = "Ctrl+`"
    CLOSE: str = "Ctrl+W"
    CLOSE_ALL: str = "Ctrl+Shift+W"
    EXIT: str = "Alt+F4"
