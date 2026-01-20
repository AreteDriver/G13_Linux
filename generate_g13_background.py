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


def _draw_body_shape(draw, chrome_mid, body_color_dark, body_color_mid):
    """Draw the main G13 body outline and chrome trim."""
    # Left chrome accent
    points_left_chrome = [
        (20, 80), (60, 30), (70, 30), (45, 100), (35, 200),
        (25, 400), (40, 580), (60, 620), (40, 620), (15, 580), (10, 400), (15, 150),
    ]
    draw.polygon(points_left_chrome, fill=chrome_mid)

    # Right chrome accent
    points_right_chrome = [
        (KEYBOARD_WIDTH - 20, 80), (KEYBOARD_WIDTH - 60, 30), (KEYBOARD_WIDTH - 70, 30),
        (KEYBOARD_WIDTH - 45, 100), (KEYBOARD_WIDTH - 35, 200), (KEYBOARD_WIDTH - 25, 400),
        (KEYBOARD_WIDTH - 40, 580), (KEYBOARD_WIDTH - 60, 620), (KEYBOARD_WIDTH - 40, 620),
        (KEYBOARD_WIDTH - 15, 580), (KEYBOARD_WIDTH - 10, 400), (KEYBOARD_WIDTH - 15, 150),
    ]
    draw.polygon(points_right_chrome, fill=chrome_mid)

    # Main body
    body_points = [
        (60, 35), (KEYBOARD_WIDTH - 60, 35), (KEYBOARD_WIDTH - 40, 150),
        (KEYBOARD_WIDTH - 35, 420), (KEYBOARD_WIDTH - 50, 600), (50, 600), (35, 420), (40, 150),
    ]
    draw.polygon(body_points, fill=body_color_dark)

    # Inner body panel
    inner_points = [
        (70, 45), (KEYBOARD_WIDTH - 70, 45), (KEYBOARD_WIDTH - 55, 150),
        (KEYBOARD_WIDTH - 50, 400), (KEYBOARD_WIDTH - 65, 585), (65, 585), (50, 400), (55, 150),
    ]
    draw.polygon(inner_points, fill=body_color_mid)


def _draw_lcd_area(draw, lcd):
    """Draw the LCD display housing and screen."""
    lcd_bezel = 12
    # Outer frame shadow
    draw.rounded_rectangle(
        [lcd["x"] - lcd_bezel - 3, lcd["y"] - lcd_bezel - 3,
         lcd["x"] + lcd["width"] + lcd_bezel + 3, lcd["y"] + lcd["height"] + lcd_bezel + 3],
        radius=8, fill=(20, 20, 22),
    )
    # Frame
    draw.rounded_rectangle(
        [lcd["x"] - lcd_bezel, lcd["y"] - lcd_bezel,
         lcd["x"] + lcd["width"] + lcd_bezel, lcd["y"] + lcd["height"] + lcd_bezel],
        radius=6, fill=(45, 45, 48),
    )
    # Inner bezel
    draw.rounded_rectangle(
        [lcd["x"] - 4, lcd["y"] - 4, lcd["x"] + lcd["width"] + 4, lcd["y"] + lcd["height"] + 4],
        radius=3, fill=(15, 15, 18),
    )
    # LCD screen
    draw.rectangle(
        [lcd["x"], lcd["y"], lcd["x"] + lcd["width"], lcd["y"] + lcd["height"]], fill=(5, 15, 5)
    )
    # Scanlines
    for i in range(0, lcd["height"], 3):
        draw.line(
            [(lcd["x"], lcd["y"] + i), (lcd["x"] + lcd["width"], lcd["y"] + i)],
            fill=(8, 20, 8), width=1,
        )


def _draw_keys(draw):
    """Draw all G13 keys (M-keys and G-keys)."""
    # M-keys
    for btn_id in ["M1", "M2", "M3", "MR"]:
        pos = G13_BUTTON_POSITIONS[btn_id]
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        draw.rounded_rectangle([x - 1, y - 1, x + w + 1, y + h + 2], radius=3, fill=(12, 12, 14))
        draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=(38, 38, 42))
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + 4], radius=1, fill=(55, 55, 60))

    # G-keys
    for btn_id, pos in G13_BUTTON_POSITIONS.items():
        if btn_id.startswith("M") or btn_id in ("LEFT", "DOWN", "STICK"):
            continue
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        draw.rounded_rectangle([x - 2, y - 2, x + w + 2, y + h + 3], radius=4, fill=(12, 12, 14))
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(35, 35, 40))
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + h - 2], radius=2, fill=(45, 45, 50))
        draw.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 6], radius=1, fill=(60, 60, 65))
        draw.line([(x + 3, y + h - 2), (x + w - 3, y + h - 2)], fill=(25, 25, 28), width=1)


