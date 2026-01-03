#!/usr/bin/env python3
"""Capture raw bytes when pressing thumb/joystick buttons."""
import sys
import time
sys.path.insert(0, 'src')

from g13_ops.device import open_g13_libusb

print("=" * 60)
print("RAW BYTE CAPTURE - Press thumb buttons / joystick click")
print("=" * 60)
print()

device = open_g13_libusb()
print("Device opened. Press the buttons near the joystick!")
print("Looking for byte changes...")
print()

baseline = None
start = time.time()

while time.time() - start < 20:
    data = device.read(timeout_ms=100)
    if data and len(data) >= 8:
        if baseline is None:
            baseline = list(data[:8])
            print(f"Baseline: {' '.join(f'{b:02x}' for b in baseline)}")
            print("-" * 60)
            continue
        
        # Check for changes in bytes 5-7 (where thumb buttons likely are)
        changes = []
        for i in range(8):
            if data[i] != baseline[i]:
                changes.append(f"Byte {i}: {baseline[i]:02x} -> {data[i]:02x}")
        
        if changes:
            print(f"CHANGE: {' | '.join(changes)}")
            print(f"   Raw: {' '.join(f'{data[i]:02x}' for i in range(8))}")

device.close()
print("\nDone!")
