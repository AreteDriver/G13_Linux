"""
G13 Linux Driver
================

A Python userspace driver for the Logitech G13 Gaming Keyboard on Linux.

Features:
- Full key mapping and macro support
- RGB LED control
- LCD display management (160x43 pixels)
- Profile-based configuration
- PyQt6 GUI application

Basic Usage:
    >>> from g13_linux import open_g13, G13Mapper
    >>> device = open_g13()
    >>> mapper = G13Mapper(device)

For more information, see: https://github.com/AreteDriver/G13_Linux
"""

__version__ = "1.3.0"
__author__ = "AreteDriver"
__license__ = "MIT"

from .device import open_g13, read_event, G13_VENDOR_ID, G13_PRODUCT_ID
from .mapper import G13Mapper

__all__ = [
    "open_g13",
    "read_event",
    "G13Mapper",
    "G13_VENDOR_ID",
    "G13_PRODUCT_ID",
]
