import os
from dataclasses import dataclass
from typing import Final, Optional
from extensions import Extensions
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTextEdit
from . import (
    QMenu,
    QAction,
    Slot,
    ActionHelper,
    SectionsNames,
    QCoreApplication as coreapp,
)


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
class FileMenuActionsShortcuts:
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


OPEN_HERE: Final[int] = 0
OPEN_NEW_TAB: Final[int] = 1


class FileMenu(QMenu):

    def __init__(self, home):
        super().__init__()
        self._file_menu = QMenu(SectionsNames.FILE)
        self._home = home
        self._create_actions()

    def get_menu(self) -> QMenu:
        return self._file_menu

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
        ActionHelper().config(
            action=open_file_action,
            status_tip="Open a file",
            shortcut=FileMenuActionsShortcuts.OPEN,
            method=self._open_file,
        )
        self._file_menu.addAction(open_file_action)

    def _new_file_action(self) -> None:
        new_file_action = QAction(FileMenuActionsNames.NEW, self)
        ActionHelper().config(
            action=new_file_action,
            status_tip="Create a new file",
            shortcut=FileMenuActionsShortcuts.NEW,
            method=self._new_file,
        )
        self._file_menu.addAction(new_file_action)

    def _save_file_action(self) -> None:
        save_file_action = QAction(FileMenuActionsNames.SAVE, self)
        ActionHelper().config(
            action=save_file_action,
            status_tip="Save a file",
            shortcut=FileMenuActionsShortcuts.SAVE,
            method=self._save_file,
        )
        self._file_menu.addAction(save_file_action)

    def _save_as_action(self) -> None:
        save_as_action = QAction(FileMenuActionsNames.SAVE_AS, self)
        ActionHelper().config(
            action=save_as_action,
            status_tip="Save a file as...",
            shortcut=FileMenuActionsShortcuts.SAVE_AS,
            method=self._save_file,
        )
        self._file_menu.addAction(save_as_action)

    def _save_all_files_action(self) -> None:
        save_all_files_action = QAction(FileMenuActionsNames.SAVE_ALL, self)
        ActionHelper().config(
            action=save_all_files_action,
            status_tip="Save all files",
            shortcut=FileMenuActionsShortcuts.SAVE_ALL,
            method=self._save_all_files,
        )
        self._file_menu.addAction(save_all_files_action)

    def _close_file_action(self) -> None:
        close_file_action = QAction(FileMenuActionsNames.CLOSE, self)
        ActionHelper().config(
            action=close_file_action,
            status_tip="Close a file",
            shortcut=FileMenuActionsShortcuts.CLOSE,
            method=self._edit_file,
        )
        self._file_menu.addAction(close_file_action)

    def _close_all_files_action(self) -> None:
        close_all_files_action = QAction(FileMenuActionsNames.CLOSE_ALL, self)
        ActionHelper().config(
            action=close_all_files_action,
            status_tip="Close all files",
            shortcut=FileMenuActionsShortcuts.CLOSE_ALL,
            method=self._edit_file,
        )
        self._file_menu.addAction(close_all_files_action)

    def _print_action(self) -> None:
        print_action = QAction(FileMenuActionsNames.PRINT, self)
        ActionHelper().config(
            action=print_action,
            status_tip="Print a file",
            shortcut="",
            method=self._print_file,
        )
        self._file_menu.addAction(print_action)

    def _exit_action(self) -> None:
        exit_action = QAction(FileMenuActionsNames.EXIT, self)
        ActionHelper().config(
            action=exit_action,
            status_tip="Exit the application",
            shortcut=FileMenuActionsShortcuts.EXIT,
            method=self._exit_application,
        )
        self._file_menu.addAction(exit_action)

    @Slot()
    def _open_file(self) -> None:
        home_dir = os.path.expanduser("~")
        file = QFileDialog.getOpenFileName(
            self, coreapp.translate("file_menu", "Abrir archivo"), dir=home_dir
        )
        if self._has_opened_a_file(file[0]):
            path = file[0]
            extension_detected = os.path.splitext(path)[1]
            if extension_detected not in Extensions.get_available_extensions():
                QMessageBox.critical(
                    self,
                    "Error",
                    coreapp.translate("file_menu", "Extensión no permitida."),
                )
                return
            from home import Home

            self._home: Home
            content = self._get_file_selected_content(path)
            option = self.place_to_set_content_option()
            if option == OPEN_HERE:
                current = self._home.get_tab()
                current.setTabText(current.currentIndex(), os.path.basename(path))
                current.widget(current.currentIndex()).setPlainText(content)
            elif option == OPEN_NEW_TAB:
                new_index = self._home.get_tab().addTab(
                    QTextEdit(), os.path.basename(path)
                )
                self._home.get_tab().setCurrentIndex(new_index)
            else:
                return

    def _get_file_selected_content(self, path: str) -> Optional[str]:
        with open(path, "r") as file:
            content = file.read()
            return content if len(content) > 0 else None

    def place_to_set_content_option(self) -> int:
        dlg = QMessageBox(self)
        dlg.setWindowTitle(coreapp.translate("file_menu", "Abrir Archivo"))
        dlg.setText(coreapp.translate("file_menu", "¿Dónde desea abrir el archivo?"))
        dlg.setStandardButtons(QMessageBox.Cancel)
        dlg.addButton(coreapp.translate("file_menu", "Aquí"), QMessageBox.AcceptRole)
        dlg.addButton(
            coreapp.translate("file_menu", "En una nueva pestaña"),
            QMessageBox.AcceptRole,
        )
        dlg.button(QMessageBox.Cancel).setText(
            coreapp.translate("file_menu", "Cancelar")
        )
        dlg.setIcon(QMessageBox.Question)
        option_selected = dlg.exec_()
        return option_selected

    def _set_content_on_open_file(self, content: str) -> None:
        pass
        # with open(path, "r") as file:
        #     content = file.read()
        #     if len(content) > 0:
        #         from home import Home

        #         self._home: Home
        #         tab = self._home.get_tab()

        #         if tab.is_default():
        #             tab.set_content(content)
        #             tab.change_tab_name(0, os.path.basename(path))
        #     return

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
