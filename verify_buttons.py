#!/usr/bin/env python3
"""
G13 Button Verification Tool

Interactive tool to verify and correct button mappings.
Tests each button and compares actual data with predictions.
"""

import select
import sys

# Current predictions from event_decoder.py
BUTTON_MAP = {
    # Confirmed
    "G1": (3, 0),
    "G2": (3, 1),
    "G3": (3, 2),
    "G4": (3, 3),
    "G5": (3, 4),
    "MR": (7, 1),
    # Predicted - Row 1 remainder
    "G6": (3, 5),
    "G7": (3, 6),
    "G8": (3, 7),
    # Predicted - Row 2 (Byte 4)
    "G9": (4, 0),
    "G10": (4, 1),
    "G11": (4, 2),
    "G12": (4, 3),
    "G13": (4, 4),
    "G14": (4, 5),
    "G15": (4, 6),
    "G16": (4, 7),
    # Predicted - Row 3-4 (Byte 6)
    "G17": (6, 0),
    "G18": (6, 1),
    "G19": (6, 2),
    "G20": (6, 3),
    "G21": (6, 4),
    "G22": (6, 5),
    # Predicted - M keys
    "M1": (6, 6),
    "M2": (6, 7),
    "M3": (7, 0),
    # Predicted - Joystick click
    "JOYSTICK": (7, 2),
}

# Baseline captured dynamically at startup
BASELINE = None  # Will be set from first read

# Test order - confirmed first, then predicted
TEST_ORDER = [
    # Confirmed
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "MR",
    # Row 1 predictions
    "G6",
    "G7",
    # Row 2
    "G8",
    "G9",
    "G10",
    "G11",
    "G12",
    "G13",
    "G14",
    # Row 3
    "G15",
    "G16",
    "G17",
    "G18",
    "G19",
    # Row 4
    "G20",
    "G21",
    "G22",
    # Mode keys
    "M1",
    "M2",
    "M3",
    # Joystick
    "JOYSTICK",
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


def _setup_baseline(f):
    """Initialize baseline from first read. Returns baseline or None."""
    global BASELINE
    print("  Waiting for first input to sync...", end=" ", flush=True)
    ready = select.select([f], [], [], 10.0)
    if ready[0]:
        data = f.read(64)
        BASELINE = list(data[:8])
        BASELINE[3] = BASELINE[4] = BASELINE[6] = 0
        BASELINE[7] = BASELINE[7] & 0x80
        print("OK\n")
        return BASELINE
    return None


def _filter_button_changes(changes):
    """Filter changes to only button-related bytes."""
    button_changes = []
    for chg_byte, chg_bit, is_set in changes:
        if chg_byte in (3, 4, 6) or (chg_byte == 7 and chg_bit < 2):
            button_changes.append((chg_byte, chg_bit, is_set))
    return button_changes


def _analyze_button_press(button_changes, predicted, data):
    """Analyze button press and return (actual, match, message)."""
    hex_str = " ".join(f"{b:02x}" for b in data[:8])
    print(f"  RAW: {hex_str}")

    actual = next(((chg_byte, chg_bit) for chg_byte, chg_bit, is_set in button_changes if is_set), None)

    if actual == predicted:
        print(f"  ✅ MATCH! Byte[{actual[0]}] bit {actual[1]}")
        return actual, True
    elif actual:
        print("  ❌ MISMATCH!")
        print(f"     Predicted: Byte[{predicted[0]}] bit {predicted[1]}")
        print(f"     Actual:    Byte[{actual[0]}] bit {actual[1]}")
        return actual, False
    else:
        print("  ⚠️  No button change detected")
        return None, False


def _check_buttons_idle(data):
    """Check if all button bytes indicate released state."""
    return data[3] == 0 and data[4] == 0 and data[6] == 0 and (data[7] & 0x03) == 0


def _run_verification_loop(f, results):
    """Main verification loop. Updates results dict."""
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
            print("  Press and HOLD the button, then release...\n")

        ready = select.select([f], [], [], 0.1)
        if not ready[0]:
            continue

        data = f.read(64)
        if not data or data[:8] == last_data:
            continue

        last_data = data[:8]
        changes = find_changed_bits(BASELINE, data)
        button_changes = _filter_button_changes(changes)

        if waiting_for_press and button_changes:
            waiting_for_press = False
            predicted = (byte_idx, bit_pos)
            actual, match = _analyze_button_press(button_changes, predicted, data)
            results[button] = (predicted, actual, match)
            print()
        elif not waiting_for_press:
            hex_str = " ".join(f"{b:02x}" for b in data[:8])
            print(f"\r  Waiting release... [{hex_str}] idle={_check_buttons_idle(data)}", end="", flush=True)
            if _check_buttons_idle(data):
                waiting_for_press = True
                current_idx += 1
                print("\n  (Released)\n")


def _print_summary(results):
    """Print verification summary and corrected BUTTON_MAP if needed."""
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)

    confirmed = [b for b in TEST_ORDER if b in results and results[b][2]]
    mismatched = [(b, results[b][0], results[b][1]) for b in TEST_ORDER if b in results and not results[b][2]]
    untested = [b for b in TEST_ORDER if b not in results]

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

    if mismatched:
        print("\n" + "-" * 70)
        print("CORRECTED BUTTON_MAP (copy to event_decoder.py):")
        print("-" * 70)
        print("BUTTON_MAP = {")
        for button in TEST_ORDER:
            if button in results:
                pred, actual, match = results[button]
                byte_idx, bit_pos = pred if match else (actual if actual else pred)
                if not match and not actual:
                    print(f"    # ⚠️  {button} not detected, keeping prediction")
                status = "✅" if match else "❌ CORRECTED"
                print(f"    '{button}': ({byte_idx}, {bit_pos}),  # {status}")
        print("}")


def main():
    device_path = "/dev/hidraw3"

    print("=" * 70)
    print("G13 BUTTON VERIFICATION TOOL")
    print("=" * 70)
    print(f"\nDevice: {device_path}")
    print("\nThis tool will guide you through testing each button.")
    print("It compares actual data with predictions and reports mismatches.\n")

    results = {}

    try:
        with open(device_path, "rb") as f:
            print("✓ Device opened successfully!")
            if _setup_baseline(f) is None:
                print("Failed to capture baseline")
                return
            _run_verification_loop(f, results)
            _print_summary(results)

    except KeyboardInterrupt:
        print("\n\nVerification cancelled.")
    except PermissionError:
        print(f"✗ Permission denied. Run: sudo chmod 666 {device_path}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"✗ Device not found: {device_path}")
        print("Is the G13 connected?")
        sys.exit(1)


if __name__ == "__main__":
    main()
