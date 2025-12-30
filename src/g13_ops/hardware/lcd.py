"""
G13 LCD Control

Controls the G13's 160x43 monochrome LCD display.

Protocol (from g13-rs/libg13):
- LCD is 160x43 pixels, monochrome (1 bit per pixel)
- Framebuffer size: 960 bytes
- Send format: 32-byte header (first byte = 0x03) + 960-byte framebuffer
- Total packet: 992 bytes via interrupt transfer to endpoint 2
"""


class G13LCD:
    """LCD display controller for G13 (160x43 monochrome)"""

    WIDTH = 160
    HEIGHT = 43
    BYTES_PER_ROW = WIDTH // 8  # 20 bytes per row
    FRAMEBUFFER_SIZE = 960
    HEADER_SIZE = 32
    COMMAND_BYTE = 0x03

    def __init__(self, device_handle=None):
        """
        Initialize LCD controller.

        Args:
            device_handle: HidrawDevice instance from device.py
        """
        self.device = device_handle
        self._framebuffer = bytearray(self.FRAMEBUFFER_SIZE)

    def clear(self):
        """Clear LCD display (all pixels off)."""
        self._framebuffer = bytearray(self.FRAMEBUFFER_SIZE)
        self._send_framebuffer()

    def fill(self):
        """Fill LCD display (all pixels on)."""
        self._framebuffer = bytearray([0xFF] * self.FRAMEBUFFER_SIZE)
        self._send_framebuffer()

    def write_text(self, text: str, x: int = 0, y: int = 0):
        """
        Write text to LCD using a simple 5x7 font.

        Args:
            text: Text to display
            x: X position (0-159)
            y: Y position (0-42)
        """
        # Simple 5x7 font would require a font table
        # For now, just update the framebuffer with a pattern
        print(f"[LCD] Text rendering not yet implemented: '{text}'")

    def write_bitmap(self, bitmap: bytes):
        """
        Write raw bitmap to LCD.

        Args:
            bitmap: Raw bitmap data (960 bytes for full frame)
        """
        if len(bitmap) > self.FRAMEBUFFER_SIZE:
            raise ValueError(f"Bitmap too large: max {self.FRAMEBUFFER_SIZE} bytes")

        # Copy bitmap to framebuffer
        self._framebuffer[:len(bitmap)] = bitmap
        self._send_framebuffer()

    def set_pixel(self, x: int, y: int, on: bool = True):
        """
        Set a single pixel.

        Args:
            x: X coordinate (0-159)
            y: Y coordinate (0-42)
            on: True for pixel on, False for off
        """
        if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
            return

        byte_idx = (y * self.BYTES_PER_ROW) + (x // 8)
        bit_idx = 7 - (x % 8)  # MSB first

        if on:
            self._framebuffer[byte_idx] |= (1 << bit_idx)
        else:
            self._framebuffer[byte_idx] &= ~(1 << bit_idx)

    def _send_framebuffer(self):
        """Send the framebuffer to the device."""
        if not self.device:
            print("[LCD] No device connected")
            return

        try:
            # Build packet: 32-byte header + 960-byte framebuffer
            # First byte of header is command 0x03
            header = bytearray(self.HEADER_SIZE)
            header[0] = self.COMMAND_BYTE

            # Full packet is 992 bytes
            packet = bytes(header) + bytes(self._framebuffer)

            # Send as single write
            self.device.write(packet)
        except OSError as e:
            print(f"[LCD] Failed to send framebuffer: {e}")

    def set_brightness(self, level: int):
        """
        Set LCD brightness.

        Args:
            level: Brightness level (0-100)

        Note: LCD brightness may not be separately controllable on G13.
        """
        if not 0 <= level <= 100:
            raise ValueError("Brightness must be 0-100")

        print("[LCD] Brightness control not supported on G13 LCD")
