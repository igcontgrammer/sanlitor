import os
from ._menus_constants import FileMenuShortcuts, FileMenuActionsNames, OpenFileOptions
from PySide6.QtWidgets import QFileDialog, QMessageBox
from ._components.messages import Message
from common.config_action import config
from extensions import available_extensions

from . import (
    QMenu,
    QAction,
    Slot,
    SectionsNames,
    QCoreApplication as coreapp,
)


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

    def _open_file_action(self) -> None:
        open_file_action = QAction(FileMenuActionsNames.OPEN, self)
        config(
            action=open_file_action,
            status_tip=coreapp.translate("file_menu", "Open a file"),
            shortcut=FileMenuShortcuts.OPEN,
            method=self._open_file,
        )
        self._menu.addAction(open_file_action)

    def _new_file_action(self) -> None:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        config(
            action=new_file_action,
            status_tip=coreapp.translate("file_menu", "Create a new file"),
            shortcut=FileMenuShortcuts.NEW,
            method=self._new_file,
        )
        self._menu.addAction(new_file_action)

    def _save_file_action(self) -> None:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        config(
            action=save_file_action,
            status_tip=coreapp.translate("file_menu", "Save a file"),
            shortcut=FileMenuShortcuts.SAVE,
            method=self._save_file,
        )
        self._menu.addAction(save_file_action)

    def _save_as_action(self) -> None:
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        config(
            action=save_as_action,
            status_tip=coreapp.translate("file_menu", "Save a file as..."),
            shortcut=FileMenuShortcuts.SAVE_AS,
            method=self._save_file,
        )
        self._menu.addAction(save_as_action)

    def _save_all_files_action(self) -> None:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        config(
            action=save_all_files_action,
            status_tip=coreapp.translate("file_menu", "Save all files"),
            shortcut=FileMenuShortcuts.SAVE_ALL,
            method=self._save_all_files,
        )
        self._menu.addAction(save_all_files_action)

    def _close_file_action(self) -> None:
        close_file_action = QAction(FileMenuActionsNames.CLOSE, self)
        config(
            action=close_file_action,
            status_tip=coreapp.translate("file_menu", "Close a file"),
            shortcut=FileMenuShortcuts.CLOSE,
            method=self._edit_file,
        )
        self._menu.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        config(
            action=close_all_files_action,
            status_tip=coreapp.translate("file_menu", "Close all files"),
            shortcut=FileMenuShortcuts.CLOSE_ALL,
            method=self._edit_file,
        )
        self._menu.addAction(close_all_files_action)

    def _print_action(self) -> None:
        print_action = QAction(FileMenuActionsNames.PRINT, self)
        config(
            action=print_action,
            status_tip=coreapp.translate("file_menu", "Print a file"),
            shortcut="",
            method=self._print_file,
        )
        self._menu.addAction(print_action)

    def _exit_action(self) -> None:
        exit_action = QAction(FileMenuActionsNames.EXIT, self)
        config(
            action=exit_action,
            status_tip=coreapp.translate("file_menu", "Exit the application"),
            shortcut=FileMenuShortcuts.EXIT,
            method=self._exit_application,
        )
        self._menu.addAction(exit_action)

    # ************* SLOTS *************

    @Slot()
    def _open_file(self) -> None:
        file = QFileDialog.getOpenFileName(
            self,
            coreapp.translate("file_menu", "Abrir archivo"),
            dir=os.path.expanduser("~"),
        )
        if not self._has_opened_a_file(file[0]):
            return None
        path = file[0]
        extension_detected = os.path.splitext(path)[1]
        if extension_detected not in available_extensions():
            return None
        from home import Home

        self._home: Home
        tab_manager = self._home.tab_manager
        filename = os.path.basename(path)
        if tab_manager.file_was_opened(filename):
            tab_manager.move(filename)
            return
        # if tab_manager.editor_has_changes:
        #     mensaje = QMessageBox(self)
        #     mensaje.setWindowTitle(coreapp.translate("file_menu", "Advertencia"))
        #     mensaje.setText(
        #         coreapp.translate(
        #             "file_menu", "Este archivo contiene cambios. ¿Desea reemplazar?"
        #         )
        #     )
        #     mensaje.setStandardButtons(QMessageBox.Cancel)
        #     mensaje.addButton(
        #         coreapp.translate("file_menu", "Reemplazar"), QMessageBox.AcceptRole
        #     )
        #     mensaje.button(QMessageBox.Cancel).setText(
        #         coreapp.translate("file_menu", "Cancelar")
        #     )
        #     mensaje.setIcon(QMessageBox.Warning)
        #     option_selected = mensaje.exec_()
        #     print(
        #         f"opcion seleccionada en caso de identificar cambios: {option_selected}"
        #     )
        try:
            match self._get_open_file_option():
                case OpenFileOptions.HERE:
                    # TODO: get to know if file has changes. If it's true, then show a message dialog
                    tab_manager.change_current_tab_name(filename)
                    tab_manager.set_content_to_current_tab(
                        self._get_content_from_file(path)
                    )
                    tab_manager.add_to_loaded_files(filename)
                case OpenFileOptions.NEW_TAB:
                    tab_manager.add_new_tab(filename, self._get_content_from_file(path))
                    tab_manager.add_to_loaded_files(filename)
        except Exception as e:
            error_message = f"An error ocurred at: {e.__class__.__name__}: {e}"
            print(error_message)
            Message.system_error(parent=self)

    def _get_open_file_option(self) -> OpenFileOptions:
        msg = QMessageBox(self)
        msg.setWindowTitle(coreapp.translate("file_menu", "Abrir Archivo"))
        msg.setText(coreapp.translate("file_menu", "¿Dónde desea abrir el archivo?"))
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.addButton(coreapp.translate("file_menu", "Aquí"), QMessageBox.AcceptRole)
        msg.addButton(
            coreapp.translate("file_menu", "En una nueva pestaña"),
            QMessageBox.AcceptRole,
        )
        msg.button(QMessageBox.Cancel).setText(
            coreapp.translate("file_menu", "Cancelar")
        )
        msg.setIcon(QMessageBox.Question)
        option_selected = msg.exec_()
        return OpenFileOptions.HERE if option_selected == 0 else OpenFileOptions.NEW_TAB

    def _get_content_from_file(self, path: str) -> str:
        try:
            with open(path, "r") as file:
                return file.read()
        except Exception as e:
            error_message = f"Error found at: {e.__class__.__name__}. Message: {e}"
            print(error_message)
            return ""

    def _has_opened_a_file(self, filepath: str) -> bool:
        return len(filepath) > 0

    @Slot()
    def _new_file(self) -> None:
        print("Creating a new file...")
        pass

    @Slot()
    def _edit_file(self) -> None:
        print("Editing a file...")
        pass

    @Slot()
    def _save_file(self) -> None:
        print("Saving a file...")
        pass

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
