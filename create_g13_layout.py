#!/usr/bin/env python3
"""
Generate a G13 keyboard layout image for the GUI background.
Based on the actual Logitech G13 hardware layout.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# Image dimensions (aspect ratio ~0.75 matching real G13)
WIDTH = 962
HEIGHT = 1280

# Colors
BG_COLOR = (30, 30, 30)  # Dark gray background
KEYBOARD_COLOR = (50, 50, 50)  # Slightly lighter for keyboard body
BUTTON_COLOR = (100, 100, 100)  # Gray for buttons
M_BUTTON_COLOR = (80, 80, 80)  # Darker for M-keys
LCD_COLOR = (20, 20, 20)  # Black for LCD
TEXT_COLOR = (220, 220, 220)  # Light gray text
ACCENT_COLOR = (100, 140, 100)  # Green accent

# Button layouts (approximate positions scaled to image size)
M_KEYS = [
    {"name": "M1", "x": 250, "y": 265, "w": 90, "h": 45},
    {"name": "M2", "x": 360, "y": 265, "w": 90, "h": 45},
    {"name": "M3", "x": 470, "y": 265, "w": 90, "h": 45},
    {"name": "MR", "x": 580, "y": 265, "w": 90, "h": 45},
]

# G-keys Row 1 (curved top row)
G_ROW1 = [
    {"name": "G1", "x": 125, "y": 355, "w": 70, "h": 65},
    {"name": "G2", "x": 210, "y": 335, "w": 70, "h": 65},
    {"name": "G3", "x": 295, "y": 325, "w": 70, "h": 65},
    {"name": "G4", "x": 380, "y": 325, "w": 70, "h": 65},
    {"name": "G5", "x": 465, "y": 325, "w": 70, "h": 65},
    {"name": "G6", "x": 550, "y": 335, "w": 70, "h": 65},
    {"name": "G7", "x": 635, "y": 355, "w": 70, "h": 65},
]

# G-keys Row 2
G_ROW2 = [
    {"name": "G8", "x": 125, "y": 445, "w": 70, "h": 65},
    {"name": "G9", "x": 210, "y": 425, "w": 70, "h": 65},
    {"name": "G10", "x": 295, "y": 415, "w": 70, "h": 65},
    {"name": "G11", "x": 380, "y": 415, "w": 70, "h": 65},
    {"name": "G12", "x": 465, "y": 415, "w": 70, "h": 65},
    {"name": "G13", "x": 550, "y": 425, "w": 70, "h": 65},
    {"name": "G14", "x": 635, "y": 445, "w": 70, "h": 65},
]

# G-keys Row 3
G_ROW3 = [
    {"name": "G15", "x": 195, "y": 530, "w": 75, "h": 65},
    {"name": "G16", "x": 285, "y": 515, "w": 75, "h": 65},
    {"name": "G17", "x": 375, "y": 510, "w": 75, "h": 65},
    {"name": "G18", "x": 465, "y": 515, "w": 75, "h": 65},
    {"name": "G19", "x": 555, "y": 530, "w": 75, "h": 65},
]

# G-keys Row 4 (bottom row - larger buttons)
G_ROW4 = [
    {"name": "G20", "x": 285, "y": 650, "w": 85, "h": 70},
    {"name": "G21", "x": 390, "y": 640, "w": 85, "h": 70},
    {"name": "G22", "x": 500, "y": 650, "w": 85, "h": 70},
]

# LCD area
LCD = {"x": 230, "y": 95, "w": 505, "h": 130}

# Joystick
JOYSTICK = {"x": 710, "y": 770, "w": 150, "h": 150}


def create_g13_layout():
    """Create the G13 layout image"""
    # Create image
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to load a font, fallback to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        ImageFont.load_default()

    # Draw keyboard body outline
    draw.rounded_rectangle(
        [50, 50, WIDTH - 50, HEIGHT - 50],
        radius=30,
        fill=KEYBOARD_COLOR,
        outline=ACCENT_COLOR,
        width=3,
    )

    # Draw LCD area
    draw.rectangle(
        [LCD["x"], LCD["y"], LCD["x"] + LCD["w"], LCD["y"] + LCD["h"]],
        fill=LCD_COLOR,
        outline=ACCENT_COLOR,
        width=2,
    )

    # Draw M-keys
    for btn in M_KEYS:
        draw.rounded_rectangle(
            [btn["x"], btn["y"], btn["x"] + btn["w"], btn["y"] + btn["h"]],
            radius=5,
            fill=M_BUTTON_COLOR,
            outline=(120, 120, 120),
            width=2,
        )
        # Center text
        bbox = draw.textbbox((0, 0), btn["name"], font=font_medium)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = btn["x"] + (btn["w"] - text_width) // 2
        text_y = btn["y"] + (btn["h"] - text_height) // 2
        draw.text((text_x, text_y), btn["name"], fill=TEXT_COLOR, font=font_medium)

    # Draw G-keys
    for row in [G_ROW1, G_ROW2, G_ROW3, G_ROW4]:
        for btn in row:
            draw.rounded_rectangle(
                [btn["x"], btn["y"], btn["x"] + btn["w"], btn["y"] + btn["h"]],
                radius=5,
                fill=BUTTON_COLOR,
                outline=(140, 140, 140),
                width=2,
            )
            # Center text
            bbox = draw.textbbox((0, 0), btn["name"], font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = btn["x"] + (btn["w"] - text_width) // 2
            text_y = btn["y"] + (btn["h"] - text_height) // 2
            draw.text((text_x, text_y), btn["name"], fill=TEXT_COLOR, font=font_medium)

    # Draw joystick area
    draw.ellipse(
        [
            JOYSTICK["x"],
            JOYSTICK["y"],
            JOYSTICK["x"] + JOYSTICK["w"],
            JOYSTICK["y"] + JOYSTICK["h"],
        ],
        fill=(60, 60, 60),
        outline=(140, 140, 140),
        width=3,
    )
    # Joystick center button
    center_x = JOYSTICK["x"] + JOYSTICK["w"] // 2
    center_y = JOYSTICK["y"] + JOYSTICK["h"] // 2
    draw.ellipse(
        [center_x - 30, center_y - 30, center_x + 30, center_y + 30],
        fill=(80, 80, 80),
        outline=(150, 150, 150),
        width=2,
    )

    # Draw Logitech logo area (simplified)
    logo_y = HEIGHT - 180
    draw.text((WIDTH // 2 - 80, logo_y), "Logitech", fill=(100, 100, 100), font=font_large)

    return img


if __name__ == "__main__":
    print("Creating G13 layout image...")
    img = create_g13_layout()

    # Save to GUI resources directory
    output_path = os.path.join(
        os.path.dirname(__file__),
        "src",
        "g13_linux",
        "gui",
        "resources",
        "images",
        "g13_layout.png",
    )

    img.save(output_path)
    print(f"✅ G13 layout image saved to: {output_path}")
    print(f"   Size: {WIDTH}x{HEIGHT} pixels")
    print("\nRestart the GUI to see the background image!")
