"""Tests for MacroEditorWidget."""

import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_dependencies():
    """Mock external dependencies for MacroEditorWidget."""
    with patch("g13_linux.gui.views.macro_editor.MacroManager") as mock_mgr, \
         patch("g13_linux.gui.views.macro_editor.MacroRecorder") as mock_rec, \
         patch("g13_linux.gui.views.macro_editor.MacroPlayer") as mock_player:

        mock_mgr_instance = MagicMock()
        mock_mgr_instance.list_macros.return_value = []
        mock_mgr_instance.list_macro_summaries.return_value = []
        mock_mgr.return_value = mock_mgr_instance

        mock_rec_instance = MagicMock()
        mock_rec_instance.state_changed = MagicMock()
        mock_rec_instance.recording_complete = MagicMock()
        mock_rec.return_value = mock_rec_instance

        mock_player_instance = MagicMock()
        mock_player_instance.playback_started = MagicMock()
        mock_player_instance.playback_complete = MagicMock()
        mock_player_instance.playback_error = MagicMock()
        mock_player.return_value = mock_player_instance

        yield {
            "manager_cls": mock_mgr,
            "manager": mock_mgr_instance,
            "recorder_cls": mock_rec,
            "recorder": mock_rec_instance,
            "player_cls": mock_player,
            "player": mock_player_instance,
        }


class TestMacroListItem:
    """Tests for MacroListItem."""

    def test_create_item(self, qapp):
        """Test creating a MacroListItem."""
        from g13_linux.gui.views.macro_editor import MacroListItem

        item = MacroListItem("macro-123", "Test Macro", 5)

        assert item.macro_id == "macro-123"
        assert "Test Macro" in item.text()
        assert "5 steps" in item.text()


class TestMacroEditorWidget:
    """Tests for MacroEditorWidget."""

    def test_init(self, qapp, mock_dependencies):
        """Test MacroEditorWidget initialization."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.macro_manager is not None
        assert widget.macro_recorder is not None
        assert widget.macro_player is not None
        assert widget._current_macro is None

    def test_has_signals(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has required signals."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "macro_assigned")
        assert hasattr(widget, "macro_saved")

    def test_has_ui_elements(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has UI elements."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.macro_list is not None
        assert widget.name_edit is not None
        assert widget.description_edit is not None
        assert widget.hotkey_edit is not None
        assert widget.steps_list is not None

    def test_has_buttons(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has buttons."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.new_btn is not None
        assert widget.record_btn is not None
        assert widget.delete_btn is not None

    def test_delete_btn_disabled_initially(self, qapp, mock_dependencies):
        """Test delete button is disabled when no macro selected."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.delete_btn.isEnabled() is False

    def test_refresh_macro_list(self, qapp, mock_dependencies):
        """Test refresh_macro_list updates list."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        # Set up mock to return summaries before widget creation
        mock_dependencies["manager"].list_macro_summaries.return_value = [
            {"id": "macro-1", "name": "Test", "step_count": 3}
        ]

        widget = MacroEditorWidget()

        assert widget.macro_list.count() == 1

    def test_create_new_macro(self, qapp, mock_dependencies):
        """Test creating a new macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget
        from g13_linux.gui.models.macro_types import Macro

        # Set up mock to return a new macro
        new_macro = MagicMock(spec=Macro)
        new_macro.id = "new-macro"
        new_macro.name = "New Macro"
        mock_dependencies["manager"].create_macro.return_value = new_macro
        mock_dependencies["manager"].list_macro_summaries.return_value = []

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("New Macro", True)
            widget._create_new_macro()

        # Macro should be created
        mock_dependencies["manager"].create_macro.assert_called_once_with("New Macro")

    def test_create_new_macro_cancelled(self, qapp, mock_dependencies):
        """Test cancelling new macro creation."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("", False)
            widget._create_new_macro()

        # Macro should not be saved
        mock_dependencies["manager"].save_macro.assert_not_called()

    def test_delete_macro_no_selection(self, qapp, mock_dependencies):
        """Test delete macro with no selection."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        # Should not raise
        widget._delete_macro()

        mock_dependencies["manager"].delete_macro.assert_not_called()

    def test_on_macro_selected_none(self, qapp, mock_dependencies):
        """Test selecting no macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._on_macro_selected(None, None)

        assert widget._current_macro is None
        assert widget.delete_btn.isEnabled() is False

    def test_on_property_changed_no_macro(self, qapp, mock_dependencies):
        """Test property change with no current macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._on_property_changed()


class TestMacroEditorPlayback:
    """Tests for playback controls."""

    def test_has_playback_controls(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has playback controls."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "play_btn")
        assert hasattr(widget, "stop_btn")

    def test_has_playback_settings(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has playback settings."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "speed_spin")
        assert hasattr(widget, "repeat_spin")
        assert hasattr(widget, "playback_mode_combo")


class TestMacroEditorSteps:
    """Tests for step management."""

    def test_insert_delay_no_macro(self, qapp, mock_dependencies):
        """Test insert delay with no current macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._insert_delay()

    def test_delete_step_no_selection(self, qapp, mock_dependencies):
        """Test delete step with no selection."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        # Should not raise
        widget._delete_step()


class TestMacroEditorRecordDialog:
    """Tests for record dialog integration."""

    def test_open_record_dialog(self, qapp, mock_dependencies):
        """Test opening record dialog."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.MacroRecordDialog") as mock_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = False
            mock_dialog.return_value = mock_dialog_instance

            widget._open_record_dialog()

            mock_dialog.assert_called_once()
