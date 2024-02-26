from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class FileMenuActionsNames:
    NEW: Final[str] = "New"
    OPEN: Final[str] = "Open..."
    OPEN_FOLDER: Final[str] = "Open Folder..."
    RELOAD_FROM_DISK: Final[str] = "Reload from disk"
    SAVE: Final[str] = "Save"
    SAVE_AS: Final[str] = "Save As..."
    SAVE_COPY_AS: Final[str] = "Save a Copy As..."
    SAVE_ALL: Final[str] = "Save All"
    RENAME: Final[str] = "Rename..."
    CLOSE: Final[str] = "Close"
    CLOSE_ALL: Final[str] = "Close All"
    PRINT: Final[str] = "Print"
    EXIT: Final[str] = "Exit"


@dataclass(frozen=True)
class FileMenuShortcuts:
    NEW: Final[str] = "Ctrl+N"
    OPEN: Final[str] = "Ctrl+O"
    OPEN_FOLDER: Final[str] = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: Final[str] = "Ctrl+R"
    SAVE: Final[str] = "Ctrl+S"
    SAVE_AS: Final[str] = "Ctrl+S"
    SAVE_ALL: Final[str] = "Ctrl+Shift+S"
    CLOSE: Final[str] = "Ctrl+W"
    CLOSE_ALL: Final[str] = "Ctrl+Shift+W"
    EXIT: Final[str] = "Alt+F4"


# ************* EDIT MENU *************


@dataclass(frozen=True)
class EditMenuActionsNames:
    UNDO: Final[str] = "Undo"
    REDO: Final[str] = "Redo"
    CUT: Final[str] = "Cut"
    COPY: Final[str] = "Copy"
    PASTE: Final[str] = "Paste"
    SELECT_ALL: Final[str] = "Select All"


@dataclass(frozen=True)
class EditMenuShortcuts:
    UNDO: Final[str] = "Ctrl+Z"
    REDO: Final[str] = "Ctrl+Shift+Z"
    CUT: Final[str] = "Ctrl+X"
    COPY: Final[str] = "Ctrl+C"
    PASTE: Final[str] = "Ctrl+V"
    SELECT_ALL: Final[str] = "Ctrl+A"


# ************* SEARCH MENU *************


@dataclass(frozen=True)
class SearchMenuActionsNames:
    SEARCH: Final[str] = "Search"
    SEARCH_IN_FILES: Final[str] = "Search in files"
    NEXT: Final[str] = "Search Next"
    BACK: Final[str] = "Search Back"


@dataclass(frozen=True)
class SearchMenuShortcuts:
    SEARCH: Final[str] = "Ctrl+F"
    SEARCH_IN_FILES: Final[str] = "Ctrl+Shift+F"
    NEXT: Final[str] = "F3"
    BACK: Final[str] = "Shift+F3"


# ************* VIEW MENU *************


@dataclass(frozen=True)
class ViewMenuActionsNames:
    TOGGLE_FULL_SCREEN: Final[str] = "Toggle full screen"
    DISTRACTION_FREE_MODE: Final[str] = "Distraction free mode"
    ZOOM: Final[str] = "Zoom"
    ZOOM_IN: Final[str] = "Zoom in"
    ZOOM_OUT: Final[str] = "Zoom out"
    MOVE_CLONE_CURRENT_DOCUMENT: Final[str] = "Move/clone current document"
    TAB: Final[str] = "Tab"
    SUMMARY: Final[str] = "Summary"
    PROJECT_PANELS: Final[str] = "Project panel"
    FOLDER_AS_WORKSPACE: Final[str] = "Folder as workspace"
    DOCUMENT_MAP: Final[str] = "Document Map"
    DOCUMENT_LIST: Final[str] = "Document List"
    FUNCTION_LIST: Final[str] = "Function List"


@dataclass(frozen=True)
class ViewMenuShortcuts:
    TOGGLE_FULL_SCREEN: Final[str] = "F11"
    ZOOM_IN: Final[str] = "Ctrl++"
    ZOOM_OUT: Final[str] = "Ctrl+-"


# ************* ENCODING MENU *************


@dataclass(frozen=True)
class EncodingMenuActionsNames:
    ANSI: Final[str] = "ANSI"
    UTF_8: Final[str] = "UTF-8"
    CONVERT_TO_ANSI: Final[str] = "Convert to ANSI"
    CONVERT_TO_UTF_8: Final[str] = "Convert to UTF-8"


# ************* SETTINGS MENU *************


@dataclass(frozen=True)
class SettingsMenuActionsNames:
    PREFERENCES: Final[str] = "Preferences..."
    STYLE_CONFIGURATOR: Final[str] = "Style Configurator"
    SHORTCUT_MANAGER: Final[str] = "Shortcut Manager"
    IMPORT: Final[str] = "Import"
    PLUGIN: Final[str] = "Plugin"
    STYLE_THEME: Final[str] = "Add Style Theme"


# ************* TOOLS MENU *************


@dataclass(frozen=True)
class ToolsMenuActionsNames:
    BASE_64_ENCODE: Final[str] = "Base 64 Encode"
    BASE_64_DECODE: Final[str] = "Base 64 Decode"


# ************* PLUGINS MENU *************


@dataclass(frozen=True)
class PluginsMenuActionsNames:
    PLUGIN_MANAGER: Final[str] = "Plugins Manager"
    OPEN_PLUGINS_FOLDER: Final[str] = "Open Plugins Folder"


# ************* TERMINAL MENU *************


@dataclass(frozen=True)
class TerminalMenuActionsNames:
    NEW_TERMINAL: Final[str] = "New Terminal"
    SPLIT_TERMINAL: Final[str] = "Split Terminal"


@dataclass(frozen=True)
class TerminalMenuShortcuts:
    NEW_TERMINAL: Final[str] = "Ctrl+Shift+T"
    SPLIT_TERMINAL: Final[str] = "Ctrl+Shift+D"


# ************* HELP MENU *************


@dataclass(frozen=True)
class HelpMenuActionsNames:
    SHOW_ALL_COMMANDS: Final[str] = "Show All Commands"
    DOCUMENTATION: Final[str] = "Documentation"
    TIPS_AND_TRICKS: Final[str] = "Tips and tricks"
    REPORT_ISSUE: Final[str] = "Report Issue"
    CHECK_FOR_UPDATES: Final[str] = "Check for updates..."


@dataclass(frozen=True)
class HelpMenuShortcuts:
    SHOW_ALL_COMMANDS: Final[str] = "Ctrl+Shift+P"
