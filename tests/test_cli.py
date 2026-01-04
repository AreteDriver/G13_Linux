"""Tests for CLI commands."""

import pytest
import sys
from unittest.mock import MagicMock, patch

from g13_linux.cli import (
    COLOR_PRESETS,
    cmd_run,
    cmd_lcd,
    cmd_color,
    cmd_profile,
    main,
)


class TestColorPresets:
    """Tests for color presets."""

    def test_has_common_colors(self):
        """Test COLOR_PRESETS has common colors."""
        assert "red" in COLOR_PRESETS
        assert "green" in COLOR_PRESETS
        assert "blue" in COLOR_PRESETS
        assert "white" in COLOR_PRESETS
        assert "off" in COLOR_PRESETS

    def test_red_is_correct(self):
        """Test red preset is correct RGB."""
        assert COLOR_PRESETS["red"] == (255, 0, 0)

    def test_green_is_correct(self):
        """Test green preset is correct RGB."""
        assert COLOR_PRESETS["green"] == (0, 255, 0)

    def test_blue_is_correct(self):
        """Test blue preset is correct RGB."""
        assert COLOR_PRESETS["blue"] == (0, 0, 255)

    def test_off_is_black(self):
        """Test off preset is black (0,0,0)."""
        assert COLOR_PRESETS["off"] == (0, 0, 0)


class TestCmdRun:
    """Tests for cmd_run command."""

    def test_cmd_run_opens_device(self, capsys):
        """Test cmd_run opens G13 device."""
        mock_handle = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_handle) as mock_open, \
             patch("g13_linux.device.read_event", side_effect=KeyboardInterrupt), \
             patch("g13_linux.mapper.G13Mapper"):
            args = MagicMock()
            cmd_run(args)

        mock_open.assert_called_once()
        mock_handle.close.assert_called_once()

    def test_cmd_run_handles_device_error(self, capsys):
        """Test cmd_run handles device open error."""
        with patch("g13_linux.device.open_g13", side_effect=Exception("Device not found")):
            args = MagicMock()

            with pytest.raises(SystemExit) as exc_info:
                cmd_run(args)

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Could not open G13" in captured.err

    def test_cmd_run_processes_events(self, capsys):
        """Test cmd_run processes events until KeyboardInterrupt."""
        mock_handle = MagicMock()
        mock_mapper = MagicMock()

        call_count = [0]
        def fake_read_event(h):
            call_count[0] += 1
            if call_count[0] >= 3:
                raise KeyboardInterrupt
            return b"\x00" * 8

        with patch("g13_linux.device.open_g13", return_value=mock_handle), \
             patch("g13_linux.device.read_event", side_effect=fake_read_event), \
             patch("g13_linux.mapper.G13Mapper", return_value=mock_mapper):
            args = MagicMock()
            cmd_run(args)

        assert mock_mapper.handle_raw_report.call_count == 2


class TestCmdLcd:
    """Tests for cmd_lcd command."""

    def test_cmd_lcd_clear(self, capsys):
        """Test cmd_lcd with --clear flag."""
        mock_device = MagicMock()
        mock_lcd = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.lcd.G13LCD", return_value=mock_lcd):
            args = MagicMock()
            args.clear = True
            args.text = None

            cmd_lcd(args)

        mock_lcd.clear.assert_called_once()
        mock_device.close.assert_called_once()

    def test_cmd_lcd_with_text(self, capsys):
        """Test cmd_lcd with text."""
        mock_device = MagicMock()
        mock_lcd = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.lcd.G13LCD", return_value=mock_lcd):
            args = MagicMock()
            args.clear = False
            args.text = ["Hello", "World"]

            cmd_lcd(args)

        mock_lcd.clear.assert_called_once()
        mock_lcd.write_text_centered.assert_called_once_with("Hello World")
        mock_device.close.assert_called_once()

    def test_cmd_lcd_no_text_no_clear(self, capsys):
        """Test cmd_lcd with no text and no --clear exits with error."""
        mock_device = MagicMock()
        mock_lcd = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.lcd.G13LCD", return_value=mock_lcd):
            args = MagicMock()
            args.clear = False
            args.text = []

            with pytest.raises(SystemExit) as exc_info:
                cmd_lcd(args)

            assert exc_info.value.code == 1

    def test_cmd_lcd_device_error(self, capsys):
        """Test cmd_lcd handles device open error."""
        with patch("g13_linux.device.open_g13", side_effect=Exception("Device not found")):
            args = MagicMock()
            args.clear = True
            args.text = None

            with pytest.raises(SystemExit) as exc_info:
                cmd_lcd(args)

            assert exc_info.value.code == 1


