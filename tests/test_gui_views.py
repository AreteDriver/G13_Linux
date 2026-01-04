"""Tests for GUI view widgets."""

import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication


# Ensure QApplication exists for widget tests
@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


class TestMainWindow:
    """Tests for MainWindow."""

    def test_init(self, qapp):
        """Test MainWindow initialization."""
        from g13_linux.gui.views.main_window import MainWindow

        window = MainWindow()

        assert window.windowTitle() == "G13LogitechOPS - Configuration Tool v0.2.0"
        assert window.minimumWidth() >= 1200
        assert window.minimumHeight() >= 700

    def test_has_widgets(self, qapp):
        """Test MainWindow has all required widgets."""
        from g13_linux.gui.views.main_window import MainWindow

        window = MainWindow()

        assert window.button_mapper is not None
        assert window.profile_widget is not None
        assert window.monitor_widget is not None
        assert window.hardware_widget is not None
        assert window.macro_widget is not None

    def test_has_status_bar(self, qapp):
        """Test MainWindow has status bar."""
        from g13_linux.gui.views.main_window import MainWindow

        window = MainWindow()

        assert window.status_bar is not None
        assert window.statusBar() == window.status_bar

    def test_set_status(self, qapp):
        """Test set_status updates status bar."""
        from g13_linux.gui.views.main_window import MainWindow

        window = MainWindow()
        window.set_status("Test message")

        assert window.status_bar.currentMessage() == "Test message"


