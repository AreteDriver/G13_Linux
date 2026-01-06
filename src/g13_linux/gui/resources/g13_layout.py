"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Coordinates based on 1024x1024 background image with auto-detected boxes.
"""

# Overall dimensions
KEYBOARD_WIDTH = 1024
KEYBOARD_HEIGHT = 1024

# Key sizing based on detected boxes
KEY_W = 32
KEY_H = 24
M_KEY_W = 31
M_KEY_H = 21
WIDE_KEY_W = 49


def _box(x, y, w, h):
    """Create position dict from x, y, width, height."""
    return {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}


# Button positions based on debug image analysis
# Standard G13 layout: G1-G14 top section, G15-G19 row 3, G20-G22 row 4
# Reference: g13_button_map_autodetect.json coordinates
G13_BUTTON_POSITIONS = {
    # M-keys row (small keys below LCD) - from K02-K05
    "M1": _box(419, 412, M_KEY_W, M_KEY_H),
    "M2": _box(456, 412, 32, 22),
    "M3": _box(495, 413, M_KEY_W, 23),
    "MR": _box(534, 413, M_KEY_W, 23),

    # G13 (left tall key) - K01
    "G13": _box(361, 402, 51, 27),

    # G14 (right small key) - K06
    "G14": _box(571, 415, 33, 18),

    # Row 1: G1-G7 - from K07, K09-K13, K08
    "G1": _box(373, 437, 37, 27),      # K07 - leftmost
    "G2": _box(416, 442, 33, 25),      # K09
    "G3": _box(455, 443, 33, 26),      # K10
    "G4": _box(495, 446, 32, 24),      # K13
    "G5": _box(533, 445, 33, 24),      # K12
    "G6": _box(572, 443, 34, 25),      # K11
    "G7": _box(611, 439, 38, 27),      # K08 - rightmost

    # Row 2: G8-G12 - from K14, K16-K18, K15
    "G8": _box(397, 478, 50, 26),      # K14 - wide left
    "G9": _box(452, 481, 34, 25),      # K16
    "G10": _box(493, 482, 33, 26),     # K17
    "G11": _box(534, 482, 33, 26),     # K18
    "G12": _box(574, 479, 49, 28),     # K15 - wide right

    # Row 3: G15-G19 - narrower row in the device waist
    "G15": _box(418, 508, 30, 22),
    "G16": _box(454, 510, 30, 22),
    "G17": _box(490, 512, 30, 22),
    "G18": _box(526, 510, 30, 22),
    "G19": _box(562, 508, 30, 22),

    # Row 4: G20-G22 (bottom keys before palm rest)
    "G20": _box(440, 538, 38, 22),
    "G21": _box(484, 540, 38, 22),
    "G22": _box(528, 538, 38, 22),

    # Thumb buttons - on the right side of device
    "LEFT": _box(618, 530, 28, 32),    # Upper thumb button
    "DOWN": _box(625, 568, 50, 30),    # Lower thumb button

    # Joystick click - button on the stick itself (clicking the thumbstick)
    "STICK": _box(620, 478, 45, 45),
}

# Joystick area (for visual indicator) - centered on the actual thumbstick
# The G13 thumbstick is located between the keyboard area and the thumb buttons
JOYSTICK_AREA = {"x": 618, "y": 476, "width": 50, "height": 50}

# LCD display area
LCD_AREA = {"x": 410, "y": 340, "width": 200, "height": 60}