class TestCmdColor:
    """Tests for cmd_color command."""

    def test_cmd_color_preset(self, capsys):
        """Test cmd_color with preset name."""
        mock_device = MagicMock()
        mock_backlight = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.backlight.G13Backlight", return_value=mock_backlight):
            args = MagicMock()
            args.color = "red"

            cmd_color(args)

        mock_backlight.set_color.assert_called_once_with(255, 0, 0)
        mock_device.close.assert_called_once()

    def test_cmd_color_hex_without_hash(self, capsys):
        """Test cmd_color with hex color without #."""
        mock_device = MagicMock()
        mock_backlight = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.backlight.G13Backlight", return_value=mock_backlight):
            args = MagicMock()
            args.color = "FF8000"

            cmd_color(args)

        mock_backlight.set_color.assert_called_once_with(255, 128, 0)

    def test_cmd_color_hex_with_hash(self, capsys):
        """Test cmd_color with hex color with #."""
        mock_device = MagicMock()
        mock_backlight = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.backlight.G13Backlight", return_value=mock_backlight):
            args = MagicMock()
            args.color = "#00FF80"

            cmd_color(args)

        mock_backlight.set_color.assert_called_once_with(0, 255, 128)

    def test_cmd_color_rgb_values(self, capsys):
        """Test cmd_color with RGB comma-separated values."""
        mock_device = MagicMock()
        mock_backlight = MagicMock()

        with patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.backlight.G13Backlight", return_value=mock_backlight):
            args = MagicMock()
            args.color = "100,200,50"

            cmd_color(args)

        mock_backlight.set_color.assert_called_once_with(100, 200, 50)

    def test_cmd_color_invalid(self, capsys):
        """Test cmd_color with invalid color."""
        args = MagicMock()
        args.color = "invalid_color"

        with pytest.raises(SystemExit) as exc_info:
            cmd_color(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid color" in captured.err

    def test_cmd_color_device_error(self, capsys):
        """Test cmd_color handles device open error."""
        with patch("g13_linux.device.open_g13", side_effect=Exception("Device not found")):
            args = MagicMock()
            args.color = "red"

            with pytest.raises(SystemExit) as exc_info:
                cmd_color(args)

            assert exc_info.value.code == 1


class TestCmdProfile:
    """Tests for cmd_profile command."""

    def test_cmd_profile_list_with_profiles(self, capsys):
        """Test profile list with profiles."""
        mock_pm = MagicMock()
        mock_pm.list_profiles.return_value = ["profile1", "profile2"]

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "list"

            cmd_profile(args)

        captured = capsys.readouterr()
        assert "profile1" in captured.out
        assert "profile2" in captured.out

    def test_cmd_profile_list_empty(self, capsys):
        """Test profile list with no profiles."""
        mock_pm = MagicMock()
        mock_pm.list_profiles.return_value = []

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "list"

            cmd_profile(args)

        captured = capsys.readouterr()
        assert "No profiles found" in captured.out

    def test_cmd_profile_show(self, capsys):
        """Test profile show command."""
        mock_pm = MagicMock()
        mock_profile = MagicMock()
        mock_profile.name = "test_profile"
        mock_profile.description = "Test description"
        mock_profile.backlight = {"color": "#FF0000"}
        mock_profile.lcd = "Hello"
        mock_profile.mappings = {"G1": "a", "G2": "b"}
        mock_pm.load_profile.return_value = mock_profile

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "show"
            args.name = "test_profile"

            cmd_profile(args)

        captured = capsys.readouterr()
        assert "test_profile" in captured.out
        assert "Test description" in captured.out

    def test_cmd_profile_show_not_found(self, capsys):
        """Test profile show with non-existent profile."""
        mock_pm = MagicMock()
        mock_pm.load_profile.side_effect = FileNotFoundError()

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "show"
            args.name = "missing"

            with pytest.raises(SystemExit) as exc_info:
                cmd_profile(args)

            assert exc_info.value.code == 1

    def test_cmd_profile_load(self, capsys):
        """Test profile load command."""
        mock_pm = MagicMock()
        mock_profile = MagicMock()
        mock_profile.name = "test_profile"
        mock_profile.backlight = {"color": "#FF0000"}
        mock_pm.load_profile.return_value = mock_profile

        mock_device = MagicMock()
        mock_backlight = MagicMock()

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm), \
             patch("g13_linux.device.open_g13", return_value=mock_device), \
             patch("g13_linux.hardware.backlight.G13Backlight", return_value=mock_backlight):
            args = MagicMock()
            args.profile_cmd = "load"
            args.name = "test_profile"

            cmd_profile(args)

        mock_backlight.set_color.assert_called_once_with(255, 0, 0)

    def test_cmd_profile_load_no_device(self, capsys):
        """Test profile load when device not available."""
        mock_pm = MagicMock()
        mock_profile = MagicMock()
        mock_profile.name = "test_profile"
        mock_profile.backlight = {"color": "#FF0000"}
        mock_pm.load_profile.return_value = mock_profile

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm), \
             patch("g13_linux.device.open_g13", side_effect=Exception("No device")):
            args = MagicMock()
            args.profile_cmd = "load"
            args.name = "test_profile"

            # Should not raise, just print note
            cmd_profile(args)

        captured = capsys.readouterr()
        assert "Could not apply to device" in captured.out

    def test_cmd_profile_create(self, capsys):
        """Test profile create command."""
        mock_pm = MagicMock()
        mock_pm.profile_exists.return_value = False
        mock_profile = MagicMock()
        mock_pm.create_profile.return_value = mock_profile

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "create"
            args.name = "new_profile"

            cmd_profile(args)

        mock_pm.create_profile.assert_called_once_with("new_profile")
        mock_pm.save_profile.assert_called_once_with(mock_profile)

    def test_cmd_profile_create_exists(self, capsys):
        """Test profile create when profile already exists."""
        mock_pm = MagicMock()
        mock_pm.profile_exists.return_value = True

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "create"
            args.name = "existing"

            with pytest.raises(SystemExit) as exc_info:
                cmd_profile(args)

            assert exc_info.value.code == 1

    def test_cmd_profile_delete(self, capsys):
        """Test profile delete command."""
        mock_pm = MagicMock()

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "delete"
            args.name = "to_delete"

            cmd_profile(args)

        mock_pm.delete_profile.assert_called_once_with("to_delete")

    def test_cmd_profile_delete_not_found(self, capsys):
        """Test profile delete with non-existent profile."""
        mock_pm = MagicMock()
        mock_pm.delete_profile.side_effect = FileNotFoundError()

        with patch("g13_linux.gui.models.profile_manager.ProfileManager", return_value=mock_pm):
            args = MagicMock()
            args.profile_cmd = "delete"
            args.name = "missing"

            with pytest.raises(SystemExit) as exc_info:
                cmd_profile(args)

            assert exc_info.value.code == 1


