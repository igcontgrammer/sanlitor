import os

from PySide6.QtWidgets import QFileSystemModel, QTreeView
from PySide6.QtCore import Slot, QModelIndex

from constants import AppMode


class Tree:
    def __init__(self, parent, path: str):
        self._parent = parent
        self._path = path
        self._is_active = False

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self._is_active = value

    def build(self) -> None:
        from home import Home

        if not isinstance(self._parent, Home):
            raise ValueError("parent is not an instance of Home")
        if not self._is_ok():
            raise ValueError(f"El directorio {self._path} no existe o no es válido.")
        tree = self._get_tree()
        tree.clicked.connect(lambda: self.on_click_element(tree.currentIndex()))
        self._hide_columns(tree)
        self._parent.change_central(AppMode.TREE, tree)
        self.is_active = True

    @Slot()
    def on_click_element(self, element: QModelIndex) -> None:
        file_selected = element.data()
        path = os.path.join(self._path, file_selected)
        # TODO: ir al storage manager y ver si existe o no
        # TODO: al hacerle click, que se visualice en el editor
        return None

    # TODO: implementar esto
    def remove(self) -> None:
        self._parent.set_central(AppMode.DEFAULT)
        self.is_active = False

    def open_file(self, index: int) -> None:
        return None

    def open_dir(self, index: int) -> None:
        return None

    def _is_ok(self) -> bool:
        return os.path.exists(self._path) and os.path.isdir(self._path)

    def _get_tree(self) -> QTreeView:
        model = QFileSystemModel()
        model.setRootPath(self._path)
        tree = QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(self._path))
        tree.setHeaderHidden(True)
        return tree

    def _hide_columns(self, tree: QTreeView) -> None:
        for i in range(1, tree.model().columnCount()):
            tree.hideColumn(i)
