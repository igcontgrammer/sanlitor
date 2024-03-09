from dataclasses import dataclass


@dataclass(frozen=True)
class FileMenuActionsNames:
    RENAME: str = "Rename"
    NEW: str = "New"
    OPEN: str = "Open..."
    OPEN_FOLDER: str = "Open Folder..."
    RELOAD_FROM_DISK: str = "Reload from disk"
    SAVE: str = "Save"
    SAVE_AS: str = "Save As..."
    SAVE_COPY_AS: str = "Save a Copy As..."
    SAVE_ALL: str = "Save All"
    RENAME: str = "Rename..."
    CLOSE: str = "Close"
    CLOSE_ALL: str = "Close All"
    PRINT: str = "Print"
    EXIT: str = "Exit"


@dataclass(frozen=True)
class FileMenuShortcuts:
    NEW: str = "Ctrl+N"
    OPEN: str = "Ctrl+O"
    OPEN_FOLDER: str = "Ctrl+Shift+O"
    RELOAD_FROM_DISK: str = "Ctrl+R"
    SAVE: str = "Ctrl+S"
    SAVE_AS: str = "Ctrl+S"
    SAVE_ALL: str = "Ctrl+Shift+S"
    CLOSE: str = "Ctrl+W"
    CLOSE_ALL: str = "Ctrl+Shift+W"
    EXIT: str = "Alt+F4"


# ************* EDIT MENU *************


@dataclass(frozen=True)
class EditMenuActionsNames:
    UNDO: str = "Undo"
    REDO: str = "Redo"
    CUT: str = "Cut"
    COPY: str = "Copy"
    PASTE: str = "Paste"
    SELECT_ALL: str = "Select All"


@dataclass(frozen=True)
class EditMenuShortcuts:
    UNDO: str = "Ctrl+Z"
    REDO: str = "Ctrl+Shift+Z"
    CUT: str = "Ctrl+X"
    COPY: str = "Ctrl+C"
    PASTE: str = "Ctrl+V"
    SELECT_ALL: str = "Ctrl+A"


# ************* SEARCH MENU *************


@dataclass(frozen=True)
class SearchMenuActionsNames:
    SEARCH: str = "Search"
    SEARCH_IN_FILES: str = "Search in files"
    NEXT: str = "Search Next"
    BACK: str = "Search Back"


@dataclass(frozen=True)
class SearchMenuShortcuts:
    SEARCH: str = "Ctrl+F"
    SEARCH_IN_FILES: str = "Ctrl+Shift+F"
    NEXT: str = "F3"
    BACK: str = "Shift+F3"


# ************* VIEW MENU *************


@dataclass(frozen=True)
class ViewMenuActionsNames:
    TOGGLE_FULL_SCREEN: str = "Toggle full screen"
    DISTRACTION_FREE_MODE: str = "Distraction free mode"
    ZOOM: str = "Zoom"
    ZOOM_IN: str = "Zoom in"
    ZOOM_OUT: str = "Zoom out"
    MOVE_CLONE_CURRENT_DOCUMENT: str = "Move/clone current document"
    TAB: str = "Tab"
    SUMMARY: str = "Summary"
    PROJECT_PANELS: str = "Project panel"
    FOLDER_AS_WORKSPACE: str = "Folder as workspace"
    DOCUMENT_MAP: str = "Document Map"
    DOCUMENT_LIST: str = "Document List"
    FUNCTION_LIST: str = "Function List"


@dataclass(frozen=True)
class ViewMenuShortcuts:
    TOGGLE_FULL_SCREEN: str = "F11"
    ZOOM_IN: str = "Ctrl++"
    ZOOM_OUT: str = "Ctrl+-"


# ************* ENCODING MENU *************


@dataclass(frozen=True)
class EncodingMenuActionsNames:
    ANSI: str = "ANSI"
    UTF_8: str = "UTF-8"
    CONVERT_TO_ANSI: str = "Convert to ANSI"
    CONVERT_TO_UTF_8: str = "Convert to UTF-8"


# ************* SETTINGS MENU *************


@dataclass(frozen=True)
class SettingsMenuActionsNames:
    PREFERENCES: str = "Preferences..."
    STYLE_CONFIGURATOR: str = "Style Configurator"
    SHORTCUT_MANAGER: str = "Shortcut Manager"
    IMPORT: str = "Import"
    PLUGIN: str = "Plugin"
    STYLE_THEME: str = "Add Style Theme"


# ************* TOOLS MENU *************


@dataclass(frozen=True)
class ToolsMenuActionsNames:
    BASE_64_ENCODE: str = "Base 64 Encode"
    BASE_64_DECODE: str = "Base 64 Decode"


# ************* PLUGINS MENU *************


@dataclass(frozen=True)
class PluginsMenuActionsNames:
    PLUGIN_MANAGER: str = "Plugins Manager"
    OPEN_PLUGINS_FOLDER: str = "Open Plugins Folder"


# ************* TERMINAL MENU *************


@dataclass(frozen=True)
class TerminalMenuActionsNames:
    NEW_TERMINAL: str = "New Terminal"
    SPLIT_TERMINAL: str = "Split Terminal"


@dataclass(frozen=True)
class TerminalMenuShortcuts:
    NEW_TERMINAL: str = "Ctrl+Shift+T"
    SPLIT_TERMINAL: str = "Ctrl+Shift+D"


# ************* HELP MENU *************


@dataclass(frozen=True)
class HelpMenuActionsNames:
    SHOW_ALL_COMMANDS: str = "Show All Commands"
    DOCUMENTATION: str = "Documentation"
    TIPS_AND_TRICKS: str = "Tips and tricks"
    REPORT_ISSUE: str = "Report Issue"
    CHECK_FOR_UPDATES: str = "Check for updates..."


@dataclass(frozen=True)
class HelpMenuShortcuts:
    SHOW_ALL_COMMANDS: str = "Ctrl+Shift+P"
