#!/usr/bin/env python3
"""
G13 Button Test - Requires sudo

This script uses libusb to read button/joystick input from the G13.
The kernel's hid-generic driver must be detached, which requires root.

Usage:
    sudo .venv/bin/python test_buttons_sudo.py
    sudo .venv/bin/python test_buttons_sudo.py --emit   # Also emit keys
"""

import sys
import time

sys.path.insert(0, "src")

from g13_linux.device import open_g13_libusb
from g13_linux.gui.models.event_decoder import EventDecoder

# Check for --emit flag
EMIT_KEYS = "--emit" in sys.argv

print("=" * 60)
print("G13 Button Test (using libusb - requires sudo)")
print("=" * 60)
print()

mapper = None
if EMIT_KEYS:
    from g13_linux.mapper import G13Mapper

    mapper = G13Mapper()
    # Load a basic test profile
    mapper.load_profile(
        {
            "mappings": {
                "G1": "KEY_1",
                "G2": "KEY_2",
                "G3": "KEY_3",
                "G4": "KEY_4",
                "G5": "KEY_5",
                "G6": "KEY_6",
                "G7": "KEY_7",
                "G8": "KEY_8",
                "G9": "KEY_9",
                "G10": "KEY_0",
            }
        }
    )
    print("KEY EMISSION ENABLED - G1-G10 will type 1-0")
    print()

try:
    print("Opening G13 via libusb...")
    device = open_g13_libusb()
    print("Device opened successfully!")
    print()
    print("Press G13 buttons now! (30 second test)")
    print("-" * 60)
    print()

    decoder = EventDecoder()
    start_time = time.time()

    while time.time() - start_time < 30:
        data = device.read(timeout_ms=100)
        if data and len(data) >= 8:
            # Decode the report
            state = decoder.decode_report(bytes(data))
            pressed, released = decoder.get_button_changes(state)

            # Show press/release events
            for btn in pressed:
                print(f"  PRESSED:  {btn}")
                if mapper:
                    mapper.handle_button_event(btn, is_pressed=True)
            for btn in released:
                print(f"  RELEASED: {btn}")
                if mapper:
                    mapper.handle_button_event(btn, is_pressed=False)

            # Show joystick if moved
            if abs(state.joystick_x - 128) > 20 or abs(state.joystick_y - 128) > 20:
                print(f"  JOYSTICK: X={state.joystick_x:3d} Y={state.joystick_y:3d}")

    print()
    print("-" * 60)
    print("Test complete!")

except RuntimeError as e:
    print(f"Error: {e}")
    if "Access denied" in str(e) or "permission" in str(e).lower():
        print("\nTry running with sudo:")
        print("  sudo .venv/bin/python test_buttons_sudo.py")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nInterrupted")
finally:
    try:
        device.close()
        if mapper:
            mapper.close()
        print("Device closed, kernel driver reattached")
    except Exception:
        pass  # Best-effort device cleanup on exit
