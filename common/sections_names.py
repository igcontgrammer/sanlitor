from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class SectionsNames:
    FILE: Final[str] = "File"
    EDIT: Final[str] = "Edit"
    SEARCH: Final[str] = "Search"
    VIEW: Final[str] = "View"
    ENCODING: Final[str] = "Encoding"
    LANGUAGE: Final[str] = "Language"
    SETTINGS: Final[str] = "Settings"
    TOOLS: Final[str] = "Tools"
    PLUGINS: Final[str] = "Plugins"
    TERMINAL: Final[str] = "Terminal"
    HELP: Final[str] = "Help"
