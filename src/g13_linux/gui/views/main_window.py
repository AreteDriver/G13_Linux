"""
Main Window

Primary application window for G13LogitechOPS GUI.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .app_profiles import AppProfilesWidget
from .button_mapper import ButtonMapperWidget
from .hardware_control import HardwareControlWidget
from .joystick_settings import JoystickSettingsWidget
from .live_monitor import LiveMonitorWidget
from .macro_editor import MacroEditorWidget
from .profile_manager import ProfileManagerWidget


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("G13LogitechOPS - Configuration Tool v0.2.0")
        self.setMinimumSize(1200, 700)

        # Create widgets
        self.button_mapper = ButtonMapperWidget()
        self.profile_widget = ProfileManagerWidget()
        self.monitor_widget = LiveMonitorWidget()
        self.hardware_widget = HardwareControlWidget()
        self.macro_widget = MacroEditorWidget()
        self.joystick_widget = JoystickSettingsWidget()
        self.app_profiles_widget: AppProfilesWidget | None = None  # Set by controller
        self._tabs: QTabWidget | None = None

        self._init_ui()

    def _init_ui(self):
        """Setup UI layout"""

        # Main splitter (left/right)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side: Button mapper
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.button_mapper)
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        # Right side: Tabs
        self._tabs = QTabWidget()
        self._tabs.addTab(self.profile_widget, "Profiles")
        self._tabs.addTab(self.joystick_widget, "Joystick")
        self._tabs.addTab(self.macro_widget, "Macros")
        self._tabs.addTab(self.hardware_widget, "Hardware")
        self._tabs.addTab(self.monitor_widget, "Monitor")

        splitter.addWidget(self._tabs)
        splitter.setSizes([800, 400])

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - No device connected")

        self.setCentralWidget(splitter)

    def set_status(self, message: str):
        """Update status bar message"""
        self.status_bar.showMessage(message)

    def setup_app_profiles(self, rules_manager, profiles: list[str]):
        """Set up the app profiles widget with the rules manager.

        Called by ApplicationController after initialization.
        """
        from ..models.app_profile_rules import AppProfileRulesManager

        self.app_profiles_widget = AppProfilesWidget(rules_manager, profiles)
        if self._tabs:
            # Insert after Profiles tab
            self._tabs.insertTab(1, self.app_profiles_widget, "App Profiles")
