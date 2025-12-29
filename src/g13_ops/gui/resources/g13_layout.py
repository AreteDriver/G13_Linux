"""
G13 Button Layout Geometry

Defines the visual positions and sizes of all G13 buttons for the GUI.
Layout matches the physical Logitech G13 device exactly.

Physical G13 (portrait orientation - taller than wide):
- LCD at very top (centered)
- M1, M2, M3, MR buttons beside LCD on right
- G1-G22 keys in grid below
- Joystick at BOTTOM LEFT
- Palm rest at bottom
- Angular wedge shape (wider at top)
"""

# Key dimensions
KEY_W = 32
KEY_H = 28
SMALL_BTN_W = 24
SMALL_BTN_H = 18

# Base positions
LCD_TOP = 15
KEY_START_Y = 70

G13_BUTTON_POSITIONS = {
    # === M-keys: Right side of LCD area ===
    'M1': {'x': 200, 'y': 20, 'width': 28, 'height': 20},
    'M2': {'x': 232, 'y': 20, 'width': 28, 'height': 20},
    'M3': {'x': 264, 'y': 20, 'width': 28, 'height': 20},
    'MR': {'x': 296, 'y': 20, 'width': 28, 'height': 20},

    # === G-Key Row 1: G1-G7 ===
    'G1':  {'x': 70,  'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G2':  {'x': 105, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G3':  {'x': 140, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G4':  {'x': 175, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G5':  {'x': 210, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G6':  {'x': 245, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},
    'G7':  {'x': 280, 'y': KEY_START_Y,      'width': KEY_W, 'height': KEY_H},

    # === G-Key Row 2: G8-G14 (slight stagger) ===
    'G8':  {'x': 78,  'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G9':  {'x': 113, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G10': {'x': 148, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G11': {'x': 183, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G12': {'x': 218, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G13': {'x': 253, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},
    'G14': {'x': 288, 'y': KEY_START_Y + 32, 'width': KEY_W, 'height': KEY_H},

    # === G-Key Row 3: G15-G19 ===
    'G15': {'x': 86,  'y': KEY_START_Y + 64, 'width': KEY_W, 'height': KEY_H},
    'G16': {'x': 121, 'y': KEY_START_Y + 64, 'width': KEY_W, 'height': KEY_H},
    'G17': {'x': 156, 'y': KEY_START_Y + 64, 'width': KEY_W, 'height': KEY_H},
    'G18': {'x': 191, 'y': KEY_START_Y + 64, 'width': KEY_W, 'height': KEY_H},
    'G19': {'x': 226, 'y': KEY_START_Y + 64, 'width': KEY_W, 'height': KEY_H},

    # === G-Key Row 4: G20-G22 (thumb row - left side) ===
    'G20': {'x': 70,  'y': KEY_START_Y + 100, 'width': 40, 'height': 30},
    'G21': {'x': 115, 'y': KEY_START_Y + 100, 'width': 40, 'height': 30},
    'G22': {'x': 160, 'y': KEY_START_Y + 100, 'width': 40, 'height': 30},

    # === Utility buttons (small, near LCD) ===
    'BD': {'x': 40, 'y': 25, 'width': 22, 'height': 16},
    'L1': {'x': 40, 'y': 45, 'width': 22, 'height': 16},
    'L2': {'x': 40, 'y': 65, 'width': 22, 'height': 16},
    'L3': {'x': 40, 'y': 85, 'width': 22, 'height': 16},
    'L4': {'x': 40, 'y': 105, 'width': 22, 'height': 16},
}

# Joystick area - BOTTOM RIGHT of device (where thumb rests)
JOYSTICK_AREA = {'x': 270, 'y': 200, 'width': 70, 'height': 70}

# LCD display area (top center)
LCD_AREA = {'x': 70, 'y': 12, 'width': 120, 'height': 35}

# Overall widget dimensions (portrait - taller than wide)
KEYBOARD_WIDTH = 365
KEYBOARD_HEIGHT = 310

# Device body shape - angular wedge matching G13
# Joystick bump on the RIGHT side
DEVICE_OUTLINE = [
    (30, 8),        # Top-left
    (320, 8),       # Top-right
    (350, 50),      # Upper-right corner
    (355, 190),     # Right side before joystick
    (355, 290),     # Right side joystick area
    (280, 300),     # Bottom-right
    (85, 300),      # Bottom-left
    (15, 200),      # Left side
    (10, 50),       # Upper-left corner
    (30, 8),        # Back to start
]

# Thumb/joystick rest area on RIGHT side
THUMB_REST_OUTLINE = [
    (220, 180),
    (355, 180),
    (355, 290),
    (280, 300),
    (220, 280),
    (220, 180),
]
