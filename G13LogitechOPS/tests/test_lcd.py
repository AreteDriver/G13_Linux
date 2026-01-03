"""Tests for G13 LCD display."""

import pytest
from g13_ops.hardware.lcd import G13LCD, FONT_5X7


class TestLCDConstants:
    """Test LCD configuration constants."""

    def test_lcd_dimensions(self):
        """LCD dimensions match G13 spec."""
        lcd = G13LCD()
        assert lcd.WIDTH == 160
        assert lcd.HEIGHT == 43

    def test_framebuffer_size(self):
        """Framebuffer size is correct for 160x43 @ 1bpp."""
        lcd = G13LCD()
        # 160 pixels / 8 bits = 20 bytes per row
        # 20 bytes * 43 rows = 860 bytes (but G13 uses 960)
        assert lcd.FRAMEBUFFER_SIZE == 960
        assert lcd.BYTES_PER_ROW == 20


class TestFontTable:
    """Test 5x7 font table."""

    def test_font_has_printable_ascii(self):
        """Font includes all printable ASCII (32-126)."""
        for code in range(32, 127):
            assert code in FONT_5X7, f"Missing char {code} ({chr(code)})"

    def test_font_entries_are_5_bytes(self):
        """Each font entry is 5 bytes (5 columns)."""
        for code, glyph in FONT_5X7.items():
            assert len(glyph) == 5, f"Char {code} has {len(glyph)} columns"

    def test_space_is_blank(self):
        """Space character (32) is all zeros."""
        assert FONT_5X7[32] == [0x00, 0x00, 0x00, 0x00, 0x00]


class TestPixelOperations:
    """Test pixel manipulation."""

    def test_set_pixel_on(self):
        """Setting a pixel turns it on."""
        lcd = G13LCD()
        lcd.set_pixel(0, 0, True)

        # Pixel (0,0) is bit 7 of byte 0
        assert lcd._framebuffer[0] & 0x80

    def test_set_pixel_off(self):
        """Clearing a pixel turns it off."""
        lcd = G13LCD()
        lcd._framebuffer[0] = 0xFF
        lcd.set_pixel(0, 0, False)

        assert not (lcd._framebuffer[0] & 0x80)

    def test_set_pixel_various_positions(self):
        """Pixels at various positions are set correctly."""
        lcd = G13LCD()

        # Test pixel at x=8 (byte 1, bit 7)
        lcd.set_pixel(8, 0, True)
        assert lcd._framebuffer[1] & 0x80

        # Test pixel at x=7 (byte 0, bit 0)
        lcd.set_pixel(7, 0, True)
        assert lcd._framebuffer[0] & 0x01

        # Test pixel on second row
        lcd.set_pixel(0, 1, True)
        assert lcd._framebuffer[20] & 0x80  # Row 1 starts at byte 20

    def test_set_pixel_out_of_bounds_ignored(self):
        """Out-of-bounds pixels are ignored."""
        lcd = G13LCD()
        lcd.set_pixel(999, 999, True)  # Should not raise
        lcd.set_pixel(-1, -1, True)  # Should not raise


class TestClearFill:
    """Test clear and fill operations."""

    def test_clear_zeroes_framebuffer(self):
        """Clear sets all pixels off."""
        lcd = G13LCD()
        lcd._framebuffer = bytearray([0xFF] * lcd.FRAMEBUFFER_SIZE)
        lcd.clear()

        assert all(b == 0 for b in lcd._framebuffer)

    def test_fill_sets_all_pixels(self):
        """Fill sets all pixels on."""
        lcd = G13LCD()
        lcd.fill()

        assert all(b == 0xFF for b in lcd._framebuffer)


class TestTextRendering:
    """Test text rendering to framebuffer."""

    def test_write_text_modifies_framebuffer(self):
        """Writing text modifies the framebuffer."""
        lcd = G13LCD()
        initial = bytes(lcd._framebuffer)

        lcd.write_text("A", 0, 0, send=False)

        assert lcd._framebuffer != initial

    def test_write_text_at_position(self):
        """Text can be written at specific position."""
        lcd = G13LCD()
        lcd.write_text("X", 10, 5, send=False)

        # Verify some pixels were set in the target area
        # Char 'X' should set pixels around x=10, y=5
        found_pixel = False
        for col in range(10, 15):  # 5-pixel wide char
            byte_idx = (5 * lcd.BYTES_PER_ROW) + (col // 8)
            if lcd._framebuffer[byte_idx]:
                found_pixel = True
                break
        assert found_pixel

    def test_write_text_unknown_char_shows_question(self):
        """Unknown characters render as '?'."""
        lcd = G13LCD()

        # Write unknown char (outside ASCII range)
        lcd.write_text("\x01", 0, 0, send=False)
        unknown_fb = bytes(lcd._framebuffer)

        lcd.clear()

        # Write '?' explicitly
        lcd.write_text("?", 0, 0, send=False)
        question_fb = bytes(lcd._framebuffer)

        assert unknown_fb == question_fb

    def test_write_text_centered(self):
        """Centered text is positioned correctly."""
        lcd = G13LCD()

        # "TEST" is 4 chars * 6 pixels = 24 pixels wide
        # Center of 160: (160 - 24) / 2 = 68
        lcd.write_text_centered("TEST", 0, send=False)

        # Check that pixels start around x=68
        # The first few bytes (0-7) should be empty
        assert all(b == 0 for b in lcd._framebuffer[:8])


class TestBitmapOperations:
    """Test raw bitmap operations."""

    def test_write_bitmap_copies_data(self):
        """Write bitmap copies data to framebuffer."""
        lcd = G13LCD()
        bitmap = bytes([0xAA] * 100)

        lcd.write_bitmap(bitmap)

        assert lcd._framebuffer[:100] == bytearray([0xAA] * 100)

    def test_write_bitmap_rejects_oversized(self):
        """Oversized bitmap raises error."""
        lcd = G13LCD()
        bitmap = bytes([0xFF] * 1000)

        with pytest.raises(ValueError):
            lcd.write_bitmap(bitmap)
