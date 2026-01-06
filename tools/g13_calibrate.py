#!/usr/bin/env python3
"""
Interactive G13 Button Position Calibrator

Click on the device image to set button positions.
Generates g13_layout.py code that can be copied to the resources folder.

Usage:
    python3 tools/g13_calibrate.py
"""
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Button click order
BUTTON_ORDER = [
    "M1", "M2", "M3", "MR",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7",
    "G8", "G9", "G10", "G11", "G12", "G13", "G14",
    "G15", "G16", "G17", "G18", "G19",
    "G20", "G21", "G22",
    "LEFT", "DOWN", "STICK",
]

# Default button sizes
BUTTON_SIZES = {
    "M": (28, 18),      # M-keys (small)
    "G_SMALL": (38, 28),  # G1-G19 (standard)
    "G_WIDE": (42, 28),   # G20-G22 (wider)
    "LEFT": (28, 22),
    "DOWN": (28, 22),
    "STICK": (35, 35),
}


def get_button_size(name: str) -> tuple[int, int]:
    """Get default size for a button."""
    if name.startswith("M"):
        return BUTTON_SIZES["M"]
    if name in ("G20", "G21", "G22"):
        return BUTTON_SIZES["G_WIDE"]
    if name.startswith("G"):
        return BUTTON_SIZES["G_SMALL"]
    return BUTTON_SIZES.get(name, (30, 25))


