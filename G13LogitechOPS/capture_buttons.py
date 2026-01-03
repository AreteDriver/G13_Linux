#!/usr/bin/env python3
"""Interactive button capture script"""
import sys
import select
import time

device_path = '/dev/hidraw3'

print("=" * 70)
print("G13 BUTTON MAPPING CAPTURE TOOL")
print("=" * 70)
print(f"\nOpening device: {device_path}")

try:
    with open(device_path, 'rb') as f:
        print("✓ Device opened successfully!")
        print("\n" + "=" * 70)
        print("READY TO CAPTURE!")
        print("=" * 70)
        print("\nInstructions:")
        print("  1. Press ONE button at a time")
        print("  2. Hold for 1 second")
        print("  3. Release completely before next button")
        print("  4. Press Ctrl+C when done")
        print("\n" + "=" * 70)
        print("Listening for button presses...\n")

        button_count = 0
        last_data = None

        while True:
            # Check if data is available (non-blocking)
            ready = select.select([f], [], [], 0.1)
            if ready[0]:
                data = f.read(64)
                if data and data != last_data:  # Only show if different from last
                    button_count += 1

                    print(f"\n[Event #{button_count}] {time.strftime('%H:%M:%S')}")
                    print("-" * 70)

                    # Hex dump
                    hex_str = ' '.join(f'{b:02x}' for b in data)
                    print(f"RAW: {hex_str}")

                    # Non-zero bytes
                    non_zero = [(i, b) for i, b in enumerate(data) if b != 0]
                    if non_zero:
                        print(f"Non-zero bytes:")
                        for idx, val in non_zero:
                            binary = bin(val)[2:].zfill(8)
                            print(f"  Byte[{idx:2d}] = 0x{val:02x} ({val:3d}) = {binary}")
                    else:
                        print("  (All zeros - button released)")

                    last_data = data

except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print(f"Capture stopped. Total events: {button_count}")
    print("=" * 70)

except PermissionError:
    print(f"✗ Permission denied")
    print(f"Fix: sudo chmod 666 {device_path}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
