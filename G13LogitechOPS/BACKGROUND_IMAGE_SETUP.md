# G13 Background Image Setup

## Overview

The GUI now supports using a background image of the actual G13 keyboard layout! This makes the interface much more intuitive and visually appealing.

## Quick Setup

### Step 1: Save the G13 Layout Image

Save your G13 layout image to:
```
src/g13_ops/gui/resources/images/g13_layout.png
```

**OR**

```
src/g13_ops/gui/resources/images/g13_layout.jpg
```

### Step 2: Image Requirements

- **Format**: PNG or JPG
- **Recommended size**: 800-1200px width
- **Aspect ratio**: Should match actual G13 (~0.75 width/height)
- **View**: Top-down view showing all buttons clearly labeled

### Step 3: Launch the GUI

That's it! The GUI will automatically detect and use the background image.

```bash
cd ~/projects/G13LogitechOPS
source .venv/bin/activate
python3 -m g13_ops.gui.main
```

**OR** just click **"G13 Configuration GUI"** in your Ubuntu applications!

## What Changed

### Visual Improvements

1. **Background Image**: The actual G13 layout shows behind the buttons
2. **Semi-Transparent Buttons**: Buttons overlay the image with transparency
   - Unmapped buttons: 40% opacity (mostly see-through)
   - Mapped buttons: 60% opacity (blue tint)
   - Pressed buttons: 85% opacity (bright green)
3. **Accurate Layout**: Button positions match the actual hardware

### Button Positioning

The coordinates in `g13_layout.py` have been updated to match the actual G13 layout:

- **M-keys**: Horizontal row at top (M1, M2, M3, MR)
- **G1-G7**: Curved top row
- **G8-G14**: Curved second row
- **G15-G19**: Curved third row
- **G20-G22**: Bottom row (3 large buttons)
- **Joystick**: Right side with clickable button in center

## Fallback Behavior

If no background image is found, the GUI falls back to a simple outline drawing:
- Gray rounded rectangle for keyboard body
- Green rectangle for LCD area
- Still fully functional, just less visually appealing

## Finding a G13 Image

If you don't have a G13 layout image, you can:

1. **Google Search**: Search for "logitech g13 top view" or "logitech g13 layout"
2. **Official Sources**: Check Logitech's website for product images
3. **Create Your Own**: Take a photo of your G13 from directly above
4. **Use Screenshots**: Screenshot from Logitech Gaming Software

## Customization

### Adjust Button Transparency

Edit `src/g13_ops/gui/widgets/g13_button.py`:

```python
# In _update_style() method:
bg_color = "rgba(33, 150, 243, 0.6)"  # Last value is opacity (0.0-1.0)
#                                         ^
#                                         Change this (0.0 = invisible, 1.0 = opaque)
```

### Adjust Button Positions

If the buttons don't align perfectly with your image, edit:
```
src/g13_ops/gui/resources/g13_layout.py
```

Update the `x` and `y` coordinates in `G13_BUTTON_POSITIONS`.

### Change Widget Size

In `g13_layout.py`:
```python
KEYBOARD_WIDTH = 800   # Adjust width
KEYBOARD_HEIGHT = 1067 # Adjust height (maintain aspect ratio!)
```

## Technical Details

### How It Works

1. **Image Loading**: `ButtonMapperWidget._load_background_image()` checks for image files
2. **Scaling**: Image is scaled to fit widget dimensions while maintaining aspect ratio
3. **Drawing**: `paintEvent()` draws the image first, then buttons overlay on top
4. **Coordinates**: Button positions in `g13_layout.py` are absolute pixel coordinates

### Supported Image Locations

The GUI checks these paths in order:
1. `src/g13_ops/gui/resources/images/g13_layout.png`
2. `src/g13_ops/gui/resources/images/g13_layout.jpg`

## Example Image Requirements

**Good Image**:
- ✅ Top-down view (bird's eye)
- ✅ All buttons clearly visible and labeled
- ✅ High contrast between buttons and background
- ✅ Good resolution (at least 800px wide)

**Bad Image**:
- ❌ Perspective/angled view
- ❌ Buttons not labeled
- ❌ Low resolution or blurry
- ❌ Cropped or missing parts

## Troubleshooting

### Image Not Showing

1. **Check path**: Ensure image is in correct directory
   ```bash
   ls src/g13_ops/gui/resources/images/
   ```

2. **Check filename**: Must be exactly `g13_layout.png` or `g13_layout.jpg`

3. **Check format**: Only PNG and JPG supported

4. **Restart GUI**: Close and reopen the application

### Buttons Don't Align

The button positions are estimates based on a reference image. You may need to adjust:

1. Edit `src/g13_ops/gui/resources/g13_layout.py`
2. Modify `x` and `y` values for misaligned buttons
3. Test and iterate

**Tip**: Start with one button (e.g., G1), get it perfect, then adjust others relative to it.

### Image Looks Stretched

Make sure `KEYBOARD_WIDTH` and `KEYBOARD_HEIGHT` maintain the aspect ratio of your image.

Example:
- If image is 962x1280 pixels
- Aspect ratio = 962/1280 = 0.7515625
- If WIDTH = 800, then HEIGHT should be 800/0.7515625 ≈ 1064

## Future Enhancements

Potential improvements:
- [ ] Auto-detect button positions using image recognition
- [ ] Multiple theme support (light/dark backgrounds)
- [ ] Custom button colors/styles
- [ ] Animated button presses
- [ ] Profile-specific backgrounds

---

**Status**: Background image support ready! Just add your G13 image and you're set! 🎨
