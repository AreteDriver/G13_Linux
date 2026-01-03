#!/usr/bin/env python3
"""
G13 Button Verification Tool

Interactive tool to verify and correct button mappings.
Tests each button and compares actual data with predictions.
"""

import sys
import select
import time

# Current predictions from event_decoder.py
BUTTON_MAP = {
    # Confirmed
    'G1': (3, 0), 'G2': (3, 1), 'G3': (3, 2), 'G4': (3, 3), 'G5': (3, 4),
    'MR': (7, 1),
    # Predicted - Row 1 remainder
    'G6': (3, 5), 'G7': (3, 6), 'G8': (3, 7),
    # Predicted - Row 2 (Byte 4)
    'G9': (4, 0), 'G10': (4, 1), 'G11': (4, 2), 'G12': (4, 3),
    'G13': (4, 4), 'G14': (4, 5), 'G15': (4, 6), 'G16': (4, 7),
    # Predicted - Row 3-4 (Byte 6)
    'G17': (6, 0), 'G18': (6, 1), 'G19': (6, 2),
    'G20': (6, 3), 'G21': (6, 4), 'G22': (6, 5),
    # Predicted - M keys
    'M1': (6, 6), 'M2': (6, 7), 'M3': (7, 0),
    # Predicted - Joystick click
    'JOYSTICK': (7, 2),
}

# Baseline captured dynamically at startup
BASELINE = None  # Will be set from first read

# Test order - confirmed first, then predicted
TEST_ORDER = [
    # Confirmed
    'G1', 'G2', 'G3', 'G4', 'G5', 'MR',
    # Row 1 predictions
    'G6', 'G7',
    # Row 2
    'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14',
    # Row 3
    'G15', 'G16', 'G17', 'G18', 'G19',
    # Row 4
    'G20', 'G21', 'G22',
    # Mode keys
    'M1', 'M2', 'M3',
    # Joystick
    'JOYSTICK',
]

def find_changed_bits(baseline: list, data: bytes) -> list:
    """Find which byte/bit positions changed from baseline."""
    changes = []
    for byte_idx in range(min(len(baseline), len(data))):
        if data[byte_idx] != baseline[byte_idx]:
            # Find which bits changed
            diff = data[byte_idx] ^ baseline[byte_idx]
            for bit in range(8):
                if diff & (1 << bit):
                    changes.append((byte_idx, bit, data[byte_idx] & (1 << bit) != 0))
    return changes

def format_prediction(button: str) -> str:
    """Format the predicted mapping."""
    byte_idx, bit_pos = BUTTON_MAP[button]
    hex_val = 1 << bit_pos
    return f"Byte[{byte_idx}] bit {bit_pos} (0x{hex_val:02x})"

