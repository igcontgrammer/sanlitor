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
from tab_manager import Tab
from utils import filename_is_valid

from . import QAction
from . import QCoreApplication as CoreApp
from . import QMenu, SectionsNames, Slot
from ._menus_constants import FileMenuActionsNames, FileMenuShortcuts

_DEFAULT_NEW_FILENAME: Final[str] = "new.txt"
_STARTING_NEW_FILE_COUNTER: Final[int] = 1


class SaveOptions(Enum):
    SAVE = auto()
    SAVE_AS = auto()
    SAVE_ALL = auto()


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


def get_new_filename(h, tab: Tab) -> str:
    from home import Home

    h: Home
    files_worked_on = h.storage_manager.get_last_files_worked()
    if _DEFAULT_NEW_FILENAME not in files_worked_on:
        return _DEFAULT_NEW_FILENAME
    for i in range(_STARTING_NEW_FILE_COUNTER, tab.count()):
        name = f"new({i}).txt"
        if name in tab.loaded_files or name in files_worked_on:
            continue
        return name


def get_save_dialog_title(option: SaveOptions) -> str:
    match option:
        case SaveOptions.SAVE:
            return "Guardar"
        case SaveOptions.SAVE_AS:
            return "Guardar como"
        case SaveOptions.SAVE_ALL:
            return "Guardar todo"
        case _:
            return ""


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
        old_name = self._home.tab_manager.tabText(self._home.tab_manager.currentIndex())
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        config(
            action=save_as_action,
            status_tip=CoreApp.translate("file_menu", "Save a file as..."),
            shortcut=FileMenuShortcuts.SAVE_AS,
            method=partial(self._save_as, old_name),
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
            show_system_error_message(
                self._home, content="La extensión de este archivo no es permitida."
            )
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
        tab = self._home.tab_manager
        tab.new(get_new_filename(h=self._home, tab=tab), False)

    @Slot()
    def _save_file(self) -> None:
        from home import Home

        self._home: Home
        tab_manager = self._home.tab_manager
        index = tab_manager.currentIndex()
        editor = tab_manager.widget(index)
        if not isinstance(editor, Editor):
            return None
        file_name = tab_manager.tabText(index)
        if editor.has_changes and self._home.is_registered(file_name):
            content = editor.toPlainText()
            save_status = self._home.storage_manager.save_changes(
                file_name=file_name, value=content, old_file_name=""
            )
            if save_status[0] is False:
                show_system_error_message(self._home, save_status[1])
                return None
            editor.has_changes = False
            tab_manager.setTabIcon(index, QIcon())
            return None
        path = self._get_path_from_save_dialog(SaveOptions.SAVE)
        if not len(path) > 0:
            return
        file_name_from_path = os.path.basename(path)
        if not filename_is_valid(os.path.basename(file_name_from_path)):
            error_message = (
                'El nombre del archivo no puede contener los siguientes caracteres: /, \\, :, *, ?, ", <, '
                ">, |"
            )
            show_system_error_message(self._home, error_message)
            return None
        file_name = os.path.basename(path)
        content = editor.toPlainText()
        with open(path, "w") as file:
            file.write(content)
        save_status = self._home.storage_manager.save_changes(path=path)
        if save_status[0] is False:
            show_system_error_message(
                self._home, "No se pudo guardar el archivo. Inténtelo de nuevo"
            )
            return None
        tab_manager.setTabText(index, file_name)
        editor.has_changes = False
        tab_manager.setTabIcon(index, QIcon())

    @Slot()
    def _save_as(self, old_name: str) -> None:
        # TODO: guardar con la extensión que elija el usuario. Esto implica trabajar con la sintaxis de las extensiones
        from home import Home

        self._home: Home
        tab_manager = self._home.tab_manager
        index = tab_manager.currentIndex()
        editor = tab_manager.widget(index)
        if not isinstance(editor, Editor):
            show_system_error_message(self._home)
            return None
        file = QFileDialog.getSaveFileName(
            self,
            CoreApp.translate("file_menu", "Guardar Archivo Como..."),
            filter=get_extensions_list(),
            dir=os.path.expanduser("~"),
        )
        path = file[0]
        has_saved = len(path) > 0
        if not has_saved:
            return
        file_name = os.path.basename(path)
        if not filename_is_valid(file_name):
            error_message = (
                'El nombre del archivo no puede contener los siguientes caracteres: /, \\, :, *, ?, ", <, '
                ">, |"
            )
            show_system_error_message(self._home, error_message)
            return
        content = editor.toPlainText()
        with open(path, "w") as write_file:
            write_file.write(content)
        if self._home.storage_manager.save_changes(path=path, old_file_name=old_name):
            tab_manager.setTabText(index, file_name)
            editor.has_changes = False
            tab_manager.setTabIcon(index, QIcon())
        else:
            error_message = "No se pudo guardar el archivo. Inténtelo de nuevo."
            show_system_error_message(self._home, error_message)

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
        extension = os.path.splitext(path)[1]
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
            tab_manager.new(file_name, False, get_content_from_file(path))
        editor.has_changes = False
        tab_manager.set_is_open_mode(False)
        tab_manager.add_to_loaded_files(file_name)

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

    def _get_path_from_save_dialog(self, option: SaveOptions) -> str:
        file = QFileDialog.getSaveFileName(
            self,
            CoreApp.translate("file_menu", get_save_dialog_title(option)),
            filter=get_extensions_list(),
            dir=os.path.expanduser("~"),
        )
        path = file[0]
        return path if path is not None else ""
