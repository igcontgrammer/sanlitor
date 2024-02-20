from dataclasses import dataclass


@dataclass(frozen=True)
class SectionsNames:
    FILE: str = "File"
    EDIT: str = "Edit"
    SEARCH: str = "Search"
    VIEW: str = "View"
    ENCODING: str = "Encoding"
    LANGUAGE: str = "Language"
    SETTINGS: str = "Settings"
    TOOLS: str = "Tools"
    PLUGINS: str = "Plugins"
    TERMINAL: str = "Terminal"
    HELP: str = "Help"
