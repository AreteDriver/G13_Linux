#!/usr/bin/env python3
"""
Generate G13 device image matching the real Logitech G13.

Key characteristics from reference photos:
- Ergonomic curved body (like a hand rest)
- Keys arranged in arcs following finger reach
- Large curved palm rest with integrated thumbstick
- Silver/gray side accents
- LCD at top center
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Canvas - portrait, sized to fit the curved shape
WIDTH = 520
HEIGHT = 700

# Colors
BLACK = (20, 22, 25)
BODY_DARK = (35, 38, 42)
BODY_MID = (50, 53, 58)
KEY_BASE = (45, 48, 52)
KEY_TOP = (65, 68, 72)
KEY_LIGHT = (80, 83, 88)
SILVER = (130, 135, 142)
SILVER_DARK = (95, 100, 108)
SILVER_LIGHT = (160, 165, 172)
LCD_DARK = (10, 20, 10)
LCD_GREEN = (60, 140, 60)


def rotate_point(x, y, cx, cy, angle_deg):
    """Rotate point (x,y) around center (cx,cy) by angle in degrees."""
    angle = math.radians(angle_deg)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    dx, dy = x - cx, y - cy
    return (cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a)


def draw_rounded_key(draw, cx, cy, w, h, angle=0, radius=5, label=None, font=None):
    """Draw a key centered at (cx, cy) with optional rotation and label."""
    # For rotated keys, we draw a polygon approximation
    hw, hh = w / 2, h / 2

    # Key corners (before rotation)
    corners = [
        (cx - hw + radius, cy - hh),
        (cx + hw - radius, cy - hh),
        (cx + hw, cy - hh + radius),
        (cx + hw, cy + hh - radius),
        (cx + hw - radius, cy + hh),
        (cx - hw + radius, cy + hh),
        (cx - hw, cy + hh - radius),
        (cx - hw, cy - hh + radius),
    ]

    if angle != 0:
        corners = [rotate_point(x, y, cx, cy, angle) for x, y in corners]

    # Shadow
    shadow = [(x + 2, y + 2) for x, y in corners]
    draw.polygon(shadow, fill=(15, 17, 20))

    # Key base
    draw.polygon(corners, fill=KEY_BASE, outline=(55, 58, 62))

    # Key top surface (inset)
    inset = 3
    inner_hw, inner_hh = hw - inset, hh - inset
    inner_corners = [
        (cx - inner_hw + radius, cy - inner_hh),
        (cx + inner_hw - radius, cy - inner_hh),
        (cx + inner_hw, cy - inner_hh + radius),
        (cx + inner_hw, cy + inner_hh - radius - 2),
        (cx + inner_hw - radius, cy + inner_hh - 2),
        (cx - inner_hw + radius, cy + inner_hh - 2),
        (cx - inner_hw, cy + inner_hh - radius - 2),
        (cx - inner_hw, cy - inner_hh + radius),
    ]

    if angle != 0:
        inner_corners = [rotate_point(x, y, cx, cy, angle) for x, y in inner_corners]

    draw.polygon(inner_corners, fill=KEY_TOP)

    # Draw label
    if label and font:
        draw.text((cx, cy - 1), label, fill=(140, 145, 150), font=font, anchor="mm")


def draw_m_key(draw, cx, cy, w, h, label=None, font=None):
    """Draw smaller M-key."""
    hw, hh = w / 2, h / 2
    # Shadow
    draw.rounded_rectangle(
        (cx - hw + 1, cy - hh + 1, cx + hw + 1, cy + hh + 1),
        radius=3, fill=(18, 20, 22)
    )
    # Key
    draw.rounded_rectangle(
        (cx - hw, cy - hh, cx + hw, cy + hh),
        radius=3, fill=(50, 53, 58), outline=(65, 68, 72)
    )
    # Label
    if label and font:
        draw.text((cx, cy), label, fill=(130, 135, 140), font=font, anchor="mm")


def main():
    img = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    # Load fonts for key labels
    try:
        font_key = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_m = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        font_thumb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font_key = ImageFont.load_default()
        font_m = font_key
        font_thumb = font_key

    # === MAIN BODY - Ergonomic curved shape ===
    # The G13 body curves like a hand rest - narrow top, wide curved bottom

    # Outer body shape (organic curve)
    body_points = [
        # Top edge (narrow, for LCD)
        (120, 25), (400, 25),
        # Right side curves out
        (440, 50), (470, 120), (485, 200),
        (495, 300), (500, 400),
        # Right side curves into palm rest
        (495, 480), (480, 540), (450, 590),
        # Bottom palm rest curve
        (400, 630), (320, 655), (200, 655), (120, 630),
        # Left side curves up
        (70, 590), (40, 540), (25, 480),
        (20, 400), (25, 300),
        (35, 200), (50, 120), (80, 50),
    ]

    # Shadow
    shadow = [(x + 4, y + 4) for x, y in body_points]
    draw.polygon(shadow, fill=(10, 11, 13))

    # Main body
    draw.polygon(body_points, fill=BODY_DARK, outline=(55, 58, 62))

    # Inner surface (slightly raised look)
    inner_points = [
        (130, 40), (390, 40),
        (425, 60), (455, 130), (468, 210),
        (478, 310), (482, 400),
        (478, 470), (465, 525), (438, 575),
        (390, 615), (315, 638), (205, 638), (130, 615),
        (82, 575), (55, 525), (42, 470),
        (38, 400), (42, 310),
        (52, 210), (65, 130), (95, 60),
    ]
    draw.polygon(inner_points, fill=BODY_MID)

    # === SILVER SIDE ACCENTS ===
    # Left accent (curved strip)
    left_silver = [
        (25, 200), (45, 200),
        (52, 310), (50, 420), (45, 500),
        (30, 480), (22, 400), (25, 300),
    ]
    draw.polygon(left_silver, fill=SILVER)
    # Highlight
    draw.line([(27, 220), (27, 380)], fill=SILVER_LIGHT, width=2)

    # Right accent
    right_silver = [
        (495, 200), (475, 200),
        (468, 310), (470, 420), (475, 500),
        (490, 480), (498, 400), (495, 300),
    ]
    draw.polygon(right_silver, fill=SILVER)
    draw.line([(493, 220), (493, 380)], fill=SILVER_LIGHT, width=2)

    # === LCD DISPLAY ===
    lcd_cx, lcd_cy = 260, 75
    lcd_w, lcd_h = 220, 70

    # Bezel
    draw.rounded_rectangle(
        (lcd_cx - lcd_w//2 - 10, lcd_cy - lcd_h//2 - 8,
         lcd_cx + lcd_w//2 + 10, lcd_cy + lcd_h//2 + 8),
        radius=6, fill=(28, 30, 34), outline=(45, 48, 52), width=2
    )

    # Screen
    draw.rectangle(
        (lcd_cx - lcd_w//2, lcd_cy - lcd_h//2,
         lcd_cx + lcd_w//2, lcd_cy + lcd_h//2),
        fill=LCD_DARK, outline=(25, 45, 25)
    )

    # Scanlines
    for y in range(lcd_cy - lcd_h//2 + 2, lcd_cy + lcd_h//2 - 2, 3):
        draw.line(
            (lcd_cx - lcd_w//2 + 3, y, lcd_cx + lcd_w//2 - 3, y),
            fill=(8, 25, 8), width=1
        )

    # === M-KEYS (below LCD) ===
    m_y = 130
    m_keys = [(185, "M1"), (230, "M2"), (275, "M3"), (320, "MR")]
    for mx, label in m_keys:
        draw_m_key(draw, mx, m_y, 38, 18, label=label, font=font_m)

    # === G-KEYS - Arranged in ARCS ===
    # The real G13 keys follow curved arcs matching finger reach
    # Each row is an arc, outer keys angled outward

    key_w, key_h = 46, 40

    # Row 1: G1-G7 (top arc)
    row1_y_base = 185
    row1_keys = [
        # (cx, cy, angle, label)
        (95,  row1_y_base + 18, -12, "G1"),
        (148, row1_y_base + 8,  -6,  "G2"),
        (201, row1_y_base + 2,  -2,  "G3"),
        (254, row1_y_base,       0,  "G4"),
        (307, row1_y_base + 2,   2,  "G5"),
        (360, row1_y_base + 8,   6,  "G6"),
        (413, row1_y_base + 18,  12, "G7"),
    ]

    for cx, cy, angle, label in row1_keys:
        draw_rounded_key(draw, cx, cy, key_w, key_h, angle, label=label, font=font_key)

    # Row 2: G8-G14
    row2_y_base = 240
    row2_keys = [
        (95,  row2_y_base + 18, -12, "G8"),
        (148, row2_y_base + 8,  -6,  "G9"),
        (201, row2_y_base + 2,  -2,  "G10"),
        (254, row2_y_base,       0,  "G11"),
        (307, row2_y_base + 2,   2,  "G12"),
        (360, row2_y_base + 8,   6,  "G13"),
        (413, row2_y_base + 18,  12, "G14"),
    ]

    for cx, cy, angle, label in row2_keys:
        draw_rounded_key(draw, cx, cy, key_w, key_h, angle, label=label, font=font_key)

    # Row 3: G15-G19 (5 keys, more centered)
    row3_y_base = 295
    row3_keys = [
        (135, row3_y_base + 12, -8, "G15"),
        (190, row3_y_base + 4,  -3, "G16"),
        (245, row3_y_base,       0, "G17"),
        (300, row3_y_base + 4,   3, "G18"),
        (355, row3_y_base + 12,  8, "G19"),
    ]

    for cx, cy, angle, label in row3_keys:
        draw_rounded_key(draw, cx, cy, key_w, key_h, angle, label=label, font=font_key)

    # Row 4: G20-G22 (3 wider keys - thumb/space row)
    row4_y_base = 355
    row4_keys = [
        (175, row4_y_base + 6, -4, "G20"),
        (245, row4_y_base,      0, "G21"),
        (315, row4_y_base + 6,  4, "G22"),
    ]

    for cx, cy, angle, label in row4_keys:
        draw_rounded_key(draw, cx, cy, key_w + 14, key_h + 6, angle, label=label, font=font_key)

    # === PALM REST with THUMBSTICK ===
    # Large curved area at bottom
    palm_cx, palm_cy = 350, 520

    # Palm rest surface (elliptical, darker)
    draw.ellipse(
        (palm_cx - 120, palm_cy - 90, palm_cx + 120, palm_cy + 90),
        fill=(30, 32, 36), outline=(45, 48, 52), width=2
    )

    # === THUMB BUTTONS (LEFT, DOWN) ===
    # To the left of thumbstick
    thumb_x = 265
    draw_rounded_key(draw, thumb_x, 480, 48, 36, 0, label="LEFT", font=font_thumb)
    draw_rounded_key(draw, thumb_x, 530, 48, 36, 0, label="DOWN", font=font_thumb)

    # === THUMBSTICK ===
    stick_cx, stick_cy = 385, 520

    # Outer housing
    draw.ellipse(
        (stick_cx - 48, stick_cy - 48, stick_cx + 48, stick_cy + 48),
        fill=(55, 58, 62), outline=(70, 73, 78), width=2
    )

    # Inner well
    draw.ellipse(
        (stick_cx - 38, stick_cy - 38, stick_cx + 38, stick_cy + 38),
        fill=(25, 27, 30), outline=(40, 42, 45)
    )

    # Stick shadow
    draw.ellipse(
        (stick_cx - 20 + 2, stick_cy - 20 + 2, stick_cx + 20 + 2, stick_cy + 20 + 2),
        fill=(12, 14, 16)
    )

    # Stick cap
    draw.ellipse(
        (stick_cx - 20, stick_cy - 20, stick_cx + 20, stick_cy + 20),
        fill=(50, 53, 58), outline=(65, 68, 72), width=2
    )

    # Stick top
    draw.ellipse(
        (stick_cx - 14, stick_cy - 14, stick_cx + 14, stick_cy + 14),
        fill=(60, 63, 68)
    )

    # Dimple
    draw.ellipse(
        (stick_cx - 5, stick_cy - 5, stick_cx + 5, stick_cy + 5),
        fill=(42, 45, 50)
    )

    # === BRANDING ===
    try:
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font_sm = ImageFont.load_default()
        font_lg = font_sm

    draw.text((260, 610), "LOGITECH", fill=(65, 68, 72), font=font_sm, anchor="mm")
    draw.text((260, 632), "G13", fill=(80, 83, 88), font=font_lg, anchor="mm")

    # Save
    img.save("src/g13_linux/gui/resources/images/g13_device.png")
    print(f"Saved: {WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
