"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Coordinates based on reference image scaled 2x (510x396 from 255x198).
"""

# Overall dimensions (2x scale of reference image)
SCALE = 2
KEYBOARD_WIDTH = 255 * SCALE  # 510
KEYBOARD_HEIGHT = 198 * SCALE  # 396

# Key sizing (scaled)
KEY_W = 15 * SCALE  # 30
KEY_H = 12 * SCALE  # 24
M_KEY_W = 11 * SCALE  # 22
M_KEY_H = 6 * SCALE  # 12
WIDE_KEY_W = 20 * SCALE  # 40


def _c(cx, cy, w, h):
    """Convert center (cx, cy) to top-left dict, applying scale."""
    return {"x": int(cx * SCALE - w / 2), "y": int(cy * SCALE - h / 2), "width": w, "height": h}


G13_BUTTON_POSITIONS = {
    # M-keys row (below LCD) - y≈48
    "M1": _c(78, 48, M_KEY_W, M_KEY_H),
    "M2": _c(91, 48, M_KEY_W, M_KEY_H),
    "M3": _c(104, 48, M_KEY_W, M_KEY_H),
    "MR": _c(117, 48, M_KEY_W, M_KEY_H),
    # G-keys Row 1 (G1-G7) - y≈63, spacing ~17
    "G1": _c(50, 63, KEY_W, KEY_H),
    "G2": _c(67, 63, KEY_W, KEY_H),
    "G3": _c(84, 63, KEY_W, KEY_H),
    "G4": _c(101, 63, KEY_W, KEY_H),
    "G5": _c(118, 63, KEY_W, KEY_H),
    "G6": _c(135, 63, KEY_W, KEY_H),
    "G7": _c(152, 63, KEY_W, KEY_H),
    # G-keys Row 2 (G8-G14) - y≈78
    "G8": _c(50, 78, KEY_W, KEY_H),
    "G9": _c(67, 78, KEY_W, KEY_H),
    "G10": _c(84, 78, KEY_W, KEY_H),
    "G11": _c(101, 78, KEY_W, KEY_H),
    "G12": _c(118, 78, KEY_W, KEY_H),
    "G13": _c(135, 78, KEY_W, KEY_H),
    "G14": _c(152, 78, KEY_W, KEY_H),
    # G-keys Row 3 (G15-G19) - y≈93, offset right
    "G15": _c(58, 93, KEY_W, KEY_H),
    "G16": _c(75, 93, KEY_W, KEY_H),
    "G17": _c(92, 93, KEY_W, KEY_H),
    "G18": _c(109, 93, KEY_W, KEY_H),
    "G19": _c(126, 93, KEY_W, KEY_H),
    # G-keys Row 4 (G20-G22) - y≈108, wider keys
    "G20": _c(67, 108, WIDE_KEY_W, KEY_H),
    "G21": _c(92, 108, WIDE_KEY_W, KEY_H),
    "G22": _c(117, 108, WIDE_KEY_W, KEY_H),
    # Thumb buttons (left of thumbstick)
    "LEFT": _c(68, 140, KEY_W, int(KEY_H * 0.85)),
    "DOWN": _c(68, 156, KEY_W, int(KEY_H * 0.85)),
    # Joystick click
    "STICK": _c(168, 150, 26 * SCALE, 26 * SCALE),
}

# Joystick area (for visual indicator)
JOYSTICK_AREA = {"x": 152 * SCALE, "y": 132 * SCALE, "width": 32 * SCALE, "height": 32 * SCALE}

# LCD display area
LCD_AREA = {"x": 68 * SCALE, "y": 18 * SCALE, "width": 62 * SCALE, "height": 22 * SCALE}
