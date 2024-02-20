from . import QMenu, QAction, Slot, ConfigAction, SectionsNames


class PluginsMenu(QMenu):

    def __init__(self):
        super().__init__()
        self._plugin_menu = QMenu(SectionsNames.PLUGINS)
        self._create_actions()

    @property
    def get_menu(self) -> QMenu:
        return self._plugin_menu

    def _create_actions(self) -> None:
        self._plugins_manager_action()
        self._open_plugins_folder_action()

    def _plugins_manager_action(self) -> None:
        plugins_manager_action = QAction("Plugins Manager", self)
        ConfigAction().config_action(
            action=plugins_manager_action,
            status_tip="Plugins Manager",
            shortcut="",
            method=self.plugins_manager,
        )
        self._plugin_menu.addAction(plugins_manager_action)

    def _open_plugins_folder_action(self) -> None:
        open_plugins_folder_action = QAction("Open Plugins Folder", self)
        ConfigAction().config_action(
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
