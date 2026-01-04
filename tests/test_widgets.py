"""Tests for GUI widgets using pytest-qt."""

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class TestColorPickerWidget:
    """Tests for ColorPickerWidget."""

    @pytest.fixture
    def widget(self, qtbot):
        """Create ColorPickerWidget instance."""
        from g13_linux.gui.widgets.color_picker import ColorPickerWidget
        w = ColorPickerWidget()
        qtbot.addWidget(w)
        return w

    def test_init_default_color(self, widget):
        """Test widget initializes with white color."""
        assert widget.current_color.name() == "#ffffff"

    def test_init_creates_preview(self, widget):
        """Test widget creates color preview label."""
        assert widget.color_preview is not None
        assert widget.color_preview.width() == 40
        assert widget.color_preview.height() == 40

    def test_set_color_updates_current(self, widget):
        """Test set_color updates current_color."""
        widget.set_color("#ff0000")
        assert widget.current_color.name() == "#ff0000"

    def test_set_color_emits_signal(self, widget, qtbot):
        """Test set_color emits color_changed signal."""
        with qtbot.waitSignal(widget.color_changed, timeout=1000) as blocker:
            widget.set_color("#00ff00")
        assert blocker.args == ["#00ff00"]

    def test_set_color_updates_preview(self, widget):
        """Test set_color updates preview stylesheet."""
        widget.set_color("#0000ff")
        style = widget.color_preview.styleSheet()
        assert "#0000ff" in style

    def test_preset_buttons_exist(self, widget):
        """Test preset color buttons are created."""
        from PyQt6.QtWidgets import QPushButton
        buttons = widget.findChildren(QPushButton)
        # Should have "Pick Color" + 7 presets = 8 buttons
        assert len(buttons) == 8

    def test_preset_red_button(self, widget, qtbot):
        """Test clicking red preset sets color."""
        from PyQt6.QtWidgets import QPushButton
        buttons = widget.findChildren(QPushButton)
        red_btn = next(b for b in buttons if b.text() == "Red")
        
        with qtbot.waitSignal(widget.color_changed):
            qtbot.mouseClick(red_btn, Qt.MouseButton.LeftButton)
        
        assert widget.current_color.name() == "#ff0000"

    def test_preset_cyan_button(self, widget, qtbot):
        """Test clicking cyan preset sets color."""
        from PyQt6.QtWidgets import QPushButton
        buttons = widget.findChildren(QPushButton)
        cyan_btn = next(b for b in buttons if b.text() == "Cyan")
        
        with qtbot.waitSignal(widget.color_changed):
            qtbot.mouseClick(cyan_btn, Qt.MouseButton.LeftButton)
        
        assert widget.current_color.name() == "#00ffff"


class TestG13Button:
    """Tests for G13Button widget."""

    @pytest.fixture
    def button(self, qtbot):
        """Create G13Button instance."""
        from g13_linux.gui.widgets.g13_button import G13Button
        btn = G13Button("G1")
        qtbot.addWidget(btn)
        return btn

    def test_init_button_id(self, button):
        """Test button initializes with correct ID."""
        assert button.button_id == "G1"

    def test_init_text(self, button):
        """Test button displays ID as text."""
        assert button.text() == "G1"

    def test_init_no_mapping(self, button):
        """Test button starts with no mapping."""
        assert button.mapped_key is None

    def test_set_mapping(self, button):
        """Test setting button mapping."""
        button.set_mapping("KEY_A")
        assert button.mapped_key == "KEY_A"

    def test_set_mapping_updates_text(self, button):
        """Test mapping updates button text."""
        button.set_mapping("KEY_SPACE")
        assert "SPACE" in button.text()

    def test_clear_mapping(self, button):
        """Test clearing mapping."""
        button.set_mapping("KEY_B")
        button.set_mapping(None)
        assert button.mapped_key is None

    def test_highlight_on(self, button):
        """Test highlighting button."""
        button.set_highlighted(True)
        assert button.is_highlighted is True

    def test_highlight_off(self, button):
        """Test unhighlighting button."""
        button.set_highlighted(True)
        button.set_highlighted(False)
        assert button.is_highlighted is False

    def test_clicked_signal(self, button, qtbot):
        """Test button emits clicked signal."""
        from g13_linux.gui.widgets.g13_button import G13Button
        
        with qtbot.waitSignal(button.clicked, timeout=1000):
            qtbot.mouseClick(button, Qt.MouseButton.LeftButton)


class TestLCDPreviewWidget:
    """Tests for LCDPreviewWidget."""

    @pytest.fixture
    def widget(self, qtbot):
        """Create LCDPreviewWidget instance."""
        from g13_linux.gui.widgets.lcd_preview import LCDPreviewWidget
        w = LCDPreviewWidget()
        qtbot.addWidget(w)
        return w

    def test_init_dimensions(self, widget):
        """Test widget initializes with correct dimensions."""
        from g13_linux.gui.widgets.lcd_preview import LCD_WIDTH, LCD_HEIGHT
        assert LCD_WIDTH == 160
        assert LCD_HEIGHT == 43

    def test_init_framebuffer_size(self, widget):
        """Test framebuffer is correct size."""
        assert len(widget._framebuffer) == 960

    def test_init_framebuffer_empty(self, widget):
        """Test framebuffer starts empty."""
        assert all(b == 0 for b in widget._framebuffer)

    def test_set_framebuffer(self, widget):
        """Test setting framebuffer data."""
        data = bytes([0xFF] * 960)
        widget.set_framebuffer(data)
        assert widget._framebuffer == bytearray(data)

    def test_set_framebuffer_partial(self, widget):
        """Test setting partial framebuffer."""
        data = bytes([0xAA] * 100)
        widget.set_framebuffer(data)
        # Should pad with zeros
        assert len(widget._framebuffer) == 960

    def test_get_pixel_off(self, widget):
        """Test getting pixel that is off."""
        assert widget.get_pixel(0, 0) is False

    def test_get_pixel_on(self, widget):
        """Test getting pixel that is on."""
        # Set bit 0 of byte 0 (pixel 0,0)
        widget._framebuffer[0] = 0x01
        assert widget.get_pixel(0, 0) is True

    def test_get_pixel_row_7(self, widget):
        """Test getting pixel at row 7."""
        widget._framebuffer[0] = 0x80  # Bit 7
        assert widget.get_pixel(0, 7) is True

    def test_get_pixel_second_row_block(self, widget):
        """Test getting pixel in second row block."""
        widget._framebuffer[160] = 0x01  # Byte 160, bit 0 = (0, 8)
        assert widget.get_pixel(0, 8) is True

    def test_clear(self, widget):
        """Test clearing framebuffer."""
        widget._framebuffer = bytearray([0xFF] * 960)
        widget.clear()
        assert all(b == 0 for b in widget._framebuffer)
