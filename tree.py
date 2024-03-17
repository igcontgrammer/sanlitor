import os
from typing import Optional, Tuple

from PySide6.QtCore import QModelIndex, Slot
from PySide6.QtWidgets import QFileSystemModel, QTreeView

from constants import AppMode
from extensions import available_extensions
from utils import get_extension


def hide_columns(tree: QTreeView) -> None:
    for i in range(1, tree.model().columnCount()):
        tree.hideColumn(i)


class Tree:
    def __init__(self, home, path: str):
        from home import Home

        self._home: Home = home
        self._path = path

    def get(self) -> QTreeView:
        if not self._is_ok():
            raise ValueError(f"El directorio {self._path} no existe o no es válido.")
        model = QFileSystemModel()
        model.setRootPath(self._path)
        tree = QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(self._path))
        tree.setHeaderHidden(True)
        tree.clicked.connect(lambda: self._on_click(tree.currentIndex()))
        hide_columns(tree)
        return tree

    def remove(self) -> None:
        self._home.change_central(AppMode.DEFAULT)

    @Slot()
    def _on_click(self, element: QModelIndex) -> None:
        file_selected = element.data()
        path = os.path.join(self._path, file_selected)
        ok, error_msg = self._open_element(path)
        if not ok:
            print(error_msg)
            return
        ok, error_msg = self._home.storage_manager.add(path)
        if not ok:
            print(error_msg)
            return

    def _open_element(self, path: str) -> Tuple[bool, Optional[str]]:
        if os.path.isdir(path):
            return True, None
        elif os.path.isfile(path):
            file_name = os.path.basename(path)
            if self._home.storage_manager.file_exists(file_name):
                self._home.tab.move(file_name)
                return True, None
            extension = get_extension(file_name)
            if extension not in available_extensions():
                return False, "La extensión no es válida."
            try:
                with open(path, "r") as file:
                    content = file.read()
                self._home.tab.new_from_already_exists(file_name, content)
                return True, None
            except FileNotFoundError as fnf:
                return False, str(fnf)
            except Exception as e:
                return False, str(e)
        else:
            raise ValueError(f"El archivo {path} no existe o no es válido.")

    def _is_ok(self) -> bool:
        return os.path.exists(self._path) and os.path.isdir(self._path)

