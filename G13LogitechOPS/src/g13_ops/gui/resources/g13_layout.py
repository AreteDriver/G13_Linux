"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Coordinates match the generated background image (962x1280 pixels).
"""

# Button positions for visual layout
# Format: 'button_id': {'x': int, 'y': int, 'width': int, 'height': int}
# Coordinates match exactly with the background image positions

G13_BUTTON_POSITIONS = {
    # M-keys row (horizontal at top: M1, M2, M3, MR)
    "M1": {"x": 250, "y": 265, "width": 90, "height": 45},
    "M2": {"x": 360, "y": 265, "width": 90, "height": 45},
    "M3": {"x": 470, "y": 265, "width": 90, "height": 45},
    "MR": {"x": 580, "y": 265, "width": 90, "height": 45},
    # G-keys Row 1 (G1-G7) - curved top row
    "G1": {"x": 125, "y": 355, "width": 70, "height": 65},
    "G2": {"x": 210, "y": 335, "width": 70, "height": 65},
    "G3": {"x": 295, "y": 325, "width": 70, "height": 65},
    "G4": {"x": 380, "y": 325, "width": 70, "height": 65},
    "G5": {"x": 465, "y": 325, "width": 70, "height": 65},
    "G6": {"x": 550, "y": 335, "width": 70, "height": 65},
    "G7": {"x": 635, "y": 355, "width": 70, "height": 65},
    # G-keys Row 2 (G8-G14) - curved second row
    "G8": {"x": 125, "y": 445, "width": 70, "height": 65},
    "G9": {"x": 210, "y": 425, "width": 70, "height": 65},
    "G10": {"x": 295, "y": 415, "width": 70, "height": 65},
    "G11": {"x": 380, "y": 415, "width": 70, "height": 65},
    "G12": {"x": 465, "y": 415, "width": 70, "height": 65},
    "G13": {"x": 550, "y": 425, "width": 70, "height": 65},
    "G14": {"x": 635, "y": 445, "width": 70, "height": 65},
    # G-keys Row 3 (G15-G19) - curved third row
    "G15": {"x": 195, "y": 530, "width": 75, "height": 65},
    "G16": {"x": 285, "y": 515, "width": 75, "height": 65},
    "G17": {"x": 375, "y": 510, "width": 75, "height": 65},
    "G18": {"x": 465, "y": 515, "width": 75, "height": 65},
    "G19": {"x": 555, "y": 530, "width": 75, "height": 65},
    # G-keys Row 4 (G20-G22) - bottom row
    "G20": {"x": 285, "y": 650, "width": 85, "height": 70},
    "G21": {"x": 390, "y": 640, "width": 85, "height": 70},
    "G22": {"x": 500, "y": 650, "width": 85, "height": 70},
    # Thumb area buttons (near joystick)
    "LEFT": {"x": 640, "y": 720, "width": 55, "height": 50},  # Thumb button 1
    "DOWN": {"x": 640, "y": 780, "width": 55, "height": 50},  # Thumb button 2
    # Joystick click (press down on stick)
    "TOP": {"x": 720, "y": 750, "width": 120, "height": 120},
}

# Joystick area (visual outline - drawn by background image)
JOYSTICK_AREA = {"x": 710, "y": 770, "width": 150, "height": 150}

# LCD display area (top of device)
LCD_AREA = {"x": 230, "y": 95, "width": 505, "height": 130}

# Overall keyboard dimensions (matches generated image exactly)
KEYBOARD_WIDTH = 962
KEYBOARD_HEIGHT = 1280
