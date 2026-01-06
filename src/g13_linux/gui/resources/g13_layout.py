"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Coordinates match the device background image (962x1280 pixels).

Button positions are carefully aligned to the actual G13 device image
so that the semi-transparent button overlays sit precisely over the
physical button locations.
"""

G13_BUTTON_POSITIONS = {
    # M-keys row (below LCD, horizontal row of mode buttons)
    # These are the smaller rectangular buttons: M1, M2, M3, MR
    "M1": {"x": 303, "y": 293, "width": 58, "height": 26},
    "M2": {"x": 375, "y": 293, "width": 58, "height": 26},
    "M3": {"x": 447, "y": 293, "width": 58, "height": 26},
    "MR": {"x": 519, "y": 293, "width": 58, "height": 26},

    # G-keys Row 1 (G1-G7) - top row of main keys, curved layout
    # Keys curve down at edges (G1 and G7 are lower than center keys)
    "G1": {"x": 90, "y": 370, "width": 58, "height": 48},
    "G2": {"x": 158, "y": 355, "width": 58, "height": 48},
    "G3": {"x": 226, "y": 345, "width": 58, "height": 48},
    "G4": {"x": 294, "y": 340, "width": 58, "height": 48},
    "G5": {"x": 362, "y": 345, "width": 58, "height": 48},
    "G6": {"x": 430, "y": 355, "width": 58, "height": 48},
    "G7": {"x": 498, "y": 370, "width": 58, "height": 48},

    # G-keys Row 2 (G8-G14) - second row, also curved
    "G8": {"x": 90, "y": 428, "width": 58, "height": 48},
    "G9": {"x": 158, "y": 418, "width": 58, "height": 48},
    "G10": {"x": 226, "y": 408, "width": 58, "height": 48},
    "G11": {"x": 294, "y": 403, "width": 58, "height": 48},
    "G12": {"x": 362, "y": 408, "width": 58, "height": 48},
    "G13": {"x": 430, "y": 418, "width": 58, "height": 48},
    "G14": {"x": 498, "y": 428, "width": 58, "height": 48},

    # G-keys Row 3 (G15-G19) - third row, 5 keys only (shifted right)
    "G15": {"x": 130, "y": 488, "width": 62, "height": 48},
    "G16": {"x": 202, "y": 478, "width": 62, "height": 48},
    "G17": {"x": 274, "y": 473, "width": 62, "height": 48},
    "G18": {"x": 346, "y": 478, "width": 62, "height": 48},
    "G19": {"x": 418, "y": 488, "width": 62, "height": 48},

    # G-keys Row 4 (G20-G22) - bottom row, 3 wider keys
    "G20": {"x": 168, "y": 548, "width": 72, "height": 52},
    "G21": {"x": 252, "y": 540, "width": 72, "height": 52},
    "G22": {"x": 336, "y": 548, "width": 72, "height": 52},

    # Thumb buttons (beside joystick on bottom-right palm rest)
    "LEFT": {"x": 598, "y": 618, "width": 52, "height": 45},
    "DOWN": {"x": 598, "y": 673, "width": 52, "height": 45},

    # Joystick click (STICK) - center of joystick area
    "STICK": {"x": 680, "y": 628, "width": 60, "height": 60},
}

# Joystick area (for visual indicator drawing)
# The thumbstick is at the bottom-right palm rest area
JOYSTICK_AREA = {"x": 665, "y": 610, "width": 90, "height": 90}

# LCD display area (green screen at top of device)
# 160x43 pixel monochrome display
LCD_AREA = {"x": 295, "y": 115, "width": 360, "height": 155}

# Overall dimensions matching the device image
KEYBOARD_WIDTH = 962
KEYBOARD_HEIGHT = 1280
