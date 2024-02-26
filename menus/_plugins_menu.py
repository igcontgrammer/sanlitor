from common.config_action import config

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import PluginsMenuActionsNames


class PluginsMenu(QMenu):
    def __init__(self):
        super().__init__()
        self._plugin_menu = QMenu(SectionsNames.PLUGINS)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self._plugin_menu

    def _create_actions(self) -> None:
        self._plugins_manager_action()
        self._open_plugins_folder_action()

    def _plugins_manager_action(self) -> None:
        plugins_manager_action = QAction(PluginsMenuActionsNames.PLUGIN_MANAGER, self)
        config(
            action=plugins_manager_action,
            status_tip="Plugins Manager",
            shortcut="",
            method=self.plugins_manager,
        )
        self._plugin_menu.addAction(plugins_manager_action)

    def _open_plugins_folder_action(self) -> None:
        open_plugins_folder_action = QAction(
            PluginsMenuActionsNames.OPEN_PLUGINS_FOLDER, self
        )
        config(
            action=open_plugins_folder_action,
            status_tip="Open Plugins Folder",
            shortcut="",
            method=self.open_plugins_folder,
        )
        self._plugin_menu.addAction(open_plugins_folder_action)

    @Slot()
    def plugins_manager(self) -> None:
        print("Plugins Manager")

    @Slot()
    def open_plugins_folder(self) -> None:
        print("Open Plugins Folder")
