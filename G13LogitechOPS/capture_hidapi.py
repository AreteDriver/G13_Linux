#!/usr/bin/env python3
"""
G13 Button Capture Tool

Captures raw HID reports from the G13 device for reverse engineering button mappings.
Uses direct hidraw access which works with standard udev rules.
"""
import os
import glob
import time
import sys
import select

def find_g13_hidraw():
    """Find the hidraw device path for the G13."""
    for hidraw in glob.glob('/sys/class/hidraw/hidraw*'):
        uevent_path = os.path.join(hidraw, 'device', 'uevent')
        try:
            with open(uevent_path, 'r') as f:
                content = f.read()
                if '0000046D' in content.upper() and '0000C21C' in content.upper():
                    device_name = os.path.basename(hidraw)
                    return f'/dev/{device_name}'
        except (IOError, OSError):
            continue
    return None

def main():
    print("=" * 70)
    print("G13 BUTTON CAPTURE - Direct hidraw access")
    print("=" * 70)

    # Find G13
    hidraw_path = find_g13_hidraw()
    if not hidraw_path:
        print("ERROR: No G13 device found!")
        print("Make sure your G13 is connected and udev rules are installed.")
        sys.exit(1)

    print(f"\nFound G13 at: {hidraw_path}")

    try:
        f = open(hidraw_path, 'rb')
        print("Device opened successfully!")

        print("\n" + "=" * 70)
        print("INSTRUCTIONS:")
        print("  1. Press each G-key (G1-G22) one at a time")
        print("  2. Press M1, M2, M3 keys")
        print("  3. Move the joystick")
        print("  4. Press the joystick button (if any)")
        print("  5. Press Ctrl+C when done")
        print("=" * 70)
        print("\nWaiting for button presses...")
        print("-" * 70)

        event_count = 0
        last_data = None

        while True:
            # Use select for timeout
            ready, _, _ = select.select([f], [], [], 0.1)
            if ready:
                data = f.read(64)
                if data and data != last_data:
                    event_count += 1
                    print(f"\n[Event #{event_count}] {time.strftime('%H:%M:%S')}")
                    print(f"RAW ({len(data)} bytes): {' '.join(f'{b:02x}' for b in data)}")

                    # Show non-zero bytes
                    non_zero = [(idx, b) for idx, b in enumerate(data) if b != 0]
                    if non_zero:
                        print("Non-zero bytes:")
                        for idx, val in non_zero:
                            binary = bin(val)[2:].zfill(8)
                            print(f"  Byte[{idx:2d}] = 0x{val:02x} ({val:3d}) = {binary}")

                    # Show what changed from last event
                    if last_data:
                        changes = []
                        for i, (old, new) in enumerate(zip(last_data, data)):
                            if old != new:
                                changes.append(f"Byte[{i}]: {old:02x} -> {new:02x}")
                        if changes:
                            print("Changes from previous:")
                            for c in changes:
                                print(f"  {c}")

                    last_data = data

    except KeyboardInterrupt:
        print(f"\n\n{'='*70}")
        print(f"Capture complete. Total events: {event_count}")
        print("=" * 70)
    except PermissionError:
        print(f"ERROR: Permission denied for {hidraw_path}")
        print("Run: sudo chmod 666 " + hidraw_path)
        print("Or install the udev rules from udev/99-logitech-g13.rules")
    finally:
        f.close()

    print("\nDone!")

if __name__ == "__main__":
    main()
