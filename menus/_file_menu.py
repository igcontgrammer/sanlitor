import os
from enum import Enum, auto
from functools import partial
from typing import Final

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog

from common.config_action import config
from constants import OpenFileOptions
from editor import Editor
from extensions import available_extensions, get_extensions_list
from messages import Messages, MessageTypes, show_system_error_message
from paths import Paths
from tab_manager import Tab
from utils import filename_is_valid

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import FileMenuActionsNames, FileMenuShortcuts

_DEFAULT_NEW_FILENAME: Final[str] = "new.txt"
_STARTING_NEW_FILE_COUNTER: Final[int] = 1


def get_content_from_file(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        error_message = f"Error found at: {e.__class__.__name__}. Message: {e}"
        print(error_message)
        return ""

def has_opened_file(path: str) -> bool:
    return len(path) > 0


def get_new_filename(home, tab: Tab) -> str:
    from home import Home

    if not isinstance(home, Home):
        raise TypeError("The home parameter must be an instance of Home")
    files_worked_on = home.storage_manager.worked_files
    if _DEFAULT_NEW_FILENAME not in files_worked_on:
        return _DEFAULT_NEW_FILENAME
    name = ""
    for i in range(_STARTING_NEW_FILE_COUNTER, tab.count()):
        name = f"new({i}).txt"
        if name in tab.worked_files or name in files_worked_on:
            continue
        else:
            break
    print(f"new name: {name}")
    return name


class FileMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        self.setTitle(SectionsNames.FILE)
        from home import Home

        self._home: Home = home
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

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
            status_tip="Open a file",
            shortcut=FileMenuShortcuts.OPEN,
            method=self._open_file,
        )
        self.addAction(open_file_action)

    def _new_file_action(self) -> None:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        config(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuShortcuts.NEW,
            method=self._new_file,
        )
        self.addAction(new_file_action)

    def _save_file_action(self) -> None:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        config(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuShortcuts.SAVE,
            method=self._save_file,
        )
        self.addAction(save_file_action)

    def _save_as_action(self) -> None:
        old_name = self._home.tab_manager.tabText(self._home.tab_manager.currentIndex())
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        config(
            action=save_as_action,
            status_tip="Save file as...",
            shortcut=FileMenuShortcuts.SAVE_AS,
            method=partial(self._save_as, old_name),
        )
        self.addAction(save_as_action)

    def _save_all_files_action(self) -> None:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        config(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuShortcuts.SAVE_ALL,
            method=self._save_all_files,
        )
        self.addAction(save_all_files_action)

    def _close_file_action(self) -> None:
        close_file_action = QAction(FileMenuActionsNames.CLOSE, self)
        config(
            action=close_file_action,
            status_tip="Close a file",
            shortcut=FileMenuShortcuts.CLOSE,
            method=None,
        )
        self.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        config(
            action=close_all_files_action,
            status_tip="Close all files",
            shortcut=FileMenuShortcuts.CLOSE_ALL,
            method=None,
        )
        self.addAction(close_all_files_action)

    def _print_action(self) -> None:
        print_action = QAction(FileMenuActionsNames.PRINT, self)
        config(
            action=print_action,
            status_tip="Print a file",
            shortcut="",
            method=self._print_file,
        )
        self.addAction(print_action)

    def _exit_action(self) -> None:
        exit_action = QAction(FileMenuActionsNames.EXIT, self)
        config(
            action=exit_action,
            status_tip="Exit the application",
            shortcut=FileMenuShortcuts.EXIT,
            method=self._exit_application,
        )
        self.addAction(exit_action)

    # ************* SLOTS *************

    @Slot()
    def _open_file(self) -> None:
        file = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            dir=os.path.expanduser("~"),
        )
        if not has_opened_file(path=file[0]):
            return None
        path = file[0]
        extension_detected = os.path.splitext(path)[1]
        if extension_detected not in available_extensions():
            show_system_error_message(
                self._home, content="La extensión de este archivo no es permitida."
            )
            return None

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

    @Slot()
    def _new_file(self) -> None:
        tab = self._home.tab_manager
        tab.new()

    @Slot()
    def _save_file(self) -> None:
        # TODO: vamos a trabajar con el save file
        tab_manager = self._home.tab_manager
        index = tab_manager.currentIndex()
        file_name = tab_manager.tabText(index)
        exists = self._home.storage_manager.path_exists(file_name)
        if not exists:
            msg = Messages(
                parent=self._home,
                content=f"Tuvimos problemas para guardar el archivo {file_name}. Asegúrese que el nombre o la ubicación sean correctos.",
                first_button_title="De acuerdo",
                message_type=MessageTypes.CRITICAL
            )
            msg.run()
            return None
        editor = tab_manager.widget(index)
        if not isinstance(editor, Editor):
            print("editor is not an instance of Editor")
            return None
        content = editor.toPlainText()
        status = self._home.storage_manager.save_from_file_name(file_name, content)
        if status[0] is False:
            print(status[1])
            error_msg = Messages(
                parent=self._home,
                content="Ocurrió un error inesperado. Por favor inténtelo de nuevo.",
                first_button_title="De acuerdo",
                message_type=MessageTypes.CRITICAL
            )
            error_msg.run()
            return None

    @Slot()
    def _save_as(self, old_name: str) -> None:
        pass

    @Slot()
    def _save_all_files(self) -> None:
        print("Saving all files...")

    @Slot()
    def _print_file(self) -> None:
        print("Printing a file...")

    @Slot()
    def _exit_application(self) -> None:
        print("Exiting the application...")

    # ************* SLOTS FUNCTIONS *************

    def _when_opening(self, tab_manager: Tab, path: str, here: bool = False) -> None:
        # TODO: implementar el manejo de extensiones y su sintaxis
        editor = tab_manager.editor
        if editor.has_changes:
            msg = Messages(
                parent=self._home,
                content="Se detectaron cambios en este archivo ¿desea abrir de todas formas?",
                first_button_title="Abrir",
                message_type=MessageTypes.WARNING,
            )
            if msg.run() != OpenFileOptions.OPEN_ANYWAY:
                return
        tab_manager.set_is_open_mode(True)
        file_name = os.path.basename(path)
        if here:
            tab_manager.change_tab_name(file_name)
            tab_manager.add_content_to_current_tab(content=get_content_from_file(path))
        else:
            tab_manager.new()
        editor.has_changes = False
        tab_manager.set_is_open_mode(False)
        tab_manager.add_to_loaded_files(file_name)
        extension = os.path.splitext(path)[1]
        editor.set_syntax(extension)

    def _get_open_file_option(self) -> int:
        msg = Messages(
            parent=self._home,
            title="Abrir Archivo",
            content="¿Dónde desea abrir el archivo?",
            first_button_title="Aquí",
            message_type=MessageTypes.QUESTION,
        )
        msg.add_button("En una nueva pestaña")
        option_selected = msg.run()
        if option_selected not in OpenFileOptions.ALLOWED_OPTIONS:
            return OpenFileOptions.CANCEL
        return OpenFileOptions.HERE if option_selected == 0 else OpenFileOptions.NEW_TAB

    def _get_path_from_save_dialog(self, title: str) -> str:
        file = QFileDialog.getSaveFileName(
            self,
            title,
            filter=get_extensions_list(),
            dir=os.path.expanduser("~"),
        )
        path = file[0]
        return path if path is not None else ""
