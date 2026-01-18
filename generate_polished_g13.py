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

import math

from PIL import Image, ImageDraw, ImageFont

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

# Default backlight color (orange like real G13)
BACKLIGHT_COLOR = (255, 120, 0)
BACKLIGHT_INTENSITY = 0.4  # 0.0 to 1.0


def rotate_point(x, y, cx, cy, angle_deg):
    """Rotate point (x,y) around center (cx,cy) by angle in degrees."""
    angle = math.radians(angle_deg)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    dx, dy = x - cx, y - cy
    return (cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a)


def draw_key_glow(draw, cx, cy, w, h, color, intensity=0.4):
    """Draw a soft glow behind a key."""
    # Draw multiple expanding rectangles with decreasing opacity
    r, g, b = color
    for i in range(8, 0, -1):
        expand = i * 2
        glow_color = (
            int(r * 0.3 + 20),
            int(g * 0.3 + 20),
            int(b * 0.3 + 20),
        )
        # Blend with background
        blend = i / 8
        blended = (
            int(glow_color[0] * (1 - blend) + BODY_MID[0] * blend),
            int(glow_color[1] * (1 - blend) + BODY_MID[1] * blend),
            int(glow_color[2] * (1 - blend) + BODY_MID[2] * blend),
        )
        draw.rounded_rectangle(
            (cx - w / 2 - expand, cy - h / 2 - expand, cx + w / 2 + expand, cy + h / 2 + expand),
            radius=8 + i,
            fill=blended,
        )


def draw_rounded_key(
    draw, cx, cy, w, h, angle=0, radius=5, label=None, font=None, backlight=None, intensity=0.5
):
    """Draw a key centered at (cx, cy) with optional rotation, label, and backlight."""
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

    # Backlight glow (drawn before shadow)
    if backlight:
        r, g, b = backlight
        # Outer glow - larger, more diffuse
        glow_corners = [
            (cx - hw - 4 + radius, cy - hh - 4),
            (cx + hw + 4 - radius, cy - hh - 4),
            (cx + hw + 4, cy - hh - 4 + radius),
            (cx + hw + 4, cy + hh + 4 - radius),
            (cx + hw + 4 - radius, cy + hh + 4),
            (cx - hw - 4 + radius, cy + hh + 4),
            (cx - hw - 4, cy + hh + 4 - radius),
            (cx - hw - 4, cy - hh - 4 + radius),
        ]
        if angle != 0:
            glow_corners = [rotate_point(x, y, cx, cy, angle) for x, y in glow_corners]

        glow_color = (
            int(r * intensity * 0.4 + 30),
            int(g * intensity * 0.4 + 30),
            int(b * intensity * 0.4 + 30),
        )
        draw.polygon(glow_corners, fill=glow_color)

    # Shadow
    shadow = [(x + 2, y + 2) for x, y in corners]
    draw.polygon(shadow, fill=(15, 17, 20))

    # Key base with backlight tint
    if backlight:
        r, g, b = backlight
        base_color = (
            int(KEY_BASE[0] + r * intensity * 0.15),
            int(KEY_BASE[1] + g * intensity * 0.15),
            int(KEY_BASE[2] + b * intensity * 0.15),
        )
        outline_color = (
            min(255, int(60 + r * intensity * 0.3)),
            min(255, int(60 + g * intensity * 0.3)),
            min(255, int(60 + b * intensity * 0.3)),
        )
    else:
        base_color = KEY_BASE
        outline_color = (55, 58, 62)

    draw.polygon(corners, fill=base_color, outline=outline_color)

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

    # Key top with subtle backlight tint
    if backlight:
        r, g, b = backlight
        top_color = (
            int(KEY_TOP[0] + r * intensity * 0.1),
            int(KEY_TOP[1] + g * intensity * 0.1),
            int(KEY_TOP[2] + b * intensity * 0.1),
        )
    else:
        top_color = KEY_TOP

    draw.polygon(inner_corners, fill=top_color)

    # Draw label
    if label and font:
        # Tint label color with backlight
        if backlight:
            r, g, b = backlight
            label_color = (
                min(255, int(140 + r * intensity * 0.3)),
                min(255, int(145 + g * intensity * 0.3)),
                min(255, int(150 + b * intensity * 0.3)),
            )
        else:
            label_color = (140, 145, 150)
        draw.text((cx, cy - 1), label, fill=label_color, font=font, anchor="mm")


