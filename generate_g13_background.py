#!/usr/bin/env python3
"""
Generate a realistic G13 background image matching the actual device appearance.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# Import layout from the project
from src.g13_linux.gui.resources.g13_layout import (
    G13_BUTTON_POSITIONS,
    JOYSTICK_AREA,
    KEYBOARD_HEIGHT,
    KEYBOARD_WIDTH,
    LCD_AREA,
)


def draw_gradient_rect(draw, bbox, color1, color2, vertical=True):
    """Draw a rectangle with gradient fill."""
    x1, y1, x2, y2 = bbox
    if vertical:
        for y in range(int(y1), int(y2)):
            ratio = (y - y1) / (y2 - y1) if y2 != y1 else 0
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(x1, y), (x2, y)], fill=(r, g, b))
    else:
        for x in range(int(x1), int(x2)):
            ratio = (x - x1) / (x2 - x1) if x2 != x1 else 0
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(x, y1), (x, y2)], fill=(r, g, b))


def create_g13_background():
    """Generate a realistic G13 device background image."""

    # Create base image
    img = Image.new("RGBA", (KEYBOARD_WIDTH, KEYBOARD_HEIGHT), (30, 30, 32, 255))
    draw = ImageDraw.Draw(img)

    # === MAIN BODY SHAPE ===
    # The G13 has a distinctive trapezoidal shape - wider at top, narrower at bottom
    # with curved palm rest area

    body_color_dark = (25, 25, 28)
    body_color_mid = (35, 35, 38)
    chrome_mid = (100, 105, 110)

    # Outer chrome/silver trim - distinctive G13 styling
    # Left side chrome accent
    points_left_chrome = [
        (20, 80),
        (60, 30),
        (70, 30),
        (45, 100),
        (35, 200),
        (25, 400),
        (40, 580),
        (60, 620),
        (40, 620),
        (15, 580),
        (10, 400),
        (15, 150),
    ]
    draw.polygon(points_left_chrome, fill=chrome_mid)

    # Right side chrome accent
    points_right_chrome = [
        (KEYBOARD_WIDTH - 20, 80),
        (KEYBOARD_WIDTH - 60, 30),
        (KEYBOARD_WIDTH - 70, 30),
        (KEYBOARD_WIDTH - 45, 100),
        (KEYBOARD_WIDTH - 35, 200),
        (KEYBOARD_WIDTH - 25, 400),
        (KEYBOARD_WIDTH - 40, 580),
        (KEYBOARD_WIDTH - 60, 620),
        (KEYBOARD_WIDTH - 40, 620),
        (KEYBOARD_WIDTH - 15, 580),
        (KEYBOARD_WIDTH - 10, 400),
        (KEYBOARD_WIDTH - 15, 150),
    ]
    draw.polygon(points_right_chrome, fill=chrome_mid)

    # Main body - dark matte black
    body_points = [
        (60, 35),  # top left
        (KEYBOARD_WIDTH - 60, 35),  # top right
        (KEYBOARD_WIDTH - 40, 150),  # upper right
        (KEYBOARD_WIDTH - 35, 420),  # mid right
        (KEYBOARD_WIDTH - 50, 600),  # lower right
        (50, 600),  # lower left
        (35, 420),  # mid left
        (40, 150),  # upper left
    ]
    draw.polygon(body_points, fill=body_color_dark)

    # Inner body panel with slight gradient effect
    inner_points = [
        (70, 45),
        (KEYBOARD_WIDTH - 70, 45),
        (KEYBOARD_WIDTH - 55, 150),
        (KEYBOARD_WIDTH - 50, 400),
        (KEYBOARD_WIDTH - 65, 585),
        (65, 585),
        (50, 400),
        (55, 150),
    ]
    draw.polygon(inner_points, fill=body_color_mid)

    # === LCD DISPLAY AREA ===
    lcd = LCD_AREA

    # LCD housing/frame - raised bezel
    lcd_bezel = 12
    # Outer frame shadow
    draw.rounded_rectangle(
        [
            lcd["x"] - lcd_bezel - 3,
            lcd["y"] - lcd_bezel - 3,
            lcd["x"] + lcd["width"] + lcd_bezel + 3,
            lcd["y"] + lcd["height"] + lcd_bezel + 3,
        ],
        radius=8,
        fill=(20, 20, 22),
    )
    # Frame
    draw.rounded_rectangle(
        [
            lcd["x"] - lcd_bezel,
            lcd["y"] - lcd_bezel,
            lcd["x"] + lcd["width"] + lcd_bezel,
            lcd["y"] + lcd["height"] + lcd_bezel,
        ],
        radius=6,
        fill=(45, 45, 48),
    )
    # Inner bezel
    draw.rounded_rectangle(
        [lcd["x"] - 4, lcd["y"] - 4, lcd["x"] + lcd["width"] + 4, lcd["y"] + lcd["height"] + 4],
        radius=3,
        fill=(15, 15, 18),
    )
    # LCD screen - characteristic green/black
    draw.rectangle(
        [lcd["x"], lcd["y"], lcd["x"] + lcd["width"], lcd["y"] + lcd["height"]], fill=(5, 15, 5)
    )
    # Scanline hint
    for i in range(0, lcd["height"], 3):
        draw.line(
            [(lcd["x"], lcd["y"] + i), (lcd["x"] + lcd["width"], lcd["y"] + i)],
            fill=(8, 20, 8),
            width=1,
        )

    # === KEY AREA PANEL ===
    # Recessed area where keys sit
    key_panel = [80, 152, 480, 395]
    # Shadow
    draw.rounded_rectangle(
        [key_panel[0] - 3, key_panel[1] - 3, key_panel[2] + 3, key_panel[3] + 3],
        radius=12,
        fill=(15, 15, 18),
    )
    # Panel
    draw.rounded_rectangle(key_panel, radius=10, fill=(22, 22, 25))

    # === DRAW KEYS ===
    # M-keys (smaller, different style)
    for btn_id in ["M1", "M2", "M3", "MR"]:
        pos = G13_BUTTON_POSITIONS[btn_id]
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]

        # Key shadow/well
        draw.rounded_rectangle([x - 1, y - 1, x + w + 1, y + h + 2], radius=3, fill=(12, 12, 14))
        # Key base
        draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=(38, 38, 42))
        # Key top highlight
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + 4], radius=1, fill=(55, 55, 60))

    # G-keys (main programmable keys)
    for btn_id, pos in G13_BUTTON_POSITIONS.items():
        if btn_id.startswith("M") or btn_id in ("LEFT", "DOWN", "STICK"):
            continue

        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]

        # Key well/recess
        draw.rounded_rectangle([x - 2, y - 2, x + w + 2, y + h + 3], radius=4, fill=(12, 12, 14))

        # Key cap with 3D effect
        # Base
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(35, 35, 40))
        # Top surface (slightly lighter)
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + h - 2], radius=2, fill=(45, 45, 50))
        # Top edge highlight
        draw.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 6], radius=1, fill=(60, 60, 65))
        # Bottom edge shadow
        draw.line([(x + 3, y + h - 2), (x + w - 3, y + h - 2)], fill=(25, 25, 28), width=1)

    # === THUMB AREA (right side) ===
    # Palm rest bump for thumb area
    # Thumb rest curved surface
    draw.ellipse([500, 410, 750, 610], fill=(30, 30, 33))

    # Thumb buttons (LEFT, DOWN)
    for btn_id in ("LEFT", "DOWN"):
        pos = G13_BUTTON_POSITIONS[btn_id]
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        # Well
        draw.rounded_rectangle([x - 2, y - 2, x + w + 2, y + h + 2], radius=4, fill=(18, 18, 20))
        # Button
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(40, 40, 45))
        # Highlight
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + 4], radius=2, fill=(55, 55, 60))

    # === JOYSTICK ===
    js = JOYSTICK_AREA
    jx = js["x"] + js["width"] // 2
    jy = js["y"] + js["height"] // 2
    jr = js["width"] // 2

    # Outer housing ring (chrome/metal look)
    for i in range(3):
        shade = chrome_mid[0] - i * 15
        draw.ellipse(
            [jx - jr - 12 + i, jy - jr - 12 + i, jx + jr + 12 - i, jy + jr + 12 - i],
            fill=(shade, shade + 2, shade + 5),
            outline=(shade - 10, shade - 8, shade - 5),
            width=1,
        )

    # Inner recessed movement area
    draw.ellipse([jx - jr, jy - jr, jx + jr, jy + jr], fill=(18, 18, 20))

    # Stick shadow
    stick_r = 20
    draw.ellipse(
        [jx - stick_r + 3, jy - stick_r + 3, jx + stick_r + 3, jy + stick_r + 3], fill=(10, 10, 12)
    )

    # Stick base (rubber)
    draw.ellipse([jx - stick_r, jy - stick_r, jx + stick_r, jy + stick_r], fill=(45, 45, 50))

    # Stick top with concave texture
    draw.ellipse(
        [jx - stick_r + 4, jy - stick_r + 4, jx + stick_r - 4, jy + stick_r - 4], fill=(55, 55, 60)
    )

    # Concave grip pattern (radial lines)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = jx + int(6 * math.cos(rad))
        y1 = jy + int(6 * math.sin(rad))
        x2 = jx + int((stick_r - 6) * math.cos(rad))
        y2 = jy + int((stick_r - 6) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(48, 48, 52), width=1)

    # Center dimple
    draw.ellipse([jx - 5, jy - 5, jx + 5, jy + 5], fill=(40, 40, 44))

    # === PALM REST (left side) ===
    # Main palm rest area
    palm_points = [
        (50, 420),
        (480, 420),
        (450, 590),
        (80, 590),
    ]
    draw.polygon(palm_points, fill=(28, 28, 32))

    # Textured surface hint (subtle dots)
    for px in range(60, 470, 8):
        for py in range(430, 580, 8):
            if (px + py) % 16 == 0:
                draw.point((px, py), fill=(32, 32, 36))

    # === KEY LABELS ===
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    label_color = (90, 90, 95)

    for button_id, pos in G13_BUTTON_POSITIONS.items():
        if button_id == "STICK":
            continue
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]

        # Use smaller font for M-keys
        f = font_small if button_id.startswith("M") else font

        bbox = draw.textbbox((0, 0), button_id, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = x + (w - tw) // 2
        ty = y + (h - th) // 2
        draw.text((tx, ty), button_id, fill=label_color, font=f)

    # === BRANDING ===
    try:
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except OSError:
        brand_font = font

    # Logitech logo area (bottom center of palm rest)
    brand_text = "LOGITECH"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    tw = bbox[2] - bbox[0]
    draw.text((250 - tw // 2, 550), brand_text, fill=(55, 55, 60), font=brand_font)

    # G13 below
    try:
        g13_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    except OSError:
        g13_font = font
    draw.text((250 - 10, 568), "G13", fill=(50, 50, 55), font=g13_font)

    # Convert to RGB and save
    img_rgb = img.convert("RGB")

    output_path = "src/g13_linux/gui/resources/images/g13_device.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img_rgb.save(output_path, "PNG")
    print(f"Generated: {output_path}")
    print(f"Dimensions: {KEYBOARD_WIDTH}x{KEYBOARD_HEIGHT}")

    return img_rgb


if __name__ == "__main__":
    create_g13_background()
