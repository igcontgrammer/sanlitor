import os
from dataclasses import dataclass
from typing import Final, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget

from constants import AppMode, SaveOptions, ThemeModes
from editor import Editor
from menus.menu import MenuBar
from messages import Messages, MessageTypes
from statusbar import StatusBar
from storage_manager import StorageManager
from tab_manager import Tab

_MAIN_WINDOW_TITLE: Final[str] = "Sanlitor"


@dataclass(frozen=True)
class HomeDefaultDimensions:
    MAIN_WINDOW_MIN_HEIGHT: int = 300
    MAIN_WINDOW_MIN_WIDTH: int = 400
    MAIN_WINDOW_DEFAULT_HEIGHT: int = 600
    MAIN_WINDOW_DEFAULT_WIDTH: int = 1000


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self._splitter = QSplitter(Qt.Horizontal)  # type: ignore
        self.storage_manager = StorageManager()
        self._tab = Tab(home=self)
        self._theme_mode = ThemeModes.LIGHT
        self.__set_main_window_default_config()
        self.__call_main_widgets()
        self.change_central(AppMode.DEFAULT)

    @property
    def tab(self) -> Tab:
        return self._tab

    @property
    def theme_mode(self) -> ThemeModes:
        return self._theme_mode

    @property
    def last_tab_worked_index(self) -> int:
        return self.storage_manager.last_tab_worked_index

    def change_central(self, mode: AppMode, widget: Optional[QWidget] = None) -> None:
        if mode != AppMode.DEFAULT and widget is not None:
            self._splitter.addWidget(widget)
            self._splitter.addWidget(self._tab)
            self.setCentralWidget(self._splitter)
        else:
            self.setCentralWidget(self._tab)

    def closeEvent(self, event: QCloseEvent) -> None:
        any_changes = self.tab.tabs_has_changes()
        has_new_tabs = len(self.tab._loaded_files) > 0
        option = None
        if any_changes:
            msg = Messages(
                parent=self,
                content="Hay cambios sin guardar ¿desea guardar todo?",
                first_button_title="Guardar",
                message_type=MessageTypes.QUESTION,
            )
            msg.add_button("No guardar")
            option = msg.run()
            if option != SaveOptions.SAVE and option != SaveOptions.NO_SAVE:
                event.ignore()
                msg.close()
                return
        if option == SaveOptions.NO_SAVE:
            super().closeEvent(event)
            return
        if has_new_tabs or option == SaveOptions.YES:
            for path in self.storage_manager.paths:
                file_name = os.path.basename(path)
                for i in range(self._tab.count()):
                    if file_name != self._tab.tabText(i):
                        continue
                    editor = self._tab.widget(i)
                    if not isinstance(editor, Editor):
                        print("editor is not an instance of Editor")
                        return None
                    content = editor.toPlainText()
                    save_status = self.storage_manager.save_from_path(path, content)
                    if save_status[0] is False:
                        msg = Messages(
                            parent=self,
                            content="Tuvimos problemas para cerrar correctamente los archivos. Reinicie la aplicación.",
                            first_button_title="De acuerdo",
                            message_type=MessageTypes.CRITICAL,
                        )
                        msg.run()
                        break
                    self._tab.set_normal(file_name)
                    editor.has_changes = False
        super().closeEvent(event)

    def _add_menu(self) -> None:
        self.menu = MenuBar(home=self)

    def _add_status_bar(self) -> None:
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar.get_status_bar())

    def __set_main_window_default_config(self) -> None:
        self.setWindowTitle(_MAIN_WINDOW_TITLE)
        self.__set_default_dimensions()

    def __call_main_widgets(self) -> None:
        self.__set_main_window_default_config()
        self._add_menu()
        self._add_status_bar()

    def __set_default_dimensions(self) -> None:
        self.setMinimumHeight(HomeDefaultDimensions.MAIN_WINDOW_MIN_HEIGHT)
        self.setMinimumWidth(HomeDefaultDimensions.MAIN_WINDOW_MIN_WIDTH)
        self.resize(
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_WIDTH,
            HomeDefaultDimensions.MAIN_WINDOW_DEFAULT_HEIGHT,
        )
