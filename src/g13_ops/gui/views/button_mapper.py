"""
Button Mapper Widget

Visual G13 keyboard layout with clickable buttons.
Renders a realistic representation of the Logitech G13 gaming keypad.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QPointF
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QFont, QBrush,
    QLinearGradient, QPainterPath
)
from ..widgets.g13_button import G13Button
from ..resources.g13_layout import (
    G13_BUTTON_POSITIONS, LCD_AREA, JOYSTICK_AREA,
    KEYBOARD_WIDTH, KEYBOARD_HEIGHT, DEVICE_OUTLINE, THUMB_REST_OUTLINE
)


class ButtonMapperWidget(QWidget):
    """Visual G13 keyboard layout with clickable buttons"""

    button_clicked = pyqtSignal(str)  # Button ID clicked for configuration

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(KEYBOARD_WIDTH, KEYBOARD_HEIGHT)
        self.buttons = {}
        self.joystick_x = 128  # Center position
        self.joystick_y = 128
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

    def set_joystick_position(self, x: int, y: int):
        """Update joystick visual position (0-255 range)"""
        self.joystick_x = x
        self.joystick_y = y
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """Draw G13 device body, LCD, and joystick"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw device body (dark gaming aesthetic)
        self._draw_device_body(painter)

        # Draw LCD screen
        self._draw_lcd(painter)

        # Draw joystick
        self._draw_joystick(painter)

    def _draw_device_body(self, painter):
        """Draw the G13 device outline with thumb rest"""
        # Create gradient for metallic look
        gradient = QLinearGradient(0, 0, 0, KEYBOARD_HEIGHT)
        gradient.setColorAt(0, QColor(55, 55, 60))
        gradient.setColorAt(0.3, QColor(45, 45, 50))
        gradient.setColorAt(0.7, QColor(35, 35, 40))
        gradient.setColorAt(1, QColor(25, 25, 30))

        # Draw main device body
        path = QPainterPath()
        points = [QPointF(float(x), float(y)) for x, y in DEVICE_OUTLINE]
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        path.closeSubpath()

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(70, 70, 75), 2))
        painter.drawPath(path)

        # Draw thumb rest area (slightly darker)
        thumb_gradient = QLinearGradient(0, 80, 100, 200)
        thumb_gradient.setColorAt(0, QColor(40, 40, 45))
        thumb_gradient.setColorAt(1, QColor(30, 30, 35))

        thumb_path = QPainterPath()
        thumb_points = [QPointF(float(x), float(y)) for x, y in THUMB_REST_OUTLINE]
        thumb_path.moveTo(thumb_points[0])
        for point in thumb_points[1:]:
            thumb_path.lineTo(point)
        thumb_path.closeSubpath()

        painter.setBrush(QBrush(thumb_gradient))
        painter.setPen(QPen(QColor(50, 50, 55), 1))
        painter.drawPath(thumb_path)

        # Add beveled edge highlights
        painter.setPen(QPen(QColor(80, 80, 85), 1))
        painter.drawLine(int(DEVICE_OUTLINE[1][0]), int(DEVICE_OUTLINE[1][1]),
                        int(DEVICE_OUTLINE[2][0]), int(DEVICE_OUTLINE[2][1]))

    def _draw_lcd(self, painter):
        """Draw LCD screen area"""
        lcd = LCD_AREA

        # LCD bezel
        painter.setBrush(QBrush(QColor(20, 20, 20)))
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawRoundedRect(lcd['x'] - 5, lcd['y'] - 5,
                               lcd['width'] + 10, lcd['height'] + 10, 3, 3)

        # LCD screen (greenish backlight)
        gradient = QLinearGradient(lcd['x'], lcd['y'],
                                   lcd['x'], lcd['y'] + lcd['height'])
        gradient.setColorAt(0, QColor(40, 80, 40))
        gradient.setColorAt(1, QColor(30, 60, 30))

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(60, 100, 60), 1))
        painter.drawRect(lcd['x'], lcd['y'], lcd['width'], lcd['height'])

        # LCD text placeholder
        painter.setPen(QColor(150, 200, 150))
        painter.setFont(QFont("Consolas", 9))
        painter.drawText(lcd['x'] + 10, lcd['y'] + 20, "G13 OPS")
        painter.setFont(QFont("Consolas", 7))
        painter.drawText(lcd['x'] + 10, lcd['y'] + 35, "Ready")

    def _draw_joystick(self, painter):
        """Draw joystick with current position"""
        js = JOYSTICK_AREA
        center_x = js['x'] + js['width'] // 2
        center_y = js['y'] + js['height'] // 2

        # Joystick base (dark circle)
        painter.setBrush(QBrush(QColor(25, 25, 25)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawEllipse(js['x'], js['y'], js['width'], js['height'])

        # Inner ring
        painter.setBrush(QBrush(QColor(35, 35, 35)))
        painter.drawEllipse(js['x'] + 10, js['y'] + 10,
                           js['width'] - 20, js['height'] - 20)

        # Joystick position (map 0-255 to offset from center)
        offset_x = int((self.joystick_x - 128) / 128 * 15)
        offset_y = int((self.joystick_y - 128) / 128 * 15)

        # Joystick knob
        knob_x = center_x + offset_x - 12
        knob_y = center_y + offset_y - 12

        gradient = QLinearGradient(knob_x, knob_y, knob_x, knob_y + 24)
        gradient.setColorAt(0, QColor(80, 80, 85))
        gradient.setColorAt(1, QColor(50, 50, 55))

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(100, 100, 105), 1))
        painter.drawEllipse(knob_x, knob_y, 24, 24)
