"""
Key Selector Dialog

Dialog for selecting keyboard key mappings.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QTabWidget,
    QWidget,
)
from evdev import ecodes


class KeySelectorDialog(QDialog):
    """Dialog for selecting key mappings"""

    def __init__(self, button_id: str, parent=None):
        super().__init__(parent)
        self.button_id = button_id
        self.selected_key = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(f"Map {self.button_id}")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()

        # Title
        title = QLabel(f"Select key mapping for {self.button_id}")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Tabs for different key categories
        tabs = QTabWidget()

        # Tab 1: Common keys
        common_keys = [
            "KEY_1",
            "KEY_2",
            "KEY_3",
            "KEY_4",
            "KEY_5",
            "KEY_A",
            "KEY_B",
            "KEY_C",
            "KEY_D",
            "KEY_E",
            "KEY_F",
            "KEY_ENTER",
            "KEY_SPACE",
            "KEY_ESC",
            "KEY_TAB",
            "KEY_LEFTCTRL",
            "KEY_LEFTSHIFT",
            "KEY_LEFTALT",
            "KEY_LEFTMETA",
        ]
        tabs.addTab(self._create_key_list(common_keys), "Common Keys")

        # Tab 2: Function keys
        fn_keys = [f"KEY_F{i}" for i in range(1, 25)]
        tabs.addTab(self._create_key_list(fn_keys), "Function Keys")

        # Tab 3: All keys
        all_keys = sorted([name for name in dir(ecodes) if name.startswith("KEY_")])
        tabs.addTab(self._create_key_list(all_keys), "All Keys")

        layout.addWidget(tabs)

        # Buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        clear_btn = QPushButton("Clear Mapping")
        clear_btn.clicked.connect(self._clear_mapping)

        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _create_key_list(self, keys):
        """Create a searchable key list widget"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Search box
        search = QLineEdit()
        search.setPlaceholderText("Search keys...")
        layout.addWidget(search)

        # List
        list_widget = QListWidget()
        list_widget.addItems(keys)
        list_widget.itemDoubleClicked.connect(self._on_key_selected)
        list_widget.itemClicked.connect(self._on_key_selected)
        layout.addWidget(list_widget)

        # Search functionality
        def filter_list(text):
            list_widget.clear()
            filtered = [k for k in keys if text.upper() in k]
            list_widget.addItems(filtered)

        search.textChanged.connect(filter_list)

        widget.setLayout(layout)
        return widget

    def _on_key_selected(self, item):
        """Handle key selection"""
        self.selected_key = item.text()

    def _clear_mapping(self):
        """Clear the mapping"""
        self.selected_key = "KEY_RESERVED"
        self.accept()
