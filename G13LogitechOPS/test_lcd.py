#!/usr/bin/env python3
"""
Test script for G13 LCD display.

Usage:
    sudo python3 test_lcd.py

Requires:
    - Logitech G13 connected via USB
    - pyusb installed (pip install pyusb)
    - Root access (sudo) to detach kernel driver
"""

import sys
import time


def main():
    print("=" * 60)
    print("G13 LCD Test")
    print("=" * 60)

    # Import after checking we're running as root
    from g13_ops.device import open_g13_libusb
    from g13_ops.hardware.lcd import G13LCD

    print("\nOpening G13 via libusb...")
    try:
        device = open_g13_libusb()
        print("✓ Device opened successfully")
    except RuntimeError as e:
        print(f"✗ Failed to open device: {e}")
        sys.exit(1)

    # Create LCD controller
    lcd = G13LCD(device)

    try:
        # Test 1: Clear screen
        print("\nTest 1: Clearing LCD...")
        lcd.clear()
        time.sleep(0.5)
        print("✓ Clear command sent")

        # Test 2: Fill screen (all pixels on)
        print("\nTest 2: Filling LCD (all pixels on)...")
        lcd.fill()
        time.sleep(1)
        print("✓ Fill command sent")

        # Test 3: Clear again
        print("\nTest 3: Clearing LCD...")
        lcd.clear()
        time.sleep(0.5)

        # Test 4: Write text
        print("\nTest 4: Writing 'Hello G13!'...")
        lcd.write_text("Hello G13!", x=10, y=5)
        time.sleep(1)
        print("✓ Text written")

        # Test 5: Centered text
        print("\nTest 5: Writing centered text...")
        lcd.clear()
        lcd.write_text_centered("G13 Linux Driver", y=10)
        lcd.write_text_centered("LCD Test OK!", y=25)
        time.sleep(2)
        print("✓ Centered text written")

        # Test 6: Draw some pixels
        print("\nTest 6: Drawing pixel pattern...")
        lcd.clear()

        # Draw a border
        for x in range(160):
            lcd.set_pixel(x, 0, True)  # Top
            lcd.set_pixel(x, 42, True)  # Bottom
        for y in range(43):
            lcd.set_pixel(0, y, True)  # Left
            lcd.set_pixel(159, y, True)  # Right

        # Draw diagonal lines
        for i in range(43):
            lcd.set_pixel(i * 3, i, True)  # Diagonal
            lcd.set_pixel(159 - i * 3, i, True)  # Opposite diagonal

        lcd._send_framebuffer()
        time.sleep(2)
        print("✓ Pixel pattern drawn")

        # Final: Show success message
        print("\nTest 7: Final message...")
        lcd.clear()
        lcd.write_text_centered("LCD WORKS!", y=18)

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("Check your G13 LCD - you should see 'LCD WORKS!'")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback

        traceback.print_exc()
    finally:
        print("\nClosing device...")
        device.close()
        print("Done.")


if __name__ == "__main__":
    main()
