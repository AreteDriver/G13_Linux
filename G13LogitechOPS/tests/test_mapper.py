"""Tests for G13 button mapper."""

from unittest.mock import MagicMock, patch
from evdev import ecodes as e


class TestMapperParsing:
    """Test mapping format parsing without hardware."""

    def test_parse_simple_mapping(self):
        """Parse simple KEY_* string format."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            keycodes = mapper._parse_mapping("KEY_A")

            assert keycodes == [e.KEY_A]

    def test_parse_combo_mapping(self):
        """Parse combo format with multiple keys."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            keycodes = mapper._parse_mapping(
                {"keys": ["KEY_LEFTCTRL", "KEY_B"], "label": "Test combo"}
            )

            assert keycodes == [e.KEY_LEFTCTRL, e.KEY_B]

    def test_parse_invalid_key_returns_empty(self):
        """Invalid key names return empty list."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            keycodes = mapper._parse_mapping("KEY_INVALID_NOT_REAL")

            assert keycodes == []

    def test_parse_empty_combo_returns_empty(self):
        """Empty combo returns empty list."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            keycodes = mapper._parse_mapping({"keys": [], "label": "Empty"})

            assert keycodes == []


class TestProfileLoading:
    """Test loading profiles into mapper."""

    def test_load_simple_profile(self):
        """Load profile with simple key mappings."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            profile = {
                "mappings": {
                    "G1": "KEY_1",
                    "G2": "KEY_2",
                }
            }
            mapper.load_profile(profile)

            assert "G1" in mapper.button_map
            assert mapper.button_map["G1"] == [e.KEY_1]
            assert mapper.button_map["G2"] == [e.KEY_2]

    def test_load_combo_profile(self):
        """Load profile with key combinations."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            profile = {
                "mappings": {
                    "G1": {"keys": ["KEY_LEFTCTRL", "KEY_C"], "label": "Copy"},
                    "G2": {"keys": ["KEY_LEFTCTRL", "KEY_V"], "label": "Paste"},
                }
            }
            mapper.load_profile(profile)

            assert mapper.button_map["G1"] == [e.KEY_LEFTCTRL, e.KEY_C]
            assert mapper.button_map["G2"] == [e.KEY_LEFTCTRL, e.KEY_V]

    def test_load_mixed_profile(self):
        """Load profile with both simple and combo mappings."""
        with patch("g13_ops.mapper.UInput"):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            profile = {
                "mappings": {
                    "G1": "KEY_F1",
                    "G2": {"keys": ["KEY_LEFTALT", "KEY_F4"], "label": "Close"},
                }
            }
            mapper.load_profile(profile)

            assert mapper.button_map["G1"] == [e.KEY_F1]
            assert mapper.button_map["G2"] == [e.KEY_LEFTALT, e.KEY_F4]


class TestButtonEvents:
    """Test button event handling."""

    def test_button_press_emits_keys(self):
        """Button press emits all keys in order."""
        mock_uinput = MagicMock()

        with patch("g13_ops.mapper.UInput", return_value=mock_uinput):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            mapper.button_map = {"G1": [e.KEY_LEFTCTRL, e.KEY_B]}

            mapper.handle_button_event("G1", True)

            # Should write Ctrl, then B, then sync
            calls = mock_uinput.write.call_args_list
            assert len(calls) == 2
            assert calls[0][0] == (e.EV_KEY, e.KEY_LEFTCTRL, 1)
            assert calls[1][0] == (e.EV_KEY, e.KEY_B, 1)
            mock_uinput.syn.assert_called_once()

    def test_button_release_emits_keys_reversed(self):
        """Button release emits keys in reverse order."""
        mock_uinput = MagicMock()

        with patch("g13_ops.mapper.UInput", return_value=mock_uinput):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            mapper.button_map = {"G1": [e.KEY_LEFTCTRL, e.KEY_B]}

            mapper.handle_button_event("G1", False)

            # Should release B first, then Ctrl
            calls = mock_uinput.write.call_args_list
            assert len(calls) == 2
            assert calls[0][0] == (e.EV_KEY, e.KEY_B, 0)
            assert calls[1][0] == (e.EV_KEY, e.KEY_LEFTCTRL, 0)

    def test_unmapped_button_does_nothing(self):
        """Unmapped button press does nothing."""
        mock_uinput = MagicMock()

        with patch("g13_ops.mapper.UInput", return_value=mock_uinput):
            from g13_ops.mapper import G13Mapper

            mapper = G13Mapper()
            mapper.button_map = {}

            mapper.handle_button_event("G99", True)

            mock_uinput.write.assert_not_called()
            mock_uinput.syn.assert_not_called()
