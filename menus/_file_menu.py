import os
from typing import Final

from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon

from common.config_action import config
from constants import AppMode, FileNames, OpenFileOptions, SaveOptions
from editor import Editor
from extensions import available_extensions, get_extensions_list
from messages import Messages, MessageTypes, show_system_error_message
from storage_manager import save_from_path
from tab_manager import Tab
from tree import Tree
from utils import get_extension_from_path, has_selected
from pathlib import Path
from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import FileMenuActionsNames, FileMenuShortcuts

DEFAULT_FILE_NAME: Final[str] = "Untitled.txt"


def get_content_from_file(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        error_message = f"Error found at: {e.__class__.__name__}. Message: {e}"
        print(error_message)
        return ""


class FileMenu(QMenu):
    def __init__(self, home):
        super().__init__()
        self.setTitle(SectionsNames.FILE)
        from home import Home

        self._home: Home = home
        self._tab = self._home.tab
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

    def _create_actions(self) -> None:
        self._rename_action()
        self._open_file_action()
        self._open_folder_action()
        self._new_file_action()
        self._save_file_action()
        self._save_as_action()
        self._save_all_files_action()
        self._close_file_action()
        self._close_all_files_action()

    # ************* ACTIONS *************

    def _rename_action(self) -> None:
        rename_action = QAction(FileMenuActionsNames.RENAME, self)
        config(
            action=rename_action,
            status_tip="Rename file",
            shortcut="",
            method=self._rename,
        )
        self.addAction(rename_action)

    def _open_file_action(self) -> None:
        open_file_action = QAction(FileMenuActionsNames.OPEN, self)
        config(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuShortcuts.OPEN,
            method=self._open_file,
        )
        self.addAction(open_file_action)

    def _open_folder_action(self) -> None:
        open_folder_action = QAction(FileMenuActionsNames.OPEN_FOLDER, self)
        config(
            action=open_folder_action,
            status_tip="Open a folder",
            shortcut="",
            method=self._open_folder,
        )
        self.addAction(open_folder_action)

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
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        config(
            action=save_as_action,
            status_tip="Save file as...",
            shortcut=FileMenuShortcuts.SAVE_AS,
            method=self._save_as,
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
            method=self._close,
        )
        self.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        config(
            action=close_all_files_action,
            status_tip="Close all files",
            shortcut=FileMenuShortcuts.CLOSE_ALL,
            method=self._close_all,
        )
        self.addAction(close_all_files_action)

    # ************* SLOTS ************

    def _open_file(self) -> None:
        file = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            dir=os.path.expanduser("~"),
        )
        if not has_selected(file[0]):
            return None
        path = Path(file[0])
        if path.suffix not in available_extensions():
            show_system_error_message(
                self._home, content="La extensión de este archivo no es permitida."
            )
            return None
        if self._tab.already_opened(path.name):
            self._tab.move(path.name)
            return
        if self._tab.has_one_tab:
            self._when_opening(self._tab, path, here=True)
            return
        else:
            option = self._get_open_file_option()
            match option:
                case OpenFileOptions.HERE:
                    self._when_opening(self._tab, path, here=True)
                case OpenFileOptions.NEW_TAB:
                    self._when_opening(self._tab, path)
                case OpenFileOptions.CANCEL:
                    return
                case _:
                    return

    @Slot()
    def _open_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "Abrir carpeta",
            dir=os.path.expanduser("~"),
        )
        if not has_selected(path):
            return None
        try:
            tree = Tree(self._home, Path(path))
            self._home.change_central(AppMode.TREE, tree.get())
        except Exception as e:
            show_system_error_message(self._home, str(e))

    @Slot()
    def _rename(self) -> None:
        old_name = self._tab.tabText(self._tab.currentIndex())
        file = self._get_path_from_save_dialog("Renombrar Archivo")
        path = file[0]
        if not has_selected(path):
            return
        new_file_name = os.path.basename(path)
        ok, error_msg = self._home.storage_manager.rename(old_name, new_file_name)
        if not ok:
            print(error_msg)
            return
        self._tab.setTabText(self._tab.currentIndex(), new_file_name)

    @Slot()
    def _new_file(self) -> None:
        tab = self._tab
        tab.new()

    def save_on_default(self) -> None:
        index = self._tab.currentIndex()
        editor = self._tab.widget(index)
        if not isinstance(editor, Editor):
            raise ValueError("editor is not an instance of Editor")
        file = QFileDialog.getSaveFileName(
            parent=self._home,
            caption="Nuevo archivo",
            dir=os.path.expanduser("~"),
            filter=get_extensions_list(),
        )
        path = file[0]
        if not has_selected(path):
            return
        content = editor.toPlainText()
        ok, error_msg = save_from_path(path, content)
        if not ok:
            raise ValueError(error_msg)
        ok, error_msg = self._home.storage_manager.add(path)
        if not ok:
            raise ValueError(error_msg)
        self._tab.setTabText(index, os.path.basename(path))
        editor.has_changes = False

    @Slot()
    def _save_file(self) -> None:
        index = self._tab.currentIndex()
        file_name = self._tab.tabText(index)
        try:
            if file_name == DEFAULT_FILE_NAME:
                self.save_on_default()
                return
            exists = self._home.storage_manager.file_exists(file_name)
            if not exists:
                raise FileNotFoundError(f"the file: {file_name} not exists")
            editor = self._tab.widget(index)
            if not isinstance(editor, Editor):
                raise ValueError("editor is not an instance of Editor")
            content = editor.toPlainText()
            status = self._home.storage_manager.save_from_file_name(file_name, content)
            if status[0] is False:
                raise ValueError("not saved from file_name")
            editor.has_changes = False
            self._tab.set_normal()
        except ValueError as ve:
            show_system_error_message(parent=self._home, content=str(ve))
            return None
        except FileNotFoundError as fnf:
            show_system_error_message(parent=self._home, content=str(fnf))
        except Exception as e:
            show_system_error_message(parent=self._home, content=str(e))
            return None

    @Slot()
    def _save_as(self) -> None:
        editor = self._tab.widget(self._tab.currentIndex())
        if not isinstance(editor, Editor):
            show_system_error_message(self._home, "editor is not an instance of Editor")
            return None
        file = QFileDialog.getSaveFileName(
            parent=self._home,
            caption="Guardar como...",
            dir=os.path.expanduser("~"),
            filter=get_extensions_list(),
        )
        path = file[0]
        if not has_selected(path):
            return None
        old_name = self._tab.tabText(self._tab.currentIndex())
        new_name = os.path.basename(path)
        status = self._home.storage_manager.rename(old_name, new_name)
        if status[0] is False:
            return
        editor.set_syntax(get_extension_from_path(path))
        self._tab.set_normal(new_name)
        editor.has_changes = False

    @Slot()
    def _save_all_files(self) -> None:
        paths_with_errors = []
        try:
            for i in range(self._tab.count()):
                editor = self._tab.widget(i)
                if not isinstance(editor, Editor):
                    continue
                content = editor.toPlainText()
                file_name = self._tab.tabText(i)
                path = self._home.storage_manager.get_path_from_file_name(file_name)
                ok, error_msg = save_from_path(path, content)
                if not ok:
                    paths_with_errors.append(str(path))
                    continue
                editor.has_changes = False
                self._tab.setTabIcon(i, QIcon())
            if len(paths_with_errors) > 0:
                print(paths_with_errors)
        except ValueError as ve:
            show_system_error_message(parent=self._home, content=str(ve))
        except FileNotFoundError as fnf:
            show_system_error_message(parent=self._home, content=str(fnf))
        except Exception as e:
            show_system_error_message(parent=self._home, content=str(e))

    @Slot()
    def _close(self) -> None:
        editor = self._tab.widget(self._tab.currentIndex())
        if not isinstance(editor, Editor):
            print("editor is not an instance of Editor")
            return None
        file_name = self._tab.tabText(self._tab.currentIndex())
        if editor.has_changes:
            msg = Messages(
                parent=self._home,
                content="Se identificaron cambios en este archivo ¿desea guardar y cerrar?",
                first_button_title="Guardar",
                message_type=MessageTypes.QUESTION,
            )
            msg.add_button("Cerrar de todas formas")
            option = msg.run()
            if option != SaveOptions.SAVE and option != SaveOptions.NO_SAVE:
                return
            content = editor.toPlainText()
            if option == SaveOptions.SAVE:
                if file_name == DEFAULT_FILE_NAME and self._tab.has_one_tab:
                    file = QFileDialog.getSaveFileName(
                        parent=self._home,
                        caption="Guardar archivo",
                        dir=os.path.expanduser("~"),
                        filter=get_extensions_list(),
                    )
                    path = file[0]
                    if has_selected(path):
                        ok, error_msg = save_from_path(
                            path, content
                        )
                        if ok:
                            ok, error_msg = self._home.storage_manager.add(path)
                            if not ok:
                                show_system_error_message(self._home, error_msg)
                                return
                            editor.clear()
                            editor.has_changes = False
                            self._tab.set_normal(DEFAULT_FILE_NAME)
                            return
                        show_system_error_message(self._home, error_msg)
                else:
                    ok, error_msg = self._home.storage_manager.save_from_file_name(
                        file_name, content
                    )
                    if ok is False:
                        show_system_error_message(self._home, error_msg)
            self._tab.removeTab(self._tab.currentIndex())
            editor.clear()
            editor.has_changes = False
            self._tab.set_normal()
        else:
            if self._tab.has_one_tab:
                editor.clear()
                editor.has_changes = False
                self._tab.set_normal(FileNames.DEFAULT)
            else:
                self._tab.removeTab(self._tab.currentIndex())
            self._home.storage_manager.remove(file_name)

    @Slot()
    def _close_all(self) -> None:
        pass

    def _when_opening(self, tab_manager: Tab, path: Path, here: bool = False) -> None:
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
        if here:
            tab_manager.change_tab_name(path.name)
            tab_manager.add_content_to_current_tab(content=get_content_from_file(path.name))
        else:
            tab_manager.new()
        editor.has_changes = False
        tab_manager.set_is_open_mode(False)
        tab_manager.add_to_loaded_files(path.name)
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
