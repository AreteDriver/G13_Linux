"""
Macros Screen

Macro management screen.
"""

from ..items import MenuItem
from .base_menu import MenuScreen
from .toast import ToastScreen


class MacrosScreen(MenuScreen):
    """
    Macro management screen.

    Lists available macros for playback or management.
    """

    def __init__(self, manager):
        """
        Initialize macros screen.

        Args:
            manager: ScreenManager instance
        """
        # TODO: Get macro manager from daemon
        items = self._build_items()
        super().__init__(manager, "MACROS", items)

    def _build_items(self) -> list[MenuItem]:
        """Build menu items from available macros."""
        items = []

        # Placeholder - integrate with macro manager
        items.append(
            MenuItem(
                id="no_macros",
                label="No macros",
                enabled=False,
            )
        )

        items.append(
            MenuItem(
                id="record",
                label="Record New",
                action=self._record_macro,
            )
        )

        return items

    def _record_macro(self):
        """Start macro recording."""
        toast = ToastScreen(self.manager, "Use GUI to record")
        self.manager.show_overlay(toast, duration=2.0)

    def on_enter(self):
        """Refresh macro list when entering."""
        self.items = self._build_items()
        self.selected_index = 0
        self.scroll_offset = 0
        self.mark_dirty()