def _draw_joystick(draw, js, chrome_mid):
    """Draw the joystick area."""
    jx = js["x"] + js["width"] // 2
    jy = js["y"] + js["height"] // 2
    jr = js["width"] // 2

    # Outer chrome ring
    for i in range(3):
        shade = chrome_mid[0] - i * 15
        draw.ellipse(
            [jx - jr - 12 + i, jy - jr - 12 + i, jx + jr + 12 - i, jy + jr + 12 - i],
            fill=(shade, shade + 2, shade + 5), outline=(shade - 10, shade - 8, shade - 5), width=1,
        )
    draw.ellipse([jx - jr, jy - jr, jx + jr, jy + jr], fill=(18, 18, 20))

    # Stick
    stick_r = 20
    draw.ellipse([jx - stick_r + 3, jy - stick_r + 3, jx + stick_r + 3, jy + stick_r + 3], fill=(10, 10, 12))
    draw.ellipse([jx - stick_r, jy - stick_r, jx + stick_r, jy + stick_r], fill=(45, 45, 50))
    draw.ellipse([jx - stick_r + 4, jy - stick_r + 4, jx + stick_r - 4, jy + stick_r - 4], fill=(55, 55, 60))

    # Grip pattern
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1, y1 = jx + int(6 * math.cos(rad)), jy + int(6 * math.sin(rad))
        x2, y2 = jx + int((stick_r - 6) * math.cos(rad)), jy + int((stick_r - 6) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(48, 48, 52), width=1)
    draw.ellipse([jx - 5, jy - 5, jx + 5, jy + 5], fill=(40, 40, 44))


def create_g13_background():
    """Generate a realistic G13 device background image."""
    img = Image.new("RGBA", (KEYBOARD_WIDTH, KEYBOARD_HEIGHT), (30, 30, 32, 255))
    draw = ImageDraw.Draw(img)

    body_color_dark = (25, 25, 28)
    body_color_mid = (35, 35, 38)
    chrome_mid = (100, 105, 110)

    _draw_body_shape(draw, chrome_mid, body_color_dark, body_color_mid)
    _draw_lcd_area(draw, LCD_AREA)

    # Key area panel
    key_panel = [80, 152, 480, 395]
    draw.rounded_rectangle([key_panel[0] - 3, key_panel[1] - 3, key_panel[2] + 3, key_panel[3] + 3],
                           radius=12, fill=(15, 15, 18))
    draw.rounded_rectangle(key_panel, radius=10, fill=(22, 22, 25))

    _draw_keys(draw)

    # Thumb area
    draw.ellipse([500, 410, 750, 610], fill=(30, 30, 33))
    for btn_id in ("LEFT", "DOWN"):
        pos = G13_BUTTON_POSITIONS[btn_id]
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        draw.rounded_rectangle([x - 2, y - 2, x + w + 2, y + h + 2], radius=4, fill=(18, 18, 20))
        draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(40, 40, 45))
        draw.rounded_rectangle([x + 1, y + 1, x + w - 1, y + 4], radius=2, fill=(55, 55, 60))

    _draw_joystick(draw, JOYSTICK_AREA, chrome_mid)

    # Palm rest
    draw.polygon([(50, 420), (480, 420), (450, 590), (80, 590)], fill=(28, 28, 32))
    for px in range(60, 470, 8):
        for py in range(430, 580, 8):
            if (px + py) % 16 == 0:
                draw.point((px, py), fill=(32, 32, 36))

    # Key labels
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    for button_id, pos in G13_BUTTON_POSITIONS.items():
        if button_id == "STICK":
            continue
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        f = font_small if button_id.startswith("M") else font
        bbox = draw.textbbox((0, 0), button_id, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x + (w - tw) // 2, y + (h - th) // 2), button_id, fill=(90, 90, 95), font=f)

    # Branding
    try:
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        g13_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    except OSError:
        brand_font = g13_font = font
    bbox = draw.textbbox((0, 0), "LOGITECH", font=brand_font)
    draw.text((250 - (bbox[2] - bbox[0]) // 2, 550), "LOGITECH", fill=(55, 55, 60), font=brand_font)
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
