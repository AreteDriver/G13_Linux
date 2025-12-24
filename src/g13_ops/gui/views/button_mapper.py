"""
Button Mapper Widget

Visual G13 keyboard layout with clickable buttons.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from ..widgets.g13_button import G13Button
from ..resources.g13_layout import G13_BUTTON_POSITIONS, LCD_AREA, KEYBOARD_WIDTH, KEYBOARD_HEIGHT


class ButtonMapperWidget(QWidget):
    """Visual G13 keyboard layout with clickable buttons"""

    button_clicked = pyqtSignal(str)  # Button ID clicked for configuration

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(KEYBOARD_WIDTH, KEYBOARD_HEIGHT)
        self.buttons = {}
        self._init_buttons()

    def _init_buttons(self):
        """Create all G13 buttons based on layout"""
        for button_id, position in G13_BUTTON_POSITIONS.items():
            btn = G13Button(button_id, self)
            btn.setGeometry(
                position['x'],
                position['y'],
                position['width'],
                position['height']
            )
            btn.clicked.connect(lambda checked=False, bid=button_id: self.button_clicked.emit(bid))
            self.buttons[button_id] = btn

    def set_button_mapping(self, button_id: str, key_name: str):
        """Update button label with mapped key"""
        if button_id in self.buttons:
            self.buttons[button_id].set_mapping(key_name)

    def highlight_button(self, button_id: str, highlight: bool):
        """Highlight button when physically pressed"""
        if button_id in self.buttons:
            self.buttons[button_id].set_highlighted(highlight)

    def clear_all_highlights(self):
        """Clear all button highlights"""
        for btn in self.buttons.values():
            btn.set_highlighted(False)

    def paintEvent(self, event):
        """Draw G13 keyboard outline and LCD area"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw keyboard body
        pen = QPen(QColor(100, 100, 100), 2)
        painter.setPen(pen)
        painter.drawRoundedRect(10, 10, KEYBOARD_WIDTH - 20, KEYBOARD_HEIGHT - 20, 10, 10)

        # Draw LCD area
        painter.setPen(QPen(QColor(50, 150, 50), 2))
        painter.drawRect(
            LCD_AREA['x'],
            LCD_AREA['y'],
            LCD_AREA['width'],
            LCD_AREA['height']
        )

        # LCD label
        painter.setFont(QFont("Arial", 8))
        painter.drawText(LCD_AREA['x'] + 5, LCD_AREA['y'] + 15, "LCD (160x43)")
