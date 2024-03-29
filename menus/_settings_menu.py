from common.config_action import config

from . import QAction, QMenu, SectionsNames, Slot
from ._menus_constants import SettingsMenuActionsNames


class SettingsMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.setTitle(SectionsNames.SETTINGS)
        self._create_actions()

    @property
    def menu(self) -> QMenu:
        return self

    def _create_actions(self) -> None:
        self._add_preferences_action()
        self._open_style_configurator_action()
        self._open_shortcut_mapper_action()
        self._import_menu_action()

    def _add_preferences_action(self) -> None:
        preferences = QAction(SettingsMenuActionsNames.PREFERENCES, self)
        config(
            action=preferences,
            shortcut="",
            status_tip="Open Preferences",
            method=self._open_preferences,
        )
        self.addAction(preferences)

    def _open_style_configurator_action(self) -> None:
        style_configurator = QAction(SettingsMenuActionsNames.STYLE_CONFIGURATOR, self)
        config(
            action=style_configurator,
            shortcut="",
            status_tip="Open Style Configurator",
            method=self._open_style_configurator_action,
        )
        self.addAction(style_configurator)

    def _open_shortcut_mapper_action(self) -> None:
        shortcut_mapper = QAction(SettingsMenuActionsNames.SHORTCUT_MANAGER, self)
        config(
            action=shortcut_mapper,
            shortcut="",
            status_tip="Open Shortcut Mapper",
            method=self._open_shortcut_mapper_action,
        )
        self.addAction(shortcut_mapper)

    def _import_menu_action(self) -> None:
        import_menu = QMenu(SettingsMenuActionsNames.IMPORT, self)
        plugin_action = QAction(SettingsMenuActionsNames.PLUGIN, self)
        style_action = QAction(SettingsMenuActionsNames.STYLE_THEME, self)
        config(
            action=plugin_action,
            shortcut="",
            status_tip="Import Plugin",
            method=self._open_import_plugin_action,
        )
        config(
            action=style_action,
            shortcut="",
            status_tip="Add Style Theme",
            method=self._open_style_theme_action,
        )
        import_menu.addAction(plugin_action)
        import_menu.addAction(style_action)
        self.addMenu(import_menu)

    @Slot()
    def _open_preferences(self) -> None:
        print("opening preferences...")
        pass

    @Slot()
    def _open_style_configurator_action(self) -> None:
        print("opening style configurator...")
        pass

    @Slot()
    def _open_shortcut_mapper_action(self) -> None:
        print("opening shortcut mapper...")
        pass

    @Slot()
    def _open_import_plugin_action(self) -> None:
        print("opening import plugin...")
        pass

    @Slot()
    def _open_style_theme_action(self) -> None:
        print("opening style theme...")
        pass
