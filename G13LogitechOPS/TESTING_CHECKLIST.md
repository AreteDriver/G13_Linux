# G13 Button Mapping - Testing Checklist

## ✅ Confirmed Mappings (Hardware Tested)

- [x] **G1-G5** - Byte[3] bits 0-4 (100% confirmed)
- [x] **Joystick X-axis** - Byte[1] (100% confirmed)
- [x] **Joystick Y-axis** - Byte[2] (100% confirmed)
- [x] **MR Button** - Byte[7] bit 1 (0x02) (100% confirmed)

## ⚠️ Priority Testing Needed

### Joystick Button (Click Down)
- [ ] **JOYSTICK** - Predicted: Byte[7] bit 2 (0x04)
- **How to test**:
  1. Launch "G13 Button Capture" from Ubuntu dock
  2. Press ONLY the joystick button (click down firmly on the stick)
  3. Look for Byte[7] = 0x04 in the output
  4. If you see 0x04, the prediction is correct ✅
  5. If you see a different value, note which byte and value changed

## 🔮 Predicted Mappings (Need Testing)

### G-Keys Row 2 (Byte 3, bits 5-7)
- [ ] **G6** - Byte[3] bit 5 (0x20)
- [ ] **G7** - Byte[3] bit 6 (0x40)
- [ ] **G8** - Byte[3] bit 7 (0x80)

### G-Keys Row 3 (Byte 4, bits 0-7)
- [ ] **G9** - Byte[4] bit 0 (0x01)
- [ ] **G10** - Byte[4] bit 1 (0x02)
- [ ] **G11** - Byte[4] bit 2 (0x04)
- [ ] **G12** - Byte[4] bit 3 (0x08)
- [ ] **G13** - Byte[4] bit 4 (0x10)
- [ ] **G14** - Byte[4] bit 5 (0x20)
- [ ] **G15** - Byte[4] bit 6 (0x40)
- [ ] **G16** - Byte[4] bit 7 (0x80)

### G-Keys Row 4 (Byte 6, bits 0-5)
- [ ] **G17** - Byte[6] bit 0 (0x01)
- [ ] **G18** - Byte[6] bit 1 (0x02)
- [ ] **G19** - Byte[6] bit 2 (0x04)
- [ ] **G20** - Byte[6] bit 3 (0x08)
- [ ] **G21** - Byte[6] bit 4 (0x10)
- [ ] **G22** - Byte[6] bit 5 (0x20)

### M-Keys (Mode) (Byte 6-7)
- [ ] **M1** - Byte[6] bit 6 (0x40)
- [ ] **M2** - Byte[6] bit 7 (0x80)
- [ ] **M3** - Byte[7] bit 0 (0x01)

## Testing Methods

### Method 1: Use the Capture Tool (Recommended)
```bash
# Launch from Ubuntu dock: "G13 Button Capture"
# OR from command line:
cd ~/projects/G13LogitechOPS
sudo .venv/bin/python3 capture_hidapi.py
```

1. Press ONE button at a time
2. Note which byte changes and what value appears
3. Compare with predictions above

### Method 2: Use the GUI Live Monitor
```bash
# Launch from Ubuntu dock: "G13 Configuration GUI"
# OR from command line:
cd ~/projects/G13LogitechOPS
source .venv/bin/activate
python3 -m g13_ops.gui.main
```

1. Go to "Live Monitor" tab
2. Check "Show raw HID reports"
3. Press buttons one at a time
4. Watch which bytes change

## Quick Reference: HID Report Format

```
8-byte HID Report Structure:
[0] = Report ID (always 0x01)
[1] = Joystick X-axis (0x00-0xFF, centered ~0x78)
[2] = Joystick Y-axis (0x00-0xFF, centered ~0x7f)
[3] = G1-G8 buttons (bits 0-7)
[4] = G9-G16 buttons (bits 0-7) - PREDICTED
[5] = Joystick Z/twist (0x80 centered)
[6] = G17-G22 + M1-M2 (bits 0-7) - PREDICTED
[7] = M3 + MR + JOYSTICK (bits 0-2) - PARTIAL CONFIRMED
```

## Reporting Issues

If a button doesn't match the prediction:

1. **Note the button name** (e.g., G10)
2. **Note the raw data** when pressed (all 8 bytes)
3. **Note which byte changed** and what value it showed
4. **Update event_decoder.py** with the correct mapping

Example fix:
```python
# In event_decoder.py, update BUTTON_MAP:
'G10': (4, 1),  # Was predicted, found to be different
# Change to:
'G10': (5, 3),  # Correct byte and bit based on testing
```

## Testing Progress

**Last Updated**: 2024-12-24

**Completion Status**:
- Confirmed: 6/28 buttons (21%)
- High priority (JOYSTICK): 1 button
- Remaining: 21 buttons

**Next Action**: Test joystick button to verify Byte[7] bit 2 mapping
