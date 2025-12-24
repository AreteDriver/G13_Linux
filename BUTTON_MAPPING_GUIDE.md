# G13 Button Mapping Reverse Engineering Guide

This guide walks you through the process of reverse engineering the USB HID report format to enable button mapping in the G13LogitechOPS GUI.

## Overview

The G13 sends 64-byte USB HID reports when buttons are pressed. We need to identify which bytes/bits correspond to which buttons by systematically pressing each button and recording the output.

## Prerequisites

- ✅ Logitech G13 keyboard connected via USB
- ✅ G13LogitechOPS installed (`pip install -e .`)
- ✅ Terminal access
- ✅ Text editor or spreadsheet for recording data

## Step 1: Verify Device Connection

```bash
# Check if G13 is detected
lsusb | grep "046d:c21c"
# Should output: Bus XXX Device XXX: ID 046d:c21c Logitech, Inc. G13 Advanced Gameboard
```

If not found:
```bash
# Check udev rules
ls -la /etc/udev/rules.d/ | grep g13

# If missing, create udev rule:
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c21c", MODE="0666"' | sudo tee /etc/udev/rules.d/99-logitech-g13.rules

# Reload udev
sudo udevadm control --reload-rules
sudo udevadm trigger

# Unplug and replug G13
```

## Step 2: Run the CLI Tool

```bash
cd ~/projects/G13LogitechOPS
source .venv/bin/activate
g13-ops
```

Expected output:
```
Opening Logitech G13…
G13 opened. Press keys; Ctrl+C to exit.
```

## Step 3: Systematic Button Testing

### Testing Procedure

1. **Press ONE button at a time**
2. **Hold for 1 second** (to ensure report is captured)
3. **Release completely** before next button
4. **Record the RAW output** in a table (see below)

### Data Recording Template

Create a file `button_mapping_data.txt` and record each button:

```
Button: G1
RAW: [00, 00, 00, 01, 00, 00, 00, 00, 00, 00, 00, 00, ...]
Notes: First non-zero byte at index 3, value 0x01

Button: G2
RAW: [00, 00, 00, 02, 00, 00, 00, 00, 00, 00, 00, 00, ...]
Notes: First non-zero byte at index 3, value 0x02

... (continue for all buttons)
```

### Button Test Sequence

Test in this order for systematic coverage:

**G-keys (22 buttons):**
- Row 1: G1, G2, G3, G4, G5
- Row 2: G6, G7, G8, G9, G10
- Row 3: G11, G12, G13, G14
- Row 4: G15, G16, G17, G18
- Row 5: G19, G20, G21, G22

**M-keys (3 buttons):**
- M1, M2, M3

**Additional:**
- MR (macro record)

### What to Look For

1. **Byte Position**: Which byte changes when button is pressed?
2. **Bit Pattern**: If multiple buttons share a byte, which bits change?
3. **Value Pattern**: Does value increment (0x01, 0x02, 0x04, 0x08) indicating bit positions?

## Step 4: Analyze the Data

### Common Patterns

**Pattern 1: Sequential Bits in Same Byte**
```
G1:  [00, 00, 00, 01, ...]  # Bit 0 (0x01 = 0000 0001)
G2:  [00, 00, 00, 02, ...]  # Bit 1 (0x02 = 0000 0010)
G3:  [00, 00, 00, 04, ...]  # Bit 2 (0x04 = 0000 0100)
G4:  [00, 00, 00, 08, ...]  # Bit 3 (0x08 = 0000 1000)
```
→ All G1-G4 use byte 3, bits 0-3

**Pattern 2: Multiple Bytes**
```
G1-G8:   Byte 3
G9-G16:  Byte 4
G17-G22: Byte 5
```

**Pattern 3: Bitmask Combination**
```
G1 + G2 pressed: [00, 00, 00, 03, ...]  # 0x01 | 0x02 = 0x03
```

### Analysis Tool (Python)

Use this script to analyze patterns:

```python
# analyze_reports.py
data = {
    'G1': [0x00, 0x00, 0x00, 0x01, 0x00, ...],
    'G2': [0x00, 0x00, 0x00, 0x02, 0x00, ...],
    # ... add all your recorded data
}

# Find non-zero bytes
for button, report in data.items():
    non_zero = [(i, val) for i, val in enumerate(report) if val != 0]
    print(f"{button}: {non_zero}")

# Check for bit patterns
def analyze_byte(byte_idx):
    print(f"\nByte {byte_idx} analysis:")
    for button, report in data.items():
        val = report[byte_idx]
        if val != 0:
            bits = bin(val)[2:].zfill(8)
            print(f"  {button}: 0x{val:02x} = {bits}")
```

## Step 5: Update EventDecoder

Once you've identified the pattern, update the code:

**File**: `src/g13_ops/gui/models/event_decoder.py`