class ImageLabel(QLabel):
    """Clickable image label."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_callback = None

    def mousePressEvent(self, event: QMouseEvent):
        if self.click_callback:
            self.click_callback(event.pos().x(), event.pos().y())


class G13Calibrator(QMainWindow):
    """Interactive G13 button position calibrator."""

    def __init__(self, image_path: str):
        super().__init__()
        self.setWindowTitle("G13 Button Position Calibrator")

        self.image_path = image_path
        self.original_pixmap = QPixmap(image_path)
        self.positions: dict[str, tuple[int, int, int, int]] = {}
        self.current_idx = 0

        self._init_ui()
        self._update_status()

    def _init_ui(self):
        """Setup the UI."""
        main_layout = QHBoxLayout()

        # Left side: image
        left_layout = QVBoxLayout()

        self.status_label = QLabel()
        self.status_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; padding: 10px; "
            "background: #333; color: #0f0;"
        )
        left_layout.addWidget(self.status_label)

        self.image_label = ImageLabel()
        self.image_label.setPixmap(self.original_pixmap)
        self.image_label.click_callback = self._on_click
        left_layout.addWidget(self.image_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.undo_btn = QPushButton("Undo Last")
        self.undo_btn.clicked.connect(self._undo_last)
        self.reset_btn = QPushButton("Reset All")
        self.reset_btn.clicked.connect(self._reset_all)
        btn_layout.addWidget(self.undo_btn)
        btn_layout.addWidget(self.reset_btn)
        left_layout.addLayout(btn_layout)

        main_layout.addLayout(left_layout)

        # Right side: output
        right_layout = QVBoxLayout()

        right_layout.addWidget(QLabel("Generated Code:"))
        self.output_text = QTextEdit()
        self.output_text.setMinimumWidth(400)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(
            "font-family: monospace; font-size: 11px; background: #1e1e1e; color: #ddd;"
        )
        right_layout.addWidget(self.output_text)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)
        right_layout.addWidget(self.copy_btn)

        main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _update_status(self):
        """Update the status label."""
        if self.current_idx < len(BUTTON_ORDER):
            btn = BUTTON_ORDER[self.current_idx]
            self.status_label.setText(
                f"Click TOP-LEFT corner of: {btn}  "
                f"({self.current_idx + 1}/{len(BUTTON_ORDER)})"
            )
            self.status_label.setStyleSheet(
                "font-size: 16px; font-weight: bold; padding: 10px; "
                "background: #333; color: #0f0;"
            )
        else:
            self.status_label.setText("✓ All buttons mapped! Copy the code.")
            self.status_label.setStyleSheet(
                "font-size: 16px; font-weight: bold; padding: 10px; "
                "background: #060; color: #fff;"
            )

    def _on_click(self, x: int, y: int):
        """Handle click on image."""
        if self.current_idx >= len(BUTTON_ORDER):
            return

        btn_name = BUTTON_ORDER[self.current_idx]
        w, h = get_button_size(btn_name)
        self.positions[btn_name] = (x, y, w, h)
        self.current_idx += 1

        self._update_preview()
        self._update_status()
        self._generate_output()

    def _update_preview(self):
        """Update the image with button overlays."""
        pixmap = QPixmap(self.image_path)
        painter = QPainter(pixmap)

        for name, (x, y, w, h) in self.positions.items():
            # Draw rectangle
            painter.setPen(QPen(QColor(0, 255, 0), 2))
            painter.drawRect(x, y, w, h)

            # Draw label
            painter.setPen(QColor(255, 255, 0))
            painter.drawText(x + 2, y + h - 3, name)

        painter.end()
        self.image_label.setPixmap(pixmap)

    def _generate_output(self):
        """Generate the Python code."""
        lines = [
            '"""G13 Button Layout - Generated by g13_calibrate.py"""',
            "",
            "KEYBOARD_WIDTH = 1024",
            "KEYBOARD_HEIGHT = 1024",
            "",
            "",
            "def _box(x, y, w, h):",
            '    """Create position dict."""',
            '    return {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}',
            "",
            "",
            "G13_BUTTON_POSITIONS = {",
        ]

        # Group by row for readability
        groups = [
            ("# M-keys row", ["M1", "M2", "M3", "MR"]),
            ("# Row 1: G1-G7", ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]),
            ("# Row 2: G8-G14", ["G8", "G9", "G10", "G11", "G12", "G13", "G14"]),
            ("# Row 3: G15-G19", ["G15", "G16", "G17", "G18", "G19"]),
            ("# Row 4: G20-G22", ["G20", "G21", "G22"]),
            ("# Thumb buttons", ["LEFT", "DOWN", "STICK"]),
        ]

        for comment, buttons in groups:
            has_any = any(b in self.positions for b in buttons)
            if has_any:
                lines.append(f"    {comment}")
                for name in buttons:
                    if name in self.positions:
                        x, y, w, h = self.positions[name]
                        lines.append(f'    "{name}": _box({x}, {y}, {w}, {h}),')
                lines.append("")

        lines.append("}")
        lines.append("")

        # Add JOYSTICK_AREA if STICK is defined
        if "STICK" in self.positions:
            x, y, w, h = self.positions["STICK"]
            lines.append(f'JOYSTICK_AREA = {{"x": {x}, "y": {y}, "width": {w}, "height": {h}}}')

        # Add LCD_AREA placeholder
        lines.append('LCD_AREA = {"x": 385, "y": 158, "width": 160, "height": 45}')

        self.output_text.setText("\n".join(lines))

    def _undo_last(self):
        """Undo the last button placement."""
        if self.current_idx > 0:
            self.current_idx -= 1
            btn_name = BUTTON_ORDER[self.current_idx]
            if btn_name in self.positions:
                del self.positions[btn_name]
            self._update_preview()
            self._update_status()
            self._generate_output()

    def _reset_all(self):
        """Reset all button placements."""
        self.positions.clear()
        self.current_idx = 0
        self.image_label.setPixmap(self.original_pixmap)
        self._update_status()
        self.output_text.clear()

    def _copy_to_clipboard(self):
        """Copy generated code to clipboard."""
        QApplication.clipboard().setText(self.output_text.toPlainText())
        self.copy_btn.setText("Copied!")
        # Reset button text after 2 seconds
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy to Clipboard"))


def main():
    app = QApplication(sys.argv)

    # Find the device image
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    image_path = project_dir / "src/g13_linux/gui/resources/images/g13_device.png"

    if not image_path.exists():
        print(f"Error: Device image not found at {image_path}")
        return 1

    calibrator = G13Calibrator(str(image_path))
    calibrator.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
