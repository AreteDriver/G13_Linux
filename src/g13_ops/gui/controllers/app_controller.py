"""
Application Controller

Main orchestrator connecting models to views.
"""

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QMessageBox
from ..models.g13_device import G13Device
from ..models.profile_manager import ProfileManager
from ..models.event_decoder import EventDecoder
from ..models.hardware_controller import HardwareController
from .device_event_controller import DeviceEventThread
from ..widgets.key_selector import KeySelectorDialog


class ApplicationController(QObject):
    """Main application orchestrator - connects models to views"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Models
        self.device = G13Device()
        self.profile_manager = ProfileManager()
        self.event_decoder = EventDecoder()
        self.hardware = HardwareController()

        # State
        self.current_mappings = {}
        self.event_thread = None

        self._connect_signals()

    def _connect_signals(self):
        """Wire up all signals between models and views"""

        # Device events
        self.device.device_connected.connect(self._on_device_connected)
        self.device.device_disconnected.connect(self._on_device_disconnected)
        self.device.raw_event_received.connect(self._on_raw_event)
        self.device.error_occurred.connect(self._on_error)

        # Profile UI
        profile_widget = self.main_window.profile_widget
        profile_widget.profile_selected.connect(self._load_profile)
        profile_widget.profile_saved.connect(self._save_profile)
        profile_widget.profile_deleted.connect(self._delete_profile)

        # Button mapper
        mapper_widget = self.main_window.button_mapper
        mapper_widget.button_clicked.connect(self._assign_key_to_button)

        # Hardware controls
        hw_widget = self.main_window.hardware_widget
        hw_widget.lcd_text_changed.connect(self._update_lcd)
        hw_widget.backlight_color_changed.connect(self._update_backlight_color)
        hw_widget.backlight_brightness_changed.connect(self._update_backlight_brightness)

    def start(self):
        """Initialize application"""
        # Connect to device
        if self.device.connect():
            self.main_window.set_status("G13 device connected")

            # Initialize hardware controller
            if self.device.handle:
                self.hardware.initialize(self.device.handle)

            # Start event thread
            self.event_thread = DeviceEventThread(self.device.handle)
            self.event_thread.event_received.connect(self._on_raw_event)
            self.event_thread.error_occurred.connect(self._on_error)
            self.event_thread.start()
        else:
            self.main_window.set_status("No G13 device found")

        # Load available profiles
        profiles = self.profile_manager.list_profiles()
        self.main_window.profile_widget.update_profile_list(profiles)

        # Load example profile if exists
        if 'example' in profiles:
            self._load_profile('example')

    @pyqtSlot(bytes)
    def _on_raw_event(self, data: bytes):
        """Handle raw HID event from device"""
        # Send to live monitor
        self.main_window.monitor_widget.on_raw_event(data)

        # Decode event
        try:
            state = self.event_decoder.decode_report(data)
            pressed, released = self.event_decoder.get_button_changes(state)

            # Update button highlights
            for button_id in pressed:
                self.main_window.button_mapper.highlight_button(button_id, True)
                self.main_window.monitor_widget.on_button_event(button_id, True)

            for button_id in released:
                self.main_window.button_mapper.highlight_button(button_id, False)
                self.main_window.monitor_widget.on_button_event(button_id, False)

        except Exception as e:
            # Debug: show decoder errors
            print(f"Decoder error: {e}")

    @pyqtSlot()
    def _on_device_connected(self):
        """Handle device connection"""
        self.main_window.set_status("G13 device connected")

    @pyqtSlot()
    def _on_device_disconnected(self):
        """Handle device disconnection"""
        self.main_window.set_status("G13 device disconnected")
        if self.event_thread:
            self.event_thread.stop()

    @pyqtSlot(str)
    def _on_error(self, message: str):
        """Handle errors"""
        self.main_window.set_status(f"Error: {message}")
        print(f"ERROR: {message}")

    @pyqtSlot(str)
    def _load_profile(self, profile_name: str):
        """Load a profile and update UI"""
        try:
            profile = self.profile_manager.load_profile(profile_name)
            self.current_mappings = profile.mappings.copy()

            # Update button mapper
            for button_id, key_name in profile.mappings.items():
                self.main_window.button_mapper.set_button_mapping(button_id, key_name)

            self.main_window.set_status(f"Loaded profile: {profile_name}")

        except Exception as e:
            self._on_error(f"Failed to load profile: {e}")
            QMessageBox.warning(
                self.main_window,
                "Profile Error",
                f"Failed to load profile '{profile_name}':\n{e}"
            )

    @pyqtSlot(str)
    def _save_profile(self, profile_name: str):
        """Save current configuration as profile"""
        try:
            # Create or update profile
            if self.profile_manager.profile_exists(profile_name):
                profile = self.profile_manager.load_profile(profile_name)
            else:
                profile = self.profile_manager.create_profile(profile_name)

            profile.mappings = self.current_mappings.copy()
            self.profile_manager.save_profile(profile, profile_name)

            # Refresh profile list
            profiles = self.profile_manager.list_profiles()
            self.main_window.profile_widget.update_profile_list(profiles)

            self.main_window.set_status(f"Saved profile: {profile_name}")

        except Exception as e:
            self._on_error(f"Failed to save profile: {e}")
            QMessageBox.warning(
                self.main_window,
                "Profile Error",
                f"Failed to save profile '{profile_name}':\n{e}"
            )

    @pyqtSlot(str)
    def _delete_profile(self, profile_name: str):
        """Delete a profile"""
        try:
            self.profile_manager.delete_profile(profile_name)

            # Refresh profile list
            profiles = self.profile_manager.list_profiles()
            self.main_window.profile_widget.update_profile_list(profiles)

            self.main_window.set_status(f"Deleted profile: {profile_name}")

        except Exception as e:
            self._on_error(f"Failed to delete profile: {e}")

    @pyqtSlot(str)
    def _assign_key_to_button(self, button_id: str):
        """Open key selector for button"""
        dialog = KeySelectorDialog(button_id, self.main_window)
        if dialog.exec():
            key_name = dialog.selected_key
            if key_name:
                self.current_mappings[button_id] = key_name
                self.main_window.button_mapper.set_button_mapping(button_id, key_name)
                self.main_window.set_status(f"Mapped {button_id} to {key_name}")

    @pyqtSlot(str)
    def _update_lcd(self, text: str):
        """Send text to LCD"""
        try:
            self.hardware.set_lcd_text(text)
            self.main_window.set_status("LCD updated")
        except Exception as e:
            self._on_error(f"LCD error: {e}")

    @pyqtSlot(str)
    def _update_backlight_color(self, color_hex: str):
        """Update backlight color"""
        try:
            self.hardware.set_backlight_color(color_hex)
            self.main_window.set_status(f"Backlight color: {color_hex}")
        except Exception as e:
            self._on_error(f"Backlight error: {e}")

    @pyqtSlot(int)
    def _update_backlight_brightness(self, brightness: int):
        """Update backlight brightness"""
        try:
            self.hardware.set_backlight_brightness(brightness)
            self.main_window.set_status(f"Backlight brightness: {brightness}%")
        except Exception as e:
            self._on_error(f"Backlight error: {e}")

    def shutdown(self):
        """Cleanup on application exit"""
        if self.event_thread:
            self.event_thread.stop()
        if self.device.is_connected:
            self.device.disconnect()
