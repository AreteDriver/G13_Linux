#!/usr/bin/env python3
"""
G13 Button Monitor - Simple real-time display of button states.

Press buttons and watch which byte/bit lights up.
Much simpler than the verification tool - no state machine, just live data.
"""

import sys
import select
import time

# Known button mappings (from hardware testing + ecraven/g13 reference)
KNOWN_BUTTONS = {
    # Byte 3: G1-G8 (confirmed)
    (3, 0): 'G1', (3, 1): 'G2', (3, 2): 'G3', (3, 3): 'G4', (3, 4): 'G5',
    (3, 5): 'G6', (3, 6): 'G7', (3, 7): 'G8',
    # Byte 4: G9-G16 (confirmed)
    (4, 0): 'G9', (4, 1): 'G10', (4, 2): 'G11', (4, 3): 'G12',
    (4, 4): 'G13', (4, 5): 'G14', (4, 6): 'G15', (4, 7): 'G16',
    # Byte 5: G17-G22 (confirmed)
    (5, 0): 'G17', (5, 1): 'G18', (5, 2): 'G19',
    (5, 3): 'G20', (5, 4): 'G21', (5, 5): 'G22',
    # Byte 6: Mode/function buttons (from reference)
    (6, 0): 'BD', (6, 1): 'L1', (6, 2): 'L2', (6, 3): 'L3', (6, 4): 'L4',
    (6, 5): 'M1', (6, 6): 'M2', (6, 7): 'M3',
    # Byte 7: MR and joystick
    (7, 0): 'MR', (7, 1): 'LEFT', (7, 2): 'DOWN', (7, 3): 'TOP',
}

# Bits to ignore (always set, not buttons)
IGNORE_BITS = {(5, 7)}  # Byte 5 bit 7 is always 0x80

def format_byte_bits(val, baseline_val, byte_idx):
    """Format a byte showing which bits are set, highlighting changes."""
    bits = []
    for bit in range(8):
        is_set = (val >> bit) & 1
        was_set = (baseline_val >> bit) & 1

        if is_set and not was_set:
            # Newly pressed - highlight
            name = KNOWN_BUTTONS.get((byte_idx, bit), f'b{bit}')
            bits.append(f'\033[92m{name}\033[0m')  # Green
        elif is_set:
            bits.append(f'b{bit}')
        else:
            bits.append('·')

    return ' '.join(bits)

def main():
    device_path = '/dev/hidraw3'

    print("=" * 70)
    print("G13 BUTTON MONITOR")
    print("=" * 70)
    print(f"\nDevice: {device_path}")
    print("\nPress buttons to see which byte/bit they activate.")
    print("Green = newly pressed button")
    print("Press Ctrl+C to exit.\n")
    print("-" * 70)

    try:
        with open(device_path, 'rb') as f:
            baseline = None
            last_buttons = None  # Will store all 8 bytes

            while True:
                ready = select.select([f], [], [], 0.05)
                if ready[0]:
                    data = f.read(64)
                    if not data:
                        continue

                    # Capture baseline on first read
                    if baseline is None:
                        baseline = list(data[:8])
                        # Zero out button bytes in baseline
                        baseline[3] = 0
                        baseline[4] = 0
                        baseline[6] = 0
                        baseline[7] = baseline[7] & 0x80
                        print("Baseline captured. Start pressing buttons!\n")
                        continue

                    # Extract button bytes
                    buttons = [data[3], data[4], data[6], data[7] & 0x03]

                    # Only track button bytes for change detection (ignore joystick noise)
                    # Bytes 1,2 = joystick X,Y - ignore for button detection
                    button_state = (data[3], data[4], data[5] & 0x7F, data[6], data[7] & 0x03)

                    # Only update display if button state changed
                    if button_state != last_buttons:
                        last_buttons = button_state

                        # Find which button(s) are pressed
                        pressed = []
                        for byte_idx, byte_val in [(3, data[3]), (4, data[4]), (5, data[5]), (6, data[6])]:
                            for bit in range(8):
                                if (byte_idx, bit) in IGNORE_BITS:
                                    continue  # Skip status flags
                                if byte_val & (1 << bit):
                                    name = KNOWN_BUTTONS.get((byte_idx, bit), f'?B{byte_idx}b{bit}')
                                    pressed.append(name)
                        # Byte 7 - separate M3/MR from joystick
                        if data[7] & 0x01:
                            pressed.append(KNOWN_BUTTONS.get((7, 0), 'M3'))
                        if data[7] & 0x02:
                            pressed.append(KNOWN_BUTTONS.get((7, 1), 'MR'))

                        # Show all 8 bytes for debugging
                        all_bytes = ' '.join(f'{data[i]:02x}' for i in range(8))

                        if pressed:
                            print(f"PRESSED: {', '.join(pressed):20s} | Bytes: {all_bytes}")
                        else:
                            print(f"(released)                     | Bytes: {all_bytes}")

    except KeyboardInterrupt:
        print("\n\nMonitor stopped.")
    except PermissionError:
        print(f"Permission denied. Try: sudo python3 {sys.argv[0]}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Device not found: {device_path}")
        sys.exit(1)

if __name__ == '__main__':
    main()
