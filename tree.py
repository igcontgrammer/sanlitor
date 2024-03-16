import os

from PySide6.QtWidgets import QFileSystemModel, QTreeView
from constants import AppModes


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
        """Construye el arbol de archivos."""
        from home import Home

        if not isinstance(self._parent, Home):
            raise ValueError("parent is not an instance of Home")
        if not self._is_ok():
            raise ValueError(f"El directorio {self._path} no existe o no es válido.")
        tree = self._get_tree()
        self._hide_columns(tree)
        self._parent.set_central(utilities=AppModes.TREE, widget=tree)
        # TODO: llamar al componente main y cambiar su estructura

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
