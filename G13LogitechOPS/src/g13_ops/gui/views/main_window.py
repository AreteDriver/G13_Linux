"""
Main Window

Primary application window for G13LogitechOPS GUI.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSplitter,
    QTabWidget,
    QStatusBar,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from .button_mapper import ButtonMapperWidget
from .profile_manager import ProfileManagerWidget
from .live_monitor import LiveMonitorWidget
from .hardware_control import HardwareControlWidget
from .macro_editor import MacroEditorWidget


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
        tabs = QTabWidget()
        tabs.addTab(self.profile_widget, "Profiles")
        tabs.addTab(self.macro_widget, "Macros")
        tabs.addTab(self.hardware_widget, "Hardware")
        tabs.addTab(self.monitor_widget, "Monitor")

        splitter.addWidget(tabs)
        splitter.setSizes([800, 400])

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - No device connected")

        self.setCentralWidget(splitter)

    def set_status(self, message: str):
        """Update status bar message"""
        self.status_bar.showMessage(message)
