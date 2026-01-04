"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Coordinates match the device background image (962x1280 pixels).
"""

G13_BUTTON_POSITIONS = {
    # M-keys row
    "M1": {"x": 218, "y": 278, "width": 62, "height": 29},
    "M2": {"x": 291, "y": 278, "width": 62, "height": 29},
    "M3": {"x": 365, "y": 278, "width": 62, "height": 29},
    "MR": {"x": 439, "y": 278, "width": 62, "height": 29},
    # G-keys Row 1 (G1-G7)
    "G1": {"x": 127, "y": 356, "width": 73, "height": 63},
    "G2": {"x": 210, "y": 340, "width": 73, "height": 63},
    "G3": {"x": 293, "y": 332, "width": 73, "height": 63},
    "G4": {"x": 377, "y": 332, "width": 73, "height": 63},
    "G5": {"x": 460, "y": 332, "width": 73, "height": 63},
    "G6": {"x": 543, "y": 340, "width": 73, "height": 63},
    "G7": {"x": 627, "y": 356, "width": 73, "height": 63},
    # G-keys Row 2 (G8-G14)
    "G8": {"x": 127, "y": 433, "width": 73, "height": 63},
    "G9": {"x": 210, "y": 422, "width": 73, "height": 63},
    "G10": {"x": 293, "y": 414, "width": 73, "height": 63},
    "G11": {"x": 377, "y": 414, "width": 73, "height": 63},
    "G12": {"x": 460, "y": 414, "width": 73, "height": 63},
    "G13": {"x": 543, "y": 422, "width": 73, "height": 63},
    "G14": {"x": 627, "y": 433, "width": 73, "height": 63},
    # G-keys Row 3 (G15-G19)
    "G15": {"x": 169, "y": 515, "width": 77, "height": 63},
    "G16": {"x": 257, "y": 507, "width": 77, "height": 63},
    "G17": {"x": 344, "y": 503, "width": 77, "height": 63},
    "G18": {"x": 431, "y": 507, "width": 77, "height": 63},
    "G19": {"x": 518, "y": 515, "width": 77, "height": 63},
    # G-keys Row 4 (G20-G22)
    "G20": {"x": 257, "y": 604, "width": 81, "height": 69},
    "G21": {"x": 348, "y": 596, "width": 81, "height": 69},
    "G22": {"x": 439, "y": 604, "width": 81, "height": 69},
    # Thumb buttons
    "LEFT": {"x": 605, "y": 627, "width": 50, "height": 46},
    "DOWN": {"x": 605, "y": 685, "width": 50, "height": 46},
    "TOP": {"x": 669, "y": 608, "width": 100, "height": 100},
}

# Joystick area (for visual indicator)
JOYSTICK_AREA = {"x": 669, "y": 608, "width": 100, "height": 100}

# LCD display area
LCD_AREA = {"x": 214, "y": 117, "width": 348, "height": 155}

# Overall dimensions
KEYBOARD_WIDTH = 962
KEYBOARD_HEIGHT = 1280