class TestLiveMonitorWidget:
    """Tests for LiveMonitorWidget."""

    def test_init(self, qapp):
        """Test LiveMonitorWidget initialization."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        assert widget.max_lines == 1000
        assert widget.event_log is not None
        assert widget.show_raw is not None
        assert widget.show_decoded is not None

    def test_show_decoded_checked_by_default(self, qapp):
        """Test show_decoded is checked by default."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        assert widget.show_decoded.isChecked() is True
        assert widget.show_raw.isChecked() is False

    def test_on_raw_event_when_enabled(self, qapp):
        """Test on_raw_event displays when show_raw is checked."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.show_raw.setChecked(True)

        widget.on_raw_event(b"\x01\x02\x03")

        assert "RAW: 01 02 03" in widget.event_log.toPlainText()

    def test_on_raw_event_when_disabled(self, qapp):
        """Test on_raw_event does not display when show_raw is unchecked."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.show_raw.setChecked(False)

        widget.on_raw_event(b"\x01\x02\x03")

        assert widget.event_log.toPlainText() == ""

    def test_on_button_event_pressed(self, qapp):
        """Test on_button_event displays pressed state."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        widget.on_button_event("G1", True)

        assert "G1: PRESSED" in widget.event_log.toPlainText()

    def test_on_button_event_released(self, qapp):
        """Test on_button_event displays released state."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        widget.on_button_event("G1", False)

        assert "G1: RELEASED" in widget.event_log.toPlainText()

    def test_on_button_event_when_disabled(self, qapp):
        """Test on_button_event does not display when show_decoded is unchecked."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.show_decoded.setChecked(False)

        widget.on_button_event("G1", True)

        assert widget.event_log.toPlainText() == ""

    def test_on_joystick_event(self, qapp):
        """Test on_joystick_event displays coordinates."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        widget.on_joystick_event(150, 100)

        assert "JOYSTICK: X=150, Y=100" in widget.event_log.toPlainText()

    def test_on_joystick_event_when_disabled(self, qapp):
        """Test on_joystick_event does not display when show_decoded is unchecked."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.show_decoded.setChecked(False)

        widget.on_joystick_event(150, 100)

        assert widget.event_log.toPlainText() == ""

    def test_append_log(self, qapp):
        """Test append_log adds message."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()

        widget.append_log("Test message")

        assert "Test message" in widget.event_log.toPlainText()

    def test_append_log_limits_lines(self, qapp):
        """Test append_log limits lines to max_lines."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.max_lines = 10

        for i in range(20):
            widget.append_log(f"Line {i}")

        lines = widget.event_log.toPlainText().strip().split("\n")
        assert len(lines) <= 10

    def test_clear_log(self, qapp):
        """Test clear_log clears the event log."""
        from g13_linux.gui.views.live_monitor import LiveMonitorWidget

        widget = LiveMonitorWidget()
        widget.append_log("Some message")
        assert widget.event_log.toPlainText() != ""

        widget.clear_log()

        assert widget.event_log.toPlainText() == ""


class TestHardwareControlWidget:
    """Tests for HardwareControlWidget."""

    def test_init(self, qapp):
        """Test HardwareControlWidget initialization."""
        from g13_linux.gui.views.hardware_control import HardwareControlWidget

        widget = HardwareControlWidget()

        assert widget.lcd_text is not None
        assert widget.brightness_slider is not None
        assert widget.brightness_value is not None

    def test_has_signals(self, qapp):
        """Test HardwareControlWidget has required signals."""
        from g13_linux.gui.views.hardware_control import HardwareControlWidget

        widget = HardwareControlWidget()

        assert hasattr(widget, "lcd_text_changed")
        assert hasattr(widget, "backlight_color_changed")
        assert hasattr(widget, "backlight_brightness_changed")

    def test_brightness_slider_range(self, qapp):
        """Test brightness slider has correct range."""
        from g13_linux.gui.views.hardware_control import HardwareControlWidget

        widget = HardwareControlWidget()

        assert widget.brightness_slider.minimum() == 0
        assert widget.brightness_slider.maximum() == 100
        assert widget.brightness_slider.value() == 100

    def test_brightness_slider_updates_label(self, qapp):
        """Test brightness slider updates label."""
        from g13_linux.gui.views.hardware_control import HardwareControlWidget

        widget = HardwareControlWidget()
        widget.brightness_slider.setValue(50)

        assert widget.brightness_value.text() == "50%"

    def test_brightness_changed_signal(self, qapp):
        """Test brightness slider emits signal."""
        from g13_linux.gui.views.hardware_control import HardwareControlWidget

        widget = HardwareControlWidget()
        received = []
        widget.backlight_brightness_changed.connect(lambda v: received.append(v))

        widget.brightness_slider.setValue(75)

        assert 75 in received


class TestProfileManagerWidget:
    """Tests for ProfileManagerWidget."""

    def test_init(self, qapp):
        """Test ProfileManagerWidget initialization."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()

        assert widget.profile_list is not None

    def test_has_signals(self, qapp):
        """Test ProfileManagerWidget has required signals."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()

        assert hasattr(widget, "profile_selected")
        assert hasattr(widget, "profile_saved")
        assert hasattr(widget, "profile_deleted")

    def test_update_profile_list(self, qapp):
        """Test update_profile_list populates list."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        widget.update_profile_list(["profile1", "profile2", "profile3"])

        assert widget.profile_list.count() == 3
        assert widget.profile_list.item(0).text() == "profile1"
        assert widget.profile_list.item(1).text() == "profile2"
        assert widget.profile_list.item(2).text() == "profile3"

    def test_update_profile_list_clears_previous(self, qapp):
        """Test update_profile_list clears previous items."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        widget.update_profile_list(["old1", "old2"])
        widget.update_profile_list(["new1"])

        assert widget.profile_list.count() == 1
        assert widget.profile_list.item(0).text() == "new1"

    def test_update_profile_list_preserves_selection(self, qapp):
        """Test update_profile_list preserves current selection."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        widget.update_profile_list(["profile1", "profile2"])
        widget.profile_list.setCurrentRow(1)  # Select profile2

        widget.update_profile_list(["profile1", "profile2", "profile3"])

        current = widget.profile_list.currentItem()
        assert current is not None
        assert current.text() == "profile2"

    def test_profile_selected_signal(self, qapp):
        """Test clicking profile emits signal."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        widget.update_profile_list(["test_profile"])

        received = []
        widget.profile_selected.connect(lambda name: received.append(name))

        # Simulate click
        item = widget.profile_list.item(0)
        widget.profile_list.itemClicked.emit(item)

        assert "test_profile" in received

    def test_on_new_profile(self, qapp):
        """Test new profile dialog."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        received = []
        widget.profile_selected.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("new_profile", True)
            widget._on_new_profile()

        assert "new_profile" in received

    def test_on_new_profile_cancelled(self, qapp):
        """Test new profile dialog cancelled."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        received = []
        widget.profile_selected.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("", False)
            widget._on_new_profile()

        assert received == []

    def test_on_save_profile(self, qapp):
        """Test save profile emits signal."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        widget.update_profile_list(["existing"])
        widget.profile_list.setCurrentRow(0)

        received = []
        widget.profile_saved.connect(lambda name: received.append(name))

        widget._on_save_profile()

        assert "existing" in received

    def test_on_save_profile_no_selection(self, qapp):
        """Test save profile with no selection opens save as."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        received = []
        widget.profile_saved.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("new_name", True)
            widget._on_save_profile()

        assert "new_name" in received

    def test_on_save_as_profile(self, qapp):
        """Test save as profile dialog."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()
        received = []
        widget.profile_saved.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("saved_as", True)
            widget._on_save_as_profile()

        assert "saved_as" in received

    def test_on_delete_profile(self, qapp):
        """Test delete profile emits signal on confirm."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget
        from PyQt6.QtWidgets import QMessageBox

        widget = ProfileManagerWidget()
        widget.update_profile_list(["to_delete"])
        widget.profile_list.setCurrentRow(0)

        received = []
        widget.profile_deleted.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QMessageBox") as mock_box:
            mock_box.StandardButton.Yes = QMessageBox.StandardButton.Yes
            mock_box.StandardButton.No = QMessageBox.StandardButton.No
            mock_box.question.return_value = QMessageBox.StandardButton.Yes
            widget._on_delete_profile()

        assert "to_delete" in received

    def test_on_delete_profile_cancelled(self, qapp):
        """Test delete profile cancelled."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget
        from PyQt6.QtWidgets import QMessageBox

        widget = ProfileManagerWidget()
        widget.update_profile_list(["to_delete"])
        widget.profile_list.setCurrentRow(0)

        received = []
        widget.profile_deleted.connect(lambda name: received.append(name))

        with patch("g13_linux.gui.views.profile_manager.QMessageBox") as mock_box:
            mock_box.StandardButton.Yes = QMessageBox.StandardButton.Yes
            mock_box.StandardButton.No = QMessageBox.StandardButton.No
            mock_box.question.return_value = QMessageBox.StandardButton.No
            widget._on_delete_profile()

        assert received == []

    def test_on_delete_profile_no_selection(self, qapp):
        """Test delete profile with no selection."""
        from g13_linux.gui.views.profile_manager import ProfileManagerWidget

        widget = ProfileManagerWidget()

        received = []
        widget.profile_deleted.connect(lambda name: received.append(name))

        # Should not raise
        widget._on_delete_profile()

        assert received == []
