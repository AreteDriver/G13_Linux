"""
Hardware Control Widget

LCD and backlight control UI.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QTextEdit,
    QPushButton,
    QSlider,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from ..widgets.color_picker import ColorPickerWidget


class HardwareControlWidget(QWidget):
    """LCD and backlight control UI"""

    lcd_text_changed = pyqtSignal(str)
    backlight_color_changed = pyqtSignal(str)  # Hex color
    backlight_brightness_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # LCD Control
        lcd_group = QGroupBox("LCD Display (160x43)")
        lcd_layout = QVBoxLayout()

        lcd_label = QLabel("Text to display:")
        lcd_layout.addWidget(lcd_label)

        self.lcd_text = QTextEdit()
        self.lcd_text.setMaximumHeight(60)
        self.lcd_text.setPlaceholderText("Enter text for LCD...")
        lcd_layout.addWidget(self.lcd_text)

        lcd_btn_layout = QHBoxLayout()
        send_btn = QPushButton("Send to LCD")
        send_btn.clicked.connect(
            lambda: self.lcd_text_changed.emit(self.lcd_text.toPlainText())
        )
        lcd_btn_layout.addWidget(send_btn)

        clear_btn = QPushButton("Clear LCD")
        clear_btn.clicked.connect(lambda: self.lcd_text_changed.emit(""))
        lcd_btn_layout.addWidget(clear_btn)

        lcd_layout.addLayout(lcd_btn_layout)
        lcd_group.setLayout(lcd_layout)
        layout.addWidget(lcd_group)

        # Backlight Control
        backlight_group = QGroupBox("RGB Backlight")
        backlight_layout = QVBoxLayout()

        # Color picker
        color_label = QLabel("Color:")
        backlight_layout.addWidget(color_label)

        self.color_picker = ColorPickerWidget()
        self.color_picker.color_changed.connect(self.backlight_color_changed.emit)
        backlight_layout.addWidget(self.color_picker)

        # Brightness slider
        brightness_label = QLabel("Brightness:")
        backlight_layout.addWidget(brightness_label)

        brightness_layout = QHBoxLayout()
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(
            self.backlight_brightness_changed.emit
        )
        brightness_layout.addWidget(self.brightness_slider)

        self.brightness_value = QLabel("100%")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_value.setText(f"{v}%")
        )
        brightness_layout.addWidget(self.brightness_value)

        backlight_layout.addLayout(brightness_layout)
        backlight_group.setLayout(backlight_layout)
        layout.addWidget(backlight_group)

        layout.addStretch()
        self.setLayout(layout)
