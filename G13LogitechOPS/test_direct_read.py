#!/usr/bin/env python3
"""Test direct reading from /dev/hidraw device"""
import sys
import select

# Find the G13 hidraw device
import subprocess
result = subprocess.run(['ls', '-la', '/dev/hidraw*'], capture_output=True, text=True)
print("HID devices:")
print(result.stdout)

# Try to read from /dev/hidraw3 (the one with rw-rw-rw- permissions)
device_path = '/dev/hidraw3'

print(f"\nAttempting to open {device_path}...")
try:
    with open(device_path, 'rb') as f:
        print("✓ Device opened successfully!")
        print("Waiting for button press (10 seconds)...")
        print("Press any button on G13 now!")
        print("-" * 60)

        # Use select to wait for data with timeout
        import time
        end_time = time.time() + 10

        while time.time() < end_time:
            # Check if data is available
            ready = select.select([f], [], [], 0.1)
            if ready[0]:
                data = f.read(64)
                if data:
                    hex_str = ' '.join(f'{b:02x}' for b in data)
                    print(f"RAW ({len(data)} bytes): {hex_str}")

                    # Show non-zero bytes
                    non_zero = [(i, b) for i, b in enumerate(data) if b != 0]
                    if non_zero:
                        print(f"Non-zero bytes: {non_zero}")
                    print("-" * 60)

        print("\nTest complete!")

except PermissionError:
    print(f"✗ Permission denied - need to add user to correct group")
    print(f"  Try: sudo usermod -a -G plugdev $USER")
    print(f"  Then log out and back in")
except FileNotFoundError:
    print(f"✗ Device not found: {device_path}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