def main():
    device_path = '/dev/hidraw3'

    print("=" * 70)
    print("G13 BUTTON VERIFICATION TOOL")
    print("=" * 70)
    print(f"\nDevice: {device_path}")
    print("\nThis tool will guide you through testing each button.")
    print("It compares actual data with predictions and reports mismatches.\n")

    results = {}  # button -> (predicted, actual, match)

    try:
        with open(device_path, 'rb') as f:
            print("✓ Device opened successfully!")

            # Set baseline - button bytes are 0 when idle, joystick varies
            global BASELINE
            print("  Waiting for first input to sync...", end=" ", flush=True)

            # Read first packet to sync
            ready = select.select([f], [], [], 10.0)
            if ready[0]:
                data = f.read(64)
                # Use this data but zero out button bytes for baseline
                BASELINE = list(data[:8])
                BASELINE[3] = 0  # G1-G8 buttons
                BASELINE[4] = 0  # G9-G16 buttons
                BASELINE[6] = 0  # G17-G22, M1-M2
                BASELINE[7] = BASELINE[7] & 0x80  # Keep joystick Y high bit, clear M3/MR/etc
                print(f"OK\n")

            current_idx = 0
            waiting_for_press = True
            last_data = None

            while current_idx < len(TEST_ORDER):
                button = TEST_ORDER[current_idx]
                byte_idx, bit_pos = BUTTON_MAP[button]

                if waiting_for_press:
                    print("=" * 70)
                    print(f"TEST {current_idx + 1}/{len(TEST_ORDER)}: Press {button}")
                    print("-" * 70)
                    print(f"  Expected: {format_prediction(button)}")
                    print(f"  Press and HOLD the button, then release...")
                    print()

                # Read with timeout
                ready = select.select([f], [], [], 0.1)
                if ready[0]:
                    data = f.read(64)
                    if data and data[:8] != last_data:
                        last_data = data[:8]

                        # Find changes from baseline
                        changes = find_changed_bits(BASELINE, data)

                        # Filter to only button-related changes
                        button_changes = []
                        for chg_byte, chg_bit, is_set in changes:
                            if chg_byte == 3:  # G1-G8
                                button_changes.append((chg_byte, chg_bit, is_set))
                            elif chg_byte == 4:  # G9-G16
                                button_changes.append((chg_byte, chg_bit, is_set))
                            elif chg_byte == 6:  # G17-G22, M1-M2
                                button_changes.append((chg_byte, chg_bit, is_set))
                            elif chg_byte == 7 and chg_bit < 2:  # M3, MR only (not joystick)
                                button_changes.append((chg_byte, chg_bit, is_set))

                        if waiting_for_press and button_changes:
                            # Button pressed - analyze
                            waiting_for_press = False

                            # Format raw data
                            hex_str = ' '.join(f'{b:02x}' for b in data[:8])
                            print(f"  RAW: {hex_str}")

                            # Check if prediction matches
                            predicted = (byte_idx, bit_pos)
                            actual = None

                            for chg_byte, chg_bit, is_set in button_changes:
                                if is_set:
                                    actual = (chg_byte, chg_bit)
                                    break

                            if actual == predicted:
                                print(f"  ✅ MATCH! Byte[{actual[0]}] bit {actual[1]}")
                                results[button] = (predicted, actual, True)
                            elif actual:
                                print(f"  ❌ MISMATCH!")
                                print(f"     Predicted: Byte[{predicted[0]}] bit {predicted[1]}")
                                print(f"     Actual:    Byte[{actual[0]}] bit {actual[1]}")
                                results[button] = (predicted, actual, False)
                            else:
                                print(f"  ⚠️  No button change detected")
                                results[button] = (predicted, None, False)

                            print()

                        elif not waiting_for_press:
                            # Check if all button bytes are zero (released)
                            buttons_idle = (
                                data[3] == 0 and
                                data[4] == 0 and
                                data[6] == 0 and
                                (data[7] & 0x03) == 0  # M3 and MR bits
                            )
                            # Debug: show what we're seeing
                            hex_str = ' '.join(f'{b:02x}' for b in data[:8])
                            print(f"\r  Waiting release... [{hex_str}] idle={buttons_idle}", end="", flush=True)
                            if buttons_idle:
                                # Button released - move to next
                                waiting_for_press = True
                                current_idx += 1
                                print("\n  (Released)\n")

            # Summary
            print("\n" + "=" * 70)
            print("VERIFICATION SUMMARY")
            print("=" * 70)

            confirmed = []
            mismatched = []
            untested = []

            for button in TEST_ORDER:
                if button in results:
                    pred, actual, match = results[button]
                    if match:
                        confirmed.append(button)
                    else:
                        mismatched.append((button, pred, actual))
                else:
                    untested.append(button)

            print(f"\n✅ Confirmed ({len(confirmed)}): {', '.join(confirmed)}")

            if mismatched:
                print(f"\n❌ Mismatched ({len(mismatched)}):")
                for button, pred, actual in mismatched:
                    if actual:
                        print(f"   {button}: Byte[{pred[0]}]b{pred[1]} -> Byte[{actual[0]}]b{actual[1]}")
                    else:
                        print(f"   {button}: Not detected")

            if untested:
                print(f"\n⚠️  Untested: {', '.join(untested)}")

            # Generate corrected BUTTON_MAP if needed
            if mismatched:
                print("\n" + "-" * 70)
                print("CORRECTED BUTTON_MAP (copy to event_decoder.py):")
                print("-" * 70)
                print("BUTTON_MAP = {")
                for button in TEST_ORDER:
                    if button in results:
                        pred, actual, match = results[button]
                        if match:
                            byte_idx, bit_pos = pred
                        elif actual:
                            byte_idx, bit_pos = actual
                        else:
                            byte_idx, bit_pos = pred
                            print(f"    # ⚠️  {button} not detected, keeping prediction")

                        status = "✅" if match else "❌ CORRECTED"
                        print(f"    '{button}': ({byte_idx}, {bit_pos}),  # {status}")
                print("}")

    except KeyboardInterrupt:
        print("\n\nVerification cancelled.")

    except PermissionError:
        print(f"✗ Permission denied. Run: sudo chmod 666 {device_path}")
        sys.exit(1)

    except FileNotFoundError:
        print(f"✗ Device not found: {device_path}")
        print("Is the G13 connected?")
        sys.exit(1)

if __name__ == '__main__':
    main()
