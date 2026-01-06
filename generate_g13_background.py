#!/usr/bin/env python3
"""
Generate a G13 background image that matches button overlay positions exactly.
Styled to look like the actual Logitech G13 with green LED edge lighting.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Import layout from the project
from src.g13_linux.gui.resources.g13_layout import (
    G13_BUTTON_POSITIONS,
    JOYSTICK_AREA,
    LCD_AREA,
    KEYBOARD_WIDTH,
    KEYBOARD_HEIGHT,
)


def create_g13_background():
    """Generate a stylized G13 device background image."""

    # Create base image with dark background
    img = Image.new('RGB', (KEYBOARD_WIDTH, KEYBOARD_HEIGHT), (20, 20, 22))
    draw = ImageDraw.Draw(img)

    # Device body dimensions
    body_margin = 50
    body_top = 40
    body_bottom = KEYBOARD_HEIGHT - 80

    # Draw green LED edge glow (characteristic G13 lighting)
    for i in range(8):
        glow_intensity = 80 - i * 10
        glow_color = (0, glow_intensity, 0)
        offset = 8 - i
        draw.rounded_rectangle(
            [body_margin - offset, body_top - offset,
             KEYBOARD_WIDTH - body_margin + offset, body_bottom + offset],
            radius=25, outline=glow_color, width=1
        )

    # Main device body
    draw.rounded_rectangle(
        [body_margin, body_top, KEYBOARD_WIDTH - body_margin, body_bottom],
        radius=20, fill=(45, 45, 48)
    )

    # Inner body (slightly darker)
    inner_margin = 8
    draw.rounded_rectangle(
        [body_margin + inner_margin, body_top + inner_margin,
         KEYBOARD_WIDTH - body_margin - inner_margin, body_bottom - inner_margin],
        radius=15, fill=(35, 35, 38)
    )

    # LCD display area with bezel
    lcd = LCD_AREA
    # LCD outer bezel (green tinted)
    draw.rounded_rectangle(
        [lcd["x"] - 15, lcd["y"] - 15,
         lcd["x"] + lcd["width"] + 15, lcd["y"] + lcd["height"] + 15],
        radius=5, fill=(20, 35, 20)
    )
    # LCD inner bezel
    draw.rounded_rectangle(
        [lcd["x"] - 5, lcd["y"] - 5,
         lcd["x"] + lcd["width"] + 5, lcd["y"] + lcd["height"] + 5],
        radius=3, fill=(10, 10, 12)
    )
    # LCD screen (dark with slight green tint)
    draw.rectangle(
        [lcd["x"], lcd["y"], lcd["x"] + lcd["width"], lcd["y"] + lcd["height"]],
        fill=(5, 12, 5)
    )

    # Key area background panel
    key_panel = [140, 255, 670, 530]
    draw.rounded_rectangle(key_panel, radius=15, fill=(28, 28, 32))

    # Draw button recesses with realistic styling
    for button_id, pos in G13_BUTTON_POSITIONS.items():
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]

        # Skip thumb buttons and stick for different treatment
        if button_id in ("LEFT", "DOWN", "STICK"):
            continue

        # Button well/recess (shadow)
        draw.rounded_rectangle(
            [x - 3, y - 3, x + w + 3, y + h + 3],
            radius=6, fill=(15, 15, 18)
        )

        # Key cap with gradient effect
        key_color = (42, 42, 46)
        draw.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=key_color)

        # Key cap top highlight
        draw.rounded_rectangle(
            [x + 2, y + 2, x + w - 2, y + h // 3],
            radius=3, fill=(52, 52, 56)
        )

    # Thumb button area (LEFT, DOWN)
    for btn_id in ("LEFT", "DOWN"):
        pos = G13_BUTTON_POSITIONS[btn_id]
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        # Recess
        draw.rounded_rectangle([x - 2, y - 2, x + w + 2, y + h + 2], radius=4, fill=(18, 18, 20))
        # Button
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(38, 38, 42))

    # Joystick area
    js = JOYSTICK_AREA
    center_x = js["x"] + js["width"] // 2
    center_y = js["y"] + js["height"] // 2
    radius = js["width"] // 2

    # Joystick housing (outer ring)
    draw.ellipse(
        [center_x - radius - 12, center_y - radius - 12,
         center_x + radius + 12, center_y + radius + 12],
        fill=(25, 25, 28), outline=(35, 35, 38), width=2
    )

    # Inner movement area
    draw.ellipse(
        [center_x - radius, center_y - radius,
         center_x + radius, center_y + radius],
        fill=(18, 18, 20)
    )

    # Joystick stick
    stick_radius = 20
    # Shadow
    draw.ellipse(
        [center_x - stick_radius + 3, center_y - stick_radius + 3,
         center_x + stick_radius + 3, center_y + stick_radius + 3],
        fill=(12, 12, 14)
    )
    # Stick base
    draw.ellipse(
        [center_x - stick_radius, center_y - stick_radius,
         center_x + stick_radius, center_y + stick_radius],
        fill=(45, 45, 50)
    )
    # Stick top (concave look)
    draw.ellipse(
        [center_x - stick_radius + 5, center_y - stick_radius + 5,
         center_x + stick_radius - 5, center_y + stick_radius - 5],
        fill=(55, 55, 60)
    )
    # Center dimple
    draw.ellipse(
        [center_x - 6, center_y - 6, center_x + 6, center_y + 6],
        fill=(40, 40, 45)
    )

    # Palm rest area
    palm_top = 620
    draw.rounded_rectangle(
        [80, palm_top, KEYBOARD_WIDTH - 80, body_bottom - 20],
        radius=40, fill=(32, 32, 35)
    )

    # "Logitech" text at bottom
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except OSError:
        font = ImageFont.load_default()

    text = "Logitech"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (KEYBOARD_WIDTH - text_width) // 2
    text_y = KEYBOARD_HEIGHT - 140
    draw.text((text_x, text_y), text, fill=(70, 70, 75), font=font)

    # "G13" text below
    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except OSError:
        font_small = font
    g13_text = "G13"
    g13_bbox = draw.textbbox((0, 0), g13_text, font=font_small)
    g13_width = g13_bbox[2] - g13_bbox[0]
    draw.text(((KEYBOARD_WIDTH - g13_width) // 2, text_y + 35), g13_text, fill=(60, 60, 65), font=font_small)

    # Save the image
    output_path = "src/g13_linux/gui/resources/images/g13_device.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")
    print(f"Dimensions: {KEYBOARD_WIDTH}x{KEYBOARD_HEIGHT}")

    return img


if __name__ == "__main__":
    create_g13_background()