```python
# Around line 35-50, update BUTTON_MAP:

BUTTON_MAP = {
    # Example based on your findings:
    # Format: 'button_id': (byte_index, bit_position)

    # G-keys in byte 3
    'G1': (3, 0),   # Byte 3, bit 0
    'G2': (3, 1),   # Byte 3, bit 1
    'G3': (3, 2),   # Byte 3, bit 2
    'G4': (3, 3),   # Byte 3, bit 3
    'G5': (3, 4),   # Byte 3, bit 4
    'G6': (3, 5),   # Byte 3, bit 5
    'G7': (3, 6),   # Byte 3, bit 6
    'G8': (3, 7),   # Byte 3, bit 7

    # G-keys in byte 4 (if pattern continues)
    'G9':  (4, 0),
    'G10': (4, 1),
    # ... etc

    # M-keys (adjust based on findings)
    'M1': (2, 0),
    'M2': (2, 1),
    'M3': (2, 2),

    # MR key
    'MR': (2, 3),
}

# Also update joystick bytes if you tested them:
JOYSTICK_X_BYTE = 5  # Example - adjust based on testing
JOYSTICK_Y_BYTE = 6  # Example - adjust based on testing
```

## Step 6: Test in GUI

```bash
# Launch GUI
g13-ops-gui

# Test:
1. Press G1 on physical keyboard
   → Button should highlight GREEN in GUI
   → Event should appear in Monitor tab

2. Configure G1 mapping:
   - Click G1 button in GUI
   - Select KEY_A
   - Press G1 physically
   → Should emit 'A' key to system

3. Save profile and test reload
```

## Step 7: Verify All Buttons

Create a test checklist:

```
[ ] G1  - Byte: ___ Bit: ___ - GUI highlights: ___
[ ] G2  - Byte: ___ Bit: ___ - GUI highlights: ___
[ ] G3  - Byte: ___ Bit: ___ - GUI highlights: ___
...
[ ] M1  - Byte: ___ Bit: ___ - GUI highlights: ___
[ ] M2  - Byte: ___ Bit: ___ - GUI highlights: ___
[ ] M3  - Byte: ___ Bit: ___ - GUI highlights: ___
```

## Example: Real G13 Data (Reference)

Based on the libg13 project, the actual format might be:

```
Byte 0-2:  Header/control
Byte 3:    G1-G8   (bits 0-7)
Byte 4:    G9-G16  (bits 0-7)
Byte 5:    G17-G22 (bits 0-5), M1-M2 (bits 6-7)
Byte 6:    M3, MR, other controls
Byte 7-8:  Joystick X (16-bit)
Byte 9-10: Joystick Y (16-bit)
```

**Note**: This is reference only - YOUR device might differ slightly!

## Troubleshooting

### Problem: No RAW output when pressing buttons

**Solution 1**: Check permissions
```bash
# Check if device is accessible
ls -l /dev/hidraw*
# Should show mode 0666 or your user in group

# Test with sudo
sudo g13-ops
```

**Solution 2**: Verify device is not claimed by another driver
```bash
# Check what's using the device
lsof | grep hidraw
fuser /dev/hidraw*

# If another process is using it, kill it
```

### Problem: Output shows all zeros

**Possible causes**:
- Wrong HID device (G13 has multiple endpoints)
- Device in different mode
- Need to send initialization command first

**Debug**:
```python
# In device.py, add debug output:
def open_g13():
    for dev in hid.enumerate():
        print(f"Device: {dev}")  # See all HID devices
        if dev["vendor_id"] == 0x046d and dev["product_id"] == 0xc21c:
            print(f"Found G13: {dev['path']}")
            # ... rest of code
```

### Problem: Inconsistent data

- Some buttons might send multiple reports
- Wait for stable state before recording
- Press and hold for 1 second to ensure capture

## Advanced: Joystick Testing

If you want to test joystick as well:

1. **Move joystick slowly in each direction**
2. **Record which bytes change**
3. **Identify X-axis bytes** (change when moving left/right)
4. **Identify Y-axis bytes** (change when moving up/down)

Joystick usually uses 2 bytes per axis (16-bit value):
- Center: ~0x80 0x00 (32768)
- Full left/up: ~0x00 0x00
- Full right/down: ~0xFF 0xFF

## Contributing Your Findings

Once you've successfully mapped all buttons:

1. **Update BUTTON_MAPPING_GUIDE.md** with your findings
2. **Submit a pull request** to help others
3. **Share in GitHub Discussions**

Your data helps the community!

## Resources

- **libg13 source**: https://github.com/ecraven/g13
- **USB HID Spec**: https://www.usb.org/hid
- **Linux HID docs**: https://www.kernel.org/doc/html/latest/hid/
- **G13 Community**: Reddit r/LogitechG

## Quick Reference Commands

```bash
# Start testing session
cd ~/projects/G13LogitechOPS
source .venv/bin/activate
g13-ops > button_test_output.txt 2>&1

# Launch GUI for verification
g13-ops-gui

# View raw device info
lsusb -v -d 046d:c21c

# Monitor all HID events (alternative method)
sudo evtest /dev/input/eventX  # Find X with: ls /dev/input/
```

## Time Estimate

- **Initial setup**: 5 minutes
- **Systematic button testing**: 15-20 minutes (25 buttons)
- **Data analysis**: 10-15 minutes
- **Code update & testing**: 10 minutes

**Total**: ~45 minutes to 1 hour

Good luck with the reverse engineering! 🎮🔧
