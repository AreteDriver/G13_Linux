"""
G13 Button Widget

Custom QPushButton representing a single G13 button.
"""

try:
    from PyQt6.QtWidgets import QPushButton
    from PyQt6.QtCore import Qt, pyqtSignal
except ImportError:
    # Stub for development without PyQt6
    class QPushButton:
        def __init__(self, *args, **kwargs):
            pass

    class Qt:
        pass

    def pyqtSignal(*args):
        return None


class G13Button(QPushButton):
    """Individual G13 button widget"""

    def __init__(self, button_id: str, parent=None):
        super().__init__(button_id, parent)
        self.button_id = button_id
        self.mapped_key = None
        self.is_highlighted = False
        self._update_style()

    def set_mapping(self, key_name: str | dict | None):
        """
        Set the mapped key and update display.

        Args:
            key_name: Key code name (e.g., 'KEY_1'), combo dict, or None to clear
                      Combo format: {'keys': ['KEY_LEFTCTRL', 'KEY_B'], 'label': '...'}
        """
        self.mapped_key = key_name

        if key_name is None or key_name == "KEY_RESERVED":
            display_text = self.button_id
        elif isinstance(key_name, dict):
            # Combo key format
            label = key_name.get("label", "")
            keys = key_name.get("keys", [])
            if label:
                display_text = f"{self.button_id}\n{label}"
            elif keys:
                # Show abbreviated key combo
                short_keys = [k.replace("KEY_", "") for k in keys]
                display_text = f"{self.button_id}\n{'+'.join(short_keys)}"
            else:
                display_text = self.button_id
        else:
            # Simple key format
            display_key = key_name.replace("KEY_", "")
            display_text = f"{self.button_id}\n{display_key}"

        self.setText(display_text)
        self._update_style()

    def set_highlighted(self, highlight: bool):
        """
        Highlight button when physically pressed.

        Args:
            highlight: True to highlight, False to unhighlight
        """
        self.is_highlighted = highlight
        self._update_style()

    def _has_mapping(self) -> bool:
        """Check if button has a valid mapping."""
        if not self.mapped_key:
            return False
        if self.mapped_key == "KEY_RESERVED":
            return False
        if isinstance(self.mapped_key, dict):
            return bool(self.mapped_key.get("keys"))
        return True

    def _update_style(self):
        """Update button appearance - semi-transparent to show device image"""
        if self.is_highlighted:
            # Bright orange when physically pressed (like real G13 backlight)
            bg_color = "rgba(255, 140, 0, 180)"
            border_color = "#FFB84D"
            text_color = "#000000"
            hover_bg = "rgba(255, 160, 50, 200)"
        elif self._has_mapping():
            # Semi-transparent teal when mapped
            bg_color = "rgba(45, 90, 90, 160)"
            border_color = "#4A9A9A"
            text_color = "#AAFFFF"
            hover_bg = "rgba(60, 110, 110, 180)"
        else:
            # Very transparent - let device image show through
            bg_color = "rgba(40, 40, 45, 80)"
            border_color = "rgba(80, 80, 85, 120)"
            text_color = "rgba(200, 200, 200, 180)"
            hover_bg = "rgba(60, 80, 80, 140)"

        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                padding: 1px;
            }}
            QPushButton:hover {{
                border: 2px solid #00CCCC;
                background: {hover_bg};
            }}
            QPushButton:pressed {{
                background: rgba(20, 40, 40, 200);
            }}
        """)

    def _lighten_color(self, hex_color: str) -> str:
        """Lighten a hex color for hover effect"""
        # Simple lightening by blending with white
        color = hex_color.lstrip("#")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _darken_color(self, hex_color: str) -> str:
        """Darken a hex color for pressed effect"""
        color = hex_color.lstrip("#")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        return f"#{r:02x}{g:02x}{b:02x}"
