"""
Profile Manager Widget

UI for managing G13 button configuration profiles.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QInputDialog,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSignal, Qt


class ProfileManagerWidget(QWidget):
    """Profile management UI"""

    profile_selected = pyqtSignal(str)  # Profile name
    profile_saved = pyqtSignal(str)  # Profile name
    profile_deleted = pyqtSignal(str)  # Profile name

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Profile Management")
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(header)

        # Profile list
        self.profile_list = QListWidget()
        self.profile_list.itemClicked.connect(
            lambda item: self.profile_selected.emit(item.text())
        )
        layout.addWidget(self.profile_list)

        # Buttons
        btn_layout = QHBoxLayout()

        new_btn = QPushButton("New")
        new_btn.clicked.connect(self._on_new_profile)
        btn_layout.addWidget(new_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save_profile)
        btn_layout.addWidget(save_btn)

        save_as_btn = QPushButton("Save As")
        save_as_btn.clicked.connect(self._on_save_as_profile)
        btn_layout.addWidget(save_as_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._on_delete_profile)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def update_profile_list(self, profiles: list):
        """Update the profile list"""
        current_selection = None
        if self.profile_list.currentItem():
            current_selection = self.profile_list.currentItem().text()

        self.profile_list.clear()
        self.profile_list.addItems(profiles)

        # Restore selection if possible
        if current_selection and current_selection in profiles:
            items = self.profile_list.findItems(
                current_selection, Qt.MatchFlag.MatchExactly
            )
            if items:
                self.profile_list.setCurrentItem(items[0])

    def _on_new_profile(self):
        """Create new profile"""
        name, ok = QInputDialog.getText(self, "New Profile", "Profile name:")
        if ok and name:
            self.profile_selected.emit(name)

    def _on_save_profile(self):
        """Save current profile"""
        current = self.profile_list.currentItem()
        if current:
            self.profile_saved.emit(current.text())
        else:
            self._on_save_as_profile()

    def _on_save_as_profile(self):
        """Save as new profile"""
        name, ok = QInputDialog.getText(self, "Save As", "Profile name:")
        if ok and name:
            self.profile_saved.emit(name)

    def _on_delete_profile(self):
        """Delete selected profile"""
        current = self.profile_list.currentItem()
        if current:
            reply = QMessageBox.question(
                self,
                "Delete Profile",
                f'Delete profile "{current.text()}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.profile_deleted.emit(current.text())
