"""
G13LogitechOPS - Python userspace driver for Logitech G13 Gaming Keyboard

A modern, easy-to-use driver for the Logitech G13 on Linux systems.
"""

__version__ = "0.2.0"
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
