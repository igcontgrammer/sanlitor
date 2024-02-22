from ._menus_constants import ViewMenuActionsNames, ViewMenuShortcuts
from . import QMenu, QAction, Slot, ActionHelper, SectionsNames


class ViewMenu(QMenu):

    def __init__(self):
        super().__init__()
        self._view_menu = QMenu(SectionsNames.VIEW)
        self._create_actions()

    def get_menu(self) -> QMenu:
        return self._view_menu

    def _create_actions(self) -> None:
        self._toggle_full_screen_action()
        self._distraction_free_mode_action()
        self._zoom_action()
        self._move_clone_current_document_action()
        self._tab_action()
        self._summary_action()
        self._project_panels_action()
        self._folder_as_workspace_action()
        self._document_map_action()
        self._document_list_action()
        self._function_list_action()

    def _toggle_full_screen_action(self) -> None:
        toggle_action = QAction(ViewMenuActionsNames.TOGGLE_FULL_SCREEN, self)
        ActionHelper().config(
            action=toggle_action,
            shortcut=ViewMenuShortcuts.TOGGLE_FULL_SCREEN,
            status_tip="Toggle full screen",
            method=self.toggle_full_screen,
        )
        self._view_menu.addAction(toggle_action)

    def _distraction_free_mode_action(self) -> None:
        distraction_free_mode_action = QAction(
            ViewMenuActionsNames.DISTRACTION_FREE_MODE, self
        )
        ActionHelper().config(
            action=distraction_free_mode_action,
            shortcut="",
            status_tip="Distraction free mode",
            method=self.distraction_free_mode,
        )
        self._view_menu.addAction(distraction_free_mode_action)

    def _zoom_action(self) -> None:
        zoom_menu = QMenu(ViewMenuActionsNames.ZOOM)
        zoom_in_action = QAction(ViewMenuActionsNames.ZOOM_IN, self)
        zoom_out_action = QAction(ViewMenuActionsNames.ZOOM_OUT, self)
        ActionHelper().config(
            action=zoom_in_action,
            shortcut=ViewMenuShortcuts.ZOOM_IN,
            status_tip="Zoom in",
            method=self._zoom_in,
        )
        ActionHelper().config(
            action=zoom_out_action,
            shortcut=ViewMenuShortcuts.ZOOM_OUT,
            status_tip="Zoom out",
            method=self._zoom_out,
        )
        zoom_menu.addAction(zoom_in_action)
        zoom_menu.addAction(zoom_out_action)
        self._view_menu.addMenu(zoom_menu)

    def _move_clone_current_document_action(self) -> None:
        move_action = QAction(ViewMenuActionsNames.MOVE_CLONE_CURRENT_DOCUMENT, self)
        ActionHelper().config(
            action=move_action,
            shortcut="",
            status_tip="Move/clone current document",
            method=self.move_clone_current_document,
        )
        self._view_menu.addAction(move_action)

    def _tab_action(self) -> None:
        tab_action = QAction(ViewMenuActionsNames.TAB, self)
        ActionHelper().config(
            action=tab_action, shortcut="", status_tip="Tab", method=self.tab
        )
        self._view_menu.addAction(tab_action)

    def _summary_action(self) -> None:
        summary_action = QAction(ViewMenuActionsNames.SUMMARY, self)
        ActionHelper().config(
            action=summary_action,
            shortcut="",
            status_tip="Summary",
            method=self.summary,
        )
        self._view_menu.addAction(summary_action)

    def _project_panels_action(self) -> None:
        project_panels_action = QAction(ViewMenuActionsNames.PROJECT_PANELS, self)
        ActionHelper().config(
            action=project_panels_action,
            shortcut="",
            status_tip="Project panels",
            method=self.project_panels,
        )
        self._view_menu.addAction(project_panels_action)

    def _folder_as_workspace_action(self) -> None:
        folder_as_workspace_action = QAction(
            ViewMenuActionsNames.FOLDER_AS_WORKSPACE, self
        )
        ActionHelper().config(
            action=folder_as_workspace_action,
            shortcut="",
            status_tip="Folder as workspace",
            method=self.folder_as_workspace,
        )
        self._view_menu.addAction(folder_as_workspace_action)

    def _document_map_action(self) -> None:
        document_map_action = QAction(ViewMenuActionsNames.DOCUMENT_MAP, self)
        ActionHelper().config(
            action=document_map_action,
            shortcut="",
            status_tip="Document map",
            method=self.document_map,
        )
        self._view_menu.addAction(document_map_action)

    def _document_list_action(self) -> None:
        document_list_action = QAction(ViewMenuActionsNames.DOCUMENT_LIST, self)
        ActionHelper().config(
            action=document_list_action,
            shortcut="",
            status_tip="Document list",
            method=self.document_list,
        )
        self._view_menu.addAction(document_list_action)

    def _function_list_action(self) -> None:
        function_list_action = QAction(ViewMenuActionsNames.FUNCTION_LIST, self)
        ActionHelper().config(
            action=function_list_action,
            shortcut="",
            status_tip="Function list",
            method=self.function_list,
        )
        self._view_menu.addAction(function_list_action)

    @Slot()
    def always_top(self) -> None:
        pass

    @Slot()
    def toggle_full_screen(self) -> None:
        pass

    @Slot()
    def distraction_free_mode(self) -> None:
        pass

    @Slot()
    def _zoom_in(self) -> None:
        print("Zoom in")
        pass

    @Slot()
    def _zoom_out(self) -> None:
        print("Zoom out")
        pass

    @Slot()
    def move_clone_current_document(self) -> None:
        pass

    @Slot()
    def tab(self) -> None:
        pass

    @Slot()
    def summary(self) -> None:
        pass

    @Slot()
    def project_panels(self) -> None:
        pass

    @Slot()
    def folder_as_workspace(self) -> None:
        pass

    @Slot()
    def document_map(self) -> None:
        pass

    @Slot()
    def document_list(self) -> None:
        pass

    @Slot()
    def function_list(self) -> None:
        pass
