import os
from typing import Final

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog

from common.config_action import config
from constants import OpenFileOptions
from editor import Editor
from extensions import available_extensions, get_extensions_list
from messages import Messages, MessageTypes
from tab_manager import Tab
from utils import filename_is_valid

from . import QAction, QMenu, SectionsNames, Slot
from . import QCoreApplication as CoreApp
from ._menus_constants import FileMenuActionsNames, FileMenuShortcuts


def get_content_from_file(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        error_message = f"Error found at: {e.__class__.__name__}. Message: {e}"
        print(error_message)
        return ""


def has_opened_file(filepath: str) -> bool:
    return len(filepath) > 0


_DEFAULT_NEW_FILENAME: Final[str] = "new.txt"
_STARTING_NEW_FILE_COUNTER: Final[int] = 1


class FileMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        self._menu = QMenu(SectionsNames.FILE)
        self._home = home
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._menu

    def _create_actions(self) -> None:
        self._open_file_action()
        self._new_file_action()
        self._save_file_action()
        self._save_as_action()
        self._save_all_files_action()
        self._close_file_action()
        self._close_all_files_action()
        self._print_action()
        self._exit_action()

    # ************* ACTIONS *************

    def _open_file_action(self) -> None:
        open_file_action = QAction(FileMenuActionsNames.OPEN, self)
        config(
            action=open_file_action,
            status_tip=CoreApp.translate("file_menu", "Open a file"),
            shortcut=FileMenuShortcuts.OPEN,
            method=self._open_file,
        )
        self._menu.addAction(open_file_action)

    def _new_file_action(self) -> None:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        config(
            action=new_file_action,
            status_tip=CoreApp.translate("file_menu", "Create a new file"),
            shortcut=FileMenuShortcuts.NEW,
            method=self._new_file,
        )
        self._menu.addAction(new_file_action)

    def _save_file_action(self) -> None:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        config(
            action=save_file_action,
            status_tip=CoreApp.translate("file_menu", "Save a file"),
            shortcut=FileMenuShortcuts.SAVE,
            method=self._save_file,
        )
        self._menu.addAction(save_file_action)

    def _save_as_action(self) -> None:
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        config(
            action=save_as_action,
            status_tip=CoreApp.translate("file_menu", "Save a file as..."),
            shortcut=FileMenuShortcuts.SAVE_AS,
            method=self._save_file,
        )
        self._menu.addAction(save_as_action)

    def _save_all_files_action(self) -> None:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        config(
            action=save_all_files_action,
            status_tip=CoreApp.translate("file_menu", "Save all files"),
            shortcut=FileMenuShortcuts.SAVE_ALL,
            method=self._save_all_files,
        )
        self._menu.addAction(save_all_files_action)

    def _close_file_action(self) -> None:
        close_file_action = QAction(FileMenuActionsNames.CLOSE, self)
        config(
            action=close_file_action,
            status_tip=CoreApp.translate("file_menu", "Close a file"),
            shortcut=FileMenuShortcuts.CLOSE,
            method=None,
        )
        self._menu.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        config(
            action=close_all_files_action,
            status_tip=CoreApp.translate("file_menu", "Close all files"),
            shortcut=FileMenuShortcuts.CLOSE_ALL,
            method=None,
        )
        self._menu.addAction(close_all_files_action)

    def _print_action(self) -> None:
        print_action = QAction(FileMenuActionsNames.PRINT, self)
        config(
            action=print_action,
            status_tip=CoreApp.translate("file_menu", "Print a file"),
            shortcut="",
            method=self._print_file,
        )
        self._menu.addAction(print_action)

    def _exit_action(self) -> None:
        exit_action = QAction(FileMenuActionsNames.EXIT, self)
        config(
            action=exit_action,
            status_tip=CoreApp.translate("file_menu", "Exit the application"),
            shortcut=FileMenuShortcuts.EXIT,
            method=self._exit_application,
        )
        self._menu.addAction(exit_action)

    @Slot()
    def _open_file(self) -> None:
        file = QFileDialog.getOpenFileName(
            self,
            CoreApp.translate("file_menu", "Abrir archivo"),
            dir=os.path.expanduser("~"),
        )
        if not has_opened_file(filepath=file[0]):
            return None
        path = file[0]
        extension_detected = os.path.splitext(path)[1]
        if extension_detected not in available_extensions():
            self.show_extension_not_allowed_message()
            return None
        from home import Home

        self._home: Home
        tab_manager = self._home.tab_manager
        filename = os.path.basename(path)
        if tab_manager.already_opened(filename):
            tab_manager.move(filename)
            return
        match self._get_open_file_option():
            case OpenFileOptions.HERE:
                self._when_opening(tab_manager, path, here=True)
            case OpenFileOptions.NEW_TAB:
                self._when_opening(tab_manager, path)
            case OpenFileOptions.CANCEL:
                return
            case _:
                return

    # ************* SLOTS *************

    @Slot()
    def _new_file(self) -> None:
        from home import Home

        self._home: Home
        tab = self._home.tab_manager
        tab.new(self.get_new_filename(tab))

    @Slot()
    def _save_file(self) -> None:
        # TODO: obtener el current tab
        from home import Home

        self._home: Home
        tab_manager = self._home.tab_manager
        current_index = tab_manager.current_index
        editor = tab_manager.widget(current_index)
        if not isinstance(editor, Editor):
            raise TypeError("editor is not an Editor object")
        content = editor.toPlainText()
        file = QFileDialog.getSaveFileName(
            self,
            CoreApp.translate("file_menu", "Guardar archivo"),
            filter=get_extensions_list(),
            dir=os.path.expanduser("~"),
        )
        filename = os.path.basename(file[0])
        if not filename_is_valid(filename):
            msg = Messages(
                parent=self._home,
                content='El nombre del archivo no puede contener los siguientes caracteres: /, \\, :, *, ?, ", <, >, |',
                first_button_title="Aceptar",
                type=MessageTypes.CRITICAL,
            )
            msg.run()
        with open(file[0], "w") as file:
            file.write(content)
        tab_manager.setTabText(current_index, filename)
        editor.has_changes = False
        tab_manager.setTabIcon(current_index, QIcon())

    @Slot()
    def _save_all_files(self) -> None:
        print("Saving all files...")
        pass

    @Slot()
    def _print_file(self) -> None:
        print("Printing a file...")
        pass

    @Slot()
    def _exit_application(self) -> None:
        print("Exiting the application...")
        pass

    # ************* SLOTS FUNCTIONS *************

    def show_extension_not_allowed_message(self) -> None:
        msg = Messages(
            parent=self._home,
            content="La extensión de este archivo no es permitida.",
            first_button_title="AceptarDe acuerdoDe acuerdo",
            type=MessageTypes.CRITICAL,
        )
        msg.run()

    def get_new_filename(self, tab: Tab) -> str:
        if _DEFAULT_NEW_FILENAME in tab.loaded_files:
            for i in range(_STARTING_NEW_FILE_COUNTER, tab.tabs_count):
                name = f"new({i}).txt"
                if name in tab.loaded_files:
                    continue
                return name
        return _DEFAULT_NEW_FILENAME

    def _when_opening(self, tab_manager: Tab, path: str, here: bool = False) -> None:
        editor = tab_manager.editor
        if editor.has_changes:
            msg = Messages(
                parent=self._home,
                content="Se detectaron cambios en este archivo ¿desea abrir de todas formas?",
                first_button_title="Abrir",
                type=MessageTypes.WARNING,
            )
            if msg.run() != OpenFileOptions.OPEN_ANYWAY:
                return
        tab_manager.set_is_open_mode(True)
        filename = os.path.basename(path)
        if here:
            tab_manager.change_tab_name(filename)
            tab_manager.add_content_to_current_tab(content=get_content_from_file(path))
        else:
            tab_manager.new(filename, get_content_from_file(path))
        editor.has_changes = False
        tab_manager.set_is_open_mode(False)
        tab_manager.add_to_loaded_files(filename)

    def _get_open_file_option(self) -> int:
        msg = Messages(
            parent=self._home,
            title="Abrir Archivo",
            content="¿Dónde desea abrir el archivo?",
            first_button_title="Aquí",
            type=MessageTypes.QUESTION,
        )
        msg.add_button("En una nueva pestaña")
        option_selected = msg.run()
        if option_selected not in OpenFileOptions.ALLOWED_OPTIONS:
            return OpenFileOptions.CANCEL
        return OpenFileOptions.HERE if option_selected == 0 else OpenFileOptions.NEW_TAB