def draw_m_key(draw, cx, cy, w, h, label=None, font=None, backlight=None, intensity=0.5):
    """Draw smaller M-key with optional backlight."""
    hw, hh = w / 2, h / 2

    # Backlight glow
    if backlight:
        r, g, b = backlight
        glow_color = (
            int(r * intensity * 0.3 + 25),
            int(g * intensity * 0.3 + 25),
            int(b * intensity * 0.3 + 25),
        )
        draw.rounded_rectangle(
            (cx - hw - 3, cy - hh - 3, cx + hw + 3, cy + hh + 3), radius=5, fill=glow_color
        )

    # Shadow
    draw.rounded_rectangle(
        (cx - hw + 1, cy - hh + 1, cx + hw + 1, cy + hh + 1), radius=3, fill=(18, 20, 22)
    )

    # Key base with backlight tint
    if backlight:
        r, g, b = backlight
        key_color = (
            int(50 + r * intensity * 0.12),
            int(53 + g * intensity * 0.12),
            int(58 + b * intensity * 0.12),
        )
        outline_color = (
            min(255, int(65 + r * intensity * 0.2)),
            min(255, int(68 + g * intensity * 0.2)),
            min(255, int(72 + b * intensity * 0.2)),
        )
    else:
        key_color = (50, 53, 58)
        outline_color = (65, 68, 72)

    draw.rounded_rectangle(
        (cx - hw, cy - hh, cx + hw, cy + hh), radius=3, fill=key_color, outline=outline_color
    )

    # Label with backlight tint
    if label and font:
        if backlight:
            r, g, b = backlight
            label_color = (
                min(255, int(130 + r * intensity * 0.25)),
                min(255, int(135 + g * intensity * 0.25)),
                min(255, int(140 + b * intensity * 0.25)),
            )
        else:
            label_color = (130, 135, 140)
        draw.text((cx, cy), label, fill=label_color, font=font, anchor="mm")


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    # === MAIN BODY - Ergonomic curved shape ===
    # The G13 body curves like a hand rest - narrow top, wide curved bottom

    # Outer body shape (organic curve)
    body_points = [
        # Top edge (narrow, for LCD)
        (120, 25),
        (400, 25),
        # Right side curves out
        (440, 50),
        (470, 120),
        (485, 200),
        (495, 300),
        (500, 400),
        # Right side curves into palm rest
        (495, 480),
        (480, 540),
        (450, 590),
        # Bottom palm rest curve
        (400, 630),
        (320, 655),
        (200, 655),
        (120, 630),
        # Left side curves up
        (70, 590),
        (40, 540),
        (25, 480),
        (20, 400),
        (25, 300),
        (35, 200),
        (50, 120),
        (80, 50),
    ]

    # Shadow
    shadow = [(x + 4, y + 4) for x, y in body_points]
    draw.polygon(shadow, fill=(10, 11, 13))

    # Main body
    draw.polygon(body_points, fill=BODY_DARK, outline=(55, 58, 62))

    # Inner surface (slightly raised look)
    inner_points = [
        (130, 40),
        (390, 40),
        (425, 60),
        (455, 130),
        (468, 210),
        (478, 310),
        (482, 400),
        (478, 470),
        (465, 525),
        (438, 575),
        (390, 615),
        (315, 638),
        (205, 638),
        (130, 615),
        (82, 575),
        (55, 525),
        (42, 470),
        (38, 400),
        (42, 310),
        (52, 210),
        (65, 130),
        (95, 60),
    ]
    draw.polygon(inner_points, fill=BODY_MID)

    # === SILVER SIDE ACCENTS ===
    # Left accent (curved strip)
    left_silver = [
        (25, 200),
        (45, 200),
        (52, 310),
        (50, 420),
        (45, 500),
        (30, 480),
        (22, 400),
        (25, 300),
    ]
    draw.polygon(left_silver, fill=SILVER)
    # Highlight
    draw.line([(27, 220), (27, 380)], fill=SILVER_LIGHT, width=2)

    # Right accent
    right_silver = [
        (495, 200),
        (475, 200),
        (468, 310),
        (470, 420),
        (475, 500),
        (490, 480),
        (498, 400),
        (495, 300),
    ]
    draw.polygon(right_silver, fill=SILVER)
    draw.line([(493, 220), (493, 380)], fill=SILVER_LIGHT, width=2)

    # === LCD DISPLAY ===
    lcd_cx, lcd_cy = 260, 75
    lcd_w, lcd_h = 220, 70

    # Bezel
    draw.rounded_rectangle(
        (
            lcd_cx - lcd_w // 2 - 10,
            lcd_cy - lcd_h // 2 - 8,
            lcd_cx + lcd_w // 2 + 10,
            lcd_cy + lcd_h // 2 + 8,
        ),
        radius=6,
        fill=(28, 30, 34),
        outline=(45, 48, 52),
        width=2,
    )

    # Screen
    draw.rectangle(
        (lcd_cx - lcd_w // 2, lcd_cy - lcd_h // 2, lcd_cx + lcd_w // 2, lcd_cy + lcd_h // 2),
        fill=LCD_DARK,
        outline=(25, 45, 25),
    )

    # Scanlines
    for y in range(lcd_cy - lcd_h // 2 + 2, lcd_cy + lcd_h // 2 - 2, 3):
        draw.line(
            (lcd_cx - lcd_w // 2 + 3, y, lcd_cx + lcd_w // 2 - 3, y), fill=(8, 25, 8), width=1
        )

    # === KEY AREAS ===
    # Keys are NOT drawn here - Qt button widgets provide the key visuals
    # This background just shows the device body with recessed key areas

    # Key area background (slightly recessed look for where keys will go)
    key_area_rect = (60, 160, 450, 420)
    draw.rounded_rectangle(key_area_rect, radius=15, fill=(25, 27, 30), outline=(35, 38, 42))

    # === PALM REST with THUMBSTICK ===
    # Large curved area at bottom
    palm_cx, palm_cy = 350, 520

    # Palm rest surface (elliptical, darker)
    draw.ellipse(
        (palm_cx - 120, palm_cy - 90, palm_cx + 120, palm_cy + 90),
        fill=(30, 32, 36),
        outline=(45, 48, 52),
        width=2,
    )

    # === THUMB BUTTONS (LEFT, DOWN) ===
    # Not drawn here - Qt button widgets provide the visuals

    # === THUMBSTICK ===
    stick_cx, stick_cy = 385, 520

    # Outer housing
    draw.ellipse(
        (stick_cx - 48, stick_cy - 48, stick_cx + 48, stick_cy + 48),
        fill=(55, 58, 62),
        outline=(70, 73, 78),
        width=2,
    )

    # Inner well
    draw.ellipse(
        (stick_cx - 38, stick_cy - 38, stick_cx + 38, stick_cy + 38),
        fill=(25, 27, 30),
        outline=(40, 42, 45),
    )

    # Stick shadow
    draw.ellipse(
        (stick_cx - 20 + 2, stick_cy - 20 + 2, stick_cx + 20 + 2, stick_cy + 20 + 2),
        fill=(12, 14, 16),
    )

    # Stick cap
    draw.ellipse(
        (stick_cx - 20, stick_cy - 20, stick_cx + 20, stick_cy + 20),
        fill=(50, 53, 58),
        outline=(65, 68, 72),
        width=2,
    )

    # Stick top
    draw.ellipse((stick_cx - 14, stick_cy - 14, stick_cx + 14, stick_cy + 14), fill=(60, 63, 68))

    # Dimple
    draw.ellipse((stick_cx - 5, stick_cy - 5, stick_cx + 5, stick_cy + 5), fill=(42, 45, 50))

    # === BRANDING ===
    try:
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font_sm = ImageFont.load_default()
        font_lg = font_sm

    draw.text((260, 610), "LOGITECH", fill=(65, 68, 72), font=font_sm, anchor="mm")
    draw.text((260, 632), "G13", fill=(80, 83, 88), font=font_lg, anchor="mm")

    # Save
    img.save("src/g13_linux/gui/resources/images/g13_device.png")
    print(f"Saved: {WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