class TestMain:
    """Tests for main() entry point."""

    def test_main_version(self, capsys):
        """Test --version flag."""
        with patch.object(sys, "argv", ["g13-linux", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    def test_main_no_args_runs_daemon(self):
        """Test main with no args runs daemon."""
        with patch.object(sys, "argv", ["g13-linux"]), \
             patch("g13_linux.cli.cmd_run") as mock_run:
            mock_run.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                main()

            mock_run.assert_called_once()

    def test_main_lcd_command(self):
        """Test main with lcd command."""
        with patch.object(sys, "argv", ["g13-linux", "lcd", "--clear"]), \
             patch("g13_linux.cli.cmd_lcd") as mock_lcd:
            mock_lcd.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                main()

            mock_lcd.assert_called_once()

    def test_main_color_command(self):
        """Test main with color command."""
        with patch.object(sys, "argv", ["g13-linux", "color", "red"]), \
             patch("g13_linux.cli.cmd_color") as mock_color:
            mock_color.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                main()

            mock_color.assert_called_once()

    def test_main_profile_list_command(self):
        """Test main with profile list command."""
        with patch.object(sys, "argv", ["g13-linux", "profile", "list"]), \
             patch("g13_linux.cli.cmd_profile") as mock_profile:
            mock_profile.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                main()

            mock_profile.assert_called_once()

    def test_main_profile_no_subcommand(self, capsys):
        """Test main with profile but no subcommand."""
        with patch.object(sys, "argv", ["g13-linux", "profile"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
