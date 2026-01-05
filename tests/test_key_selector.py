"""Tests for KeySelectorDialog widget."""

import pytest
from PyQt6.QtCore import Qt


class TestKeySelectorDialog:
    """Tests for KeySelectorDialog."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create KeySelectorDialog instance."""
        from g13_linux.gui.widgets.key_selector import KeySelectorDialog

        dlg = KeySelectorDialog("G5")
        qtbot.addWidget(dlg)
        return dlg

    def test_init_button_id(self, dialog):
        """Test dialog stores button ID."""
        assert dialog.button_id == "G5"

    def test_init_no_selection(self, dialog):
        """Test dialog starts with no selection."""
        assert dialog.selected_key is None

    def test_window_title(self, dialog):
        """Test window title includes button ID."""
        assert "G5" in dialog.windowTitle()

    def test_minimum_size(self, dialog):
        """Test minimum size is set."""
        assert dialog.minimumWidth() >= 500
        assert dialog.minimumHeight() >= 400

    def test_has_tab_widget(self, dialog):
        """Test dialog has tab widget."""
        from PyQt6.QtWidgets import QTabWidget

        tabs = dialog.findChild(QTabWidget)
        assert tabs is not None

    def test_has_three_tabs(self, dialog):
        """Test dialog has three tabs."""
        from PyQt6.QtWidgets import QTabWidget

        tabs = dialog.findChild(QTabWidget)
        assert tabs.count() == 3

    def test_tab_names(self, dialog):
        """Test tab names are correct."""
        from PyQt6.QtWidgets import QTabWidget

        tabs = dialog.findChild(QTabWidget)
        assert tabs.tabText(0) == "Common Keys"
        assert tabs.tabText(1) == "Function Keys"
        assert tabs.tabText(2) == "All Keys"

    def test_common_keys_tab_has_keys(self, dialog):
        """Test common keys tab has expected keys."""
        from PyQt6.QtWidgets import QListWidget, QTabWidget

        tabs = dialog.findChild(QTabWidget)
        common_tab = tabs.widget(0)
        list_widget = common_tab.findChild(QListWidget)

        items = [list_widget.item(i).text() for i in range(list_widget.count())]
        assert "KEY_1" in items
        assert "KEY_A" in items
        assert "KEY_SPACE" in items
        assert "KEY_LEFTCTRL" in items

    def test_function_keys_tab_has_f_keys(self, dialog):
        """Test function keys tab has F1-F24."""
        from PyQt6.QtWidgets import QListWidget, QTabWidget

        tabs = dialog.findChild(QTabWidget)
        fn_tab = tabs.widget(1)
        list_widget = fn_tab.findChild(QListWidget)

        items = [list_widget.item(i).text() for i in range(list_widget.count())]
        assert "KEY_F1" in items
        assert "KEY_F12" in items
        assert "KEY_F24" in items
        assert list_widget.count() == 24

    def test_all_keys_tab_has_many_keys(self, dialog):
        """Test all keys tab has many keys from evdev."""
        from PyQt6.QtWidgets import QListWidget, QTabWidget

        tabs = dialog.findChild(QTabWidget)
        all_tab = tabs.widget(2)
        list_widget = all_tab.findChild(QListWidget)

        # Should have many keys from evdev
        assert list_widget.count() > 100

    def test_has_ok_button(self, dialog):
        """Test dialog has OK button."""
        from PyQt6.QtWidgets import QPushButton

        buttons = dialog.findChildren(QPushButton)
        ok_btn = next((b for b in buttons if b.text() == "OK"), None)
        assert ok_btn is not None

    def test_has_cancel_button(self, dialog):
        """Test dialog has Cancel button."""
        from PyQt6.QtWidgets import QPushButton

        buttons = dialog.findChildren(QPushButton)
        cancel_btn = next((b for b in buttons if b.text() == "Cancel"), None)
        assert cancel_btn is not None

    def test_has_clear_mapping_button(self, dialog):
        """Test dialog has Clear Mapping button."""
        from PyQt6.QtWidgets import QPushButton

        buttons = dialog.findChildren(QPushButton)
        clear_btn = next((b for b in buttons if b.text() == "Clear Mapping"), None)
        assert clear_btn is not None

    def test_select_key_from_list(self, dialog, qtbot):
        """Test selecting a key from list."""
        from PyQt6.QtWidgets import QListWidget, QTabWidget

        tabs = dialog.findChild(QTabWidget)
        common_tab = tabs.widget(0)
        list_widget = common_tab.findChild(QListWidget)

        # Click on first item
        item = list_widget.item(0)
        list_widget.setCurrentItem(item)
        qtbot.mouseClick(
            list_widget.viewport(),
            Qt.MouseButton.LeftButton,
            pos=list_widget.visualItemRect(item).center(),
        )

        assert dialog.selected_key is not None

    def test_clear_mapping_sets_reserved(self, dialog, qtbot):
        """Test Clear Mapping sets KEY_RESERVED."""
        from PyQt6.QtWidgets import QPushButton

        buttons = dialog.findChildren(QPushButton)
        clear_btn = next(b for b in buttons if b.text() == "Clear Mapping")

        # Need to block accept() from closing
        dialog.done = lambda x: None
        qtbot.mouseClick(clear_btn, Qt.MouseButton.LeftButton)

        assert dialog.selected_key == "KEY_RESERVED"

    def test_search_filters_list(self, dialog, qtbot):
        """Test search box filters key list."""
        from PyQt6.QtWidgets import QLineEdit, QListWidget, QTabWidget

        tabs = dialog.findChild(QTabWidget)
        common_tab = tabs.widget(0)
        list_widget = common_tab.findChild(QListWidget)
        search_box = common_tab.findChild(QLineEdit)

        initial_count = list_widget.count()

        # Type in search box to filter
        search_box.setText("CTRL")
        qtbot.wait(50)  # Allow filter to apply

        # Should have fewer items
        assert list_widget.count() < initial_count
        # All items should contain CTRL
        for i in range(list_widget.count()):
            assert "CTRL" in list_widget.item(i).text()

    def test_different_button_id(self, qtbot):
        """Test dialog with different button ID."""
        from g13_linux.gui.widgets.key_selector import KeySelectorDialog

        dlg = KeySelectorDialog("G22")
        qtbot.addWidget(dlg)

        assert dlg.button_id == "G22"
        assert "G22" in dlg.windowTitle()
