#!/usr/bin/env python3
"""
Generate Fastwork-specific Premium slide + cover.
Same bg (premium_setup.png), same brand style — expanded messaging:
"not just portfolios — we design any Google Sheets system for you."

Outputs:
  images/slides/premium_setup/slide1_premium_setup_fastwork_th.png
  images/cover/cover_premium_setup_fastwork_th.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR  = "/Users/arnon/vokmon/study/piggywise"
BG_PATH   = os.path.join(BASE_DIR, "images/bg/premium_setup.png")
ICON_PATH = os.path.join(BASE_DIR, "logo/piggywise-icon.png")
SLIDE_OUT = os.path.join(BASE_DIR, "images/slides/premium_setup/slide1_premium_setup_fastwork_th.png")
COVER_OUT = os.path.join(BASE_DIR, "images/cover/cover_premium_setup_fastwork_th.png")

W, H = 1280, 720

BG       = (13,  13,  13)
GOLD     = (212, 160, 23)
WHITE    = (255, 255, 255)
OFFWHITE = (232, 224, 208)

F_AVENIR_HEAVY = ("/System/Library/Fonts/Avenir Next.ttc", 8)
F_KRUNGTHEP    = ("/System/Library/Fonts/Supplemental/Krungthep.ttf", 0)

def fnt(spec, size):
    path, index = spec
    return ImageFont.truetype(path, size, index=index)

def draw_tracked(draw, x, y, text, font_obj, color, tracking=2):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font_obj, fill=color)
        bbox = draw.textbbox((0, 0), ch, font=font_obj)
        cx += (bbox[2] - bbox[0]) + tracking

def tracked_width(draw, text, font_obj, tracking=2):
    w = 0
    for i, ch in enumerate(text):
        bbox = draw.textbbox((0, 0), ch, font=font_obj)
        w += bbox[2] - bbox[0]
        if i < len(text) - 1:
            w += tracking
    return w

icon_src = Image.open(ICON_PATH).convert("RGBA")

def get_icon(size):
    return icon_src.resize((size, size), Image.LANCZOS)

def load_bg():
    img = Image.open(BG_PATH).convert("RGB")
    return img.resize((W, H), Image.LANCZOS)

def apply_bg_left_heavy(base_img, ai_bg):
    base_img.paste(ai_bg, (0, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(W):
        text_fade = max(0.0, 1.0 - (x / 680) ** 1.8)
        alpha = int(25 + 175 * text_fade)
        d.line([(x, 0), (x, H)], fill=(13, 13, 13, alpha))
    base_img.paste(overlay, mask=overlay.split()[3])

def draw_brand_badge(img, draw):
    icon = get_icon(52)
    img.paste(icon, (44, 30), icon)
    draw_tracked(draw, 108, 42, "PIGGYWISE", fnt(F_AVENIR_HEAVY, 20), GOLD, tracking=3)

def draw_label_badge(draw, label, x, y):
    f = fnt(F_AVENIR_HEAVY, 13)
    tw = tracked_width(draw, label, f, tracking=3)
    px, py = 16, 8
    h = 30
    draw.rectangle([x, y, x + tw + px * 2, y + h], fill=GOLD)
    draw_tracked(draw, x + px, y + py - 1, label, f, BG, tracking=3)

def draw_accent_line(draw, y, x=44, length=300):
    draw.rectangle([x, y, x + length, y + 2], fill=GOLD)

def draw_bottom_tagline(draw):
    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H - 76, "INTELLIGENT INVESTING, SIMPLIFIED", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H - 50, "YOUR PERSONAL AI FINANCE COACH", f2, OFFWHITE, tracking=2)

def draw_feature_bullet(draw, x, y, text):
    dot_r = 5
    dot_cx = x + dot_r
    dot_cy = y + 18
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=GOLD)
    tx = x + dot_r * 2 + 14
    draw.text((tx, y), text, font=fnt(F_KRUNGTHEP, 26), fill=WHITE)

SLIDE_CONTENT = {
    "label":    "PREMIUM",
    "sub":      "ออกแบบระบบ Google Sheets ครบวงจร",
    "title":    "บริการพรีเมียม",
    "features": [
        "พอร์ตลงทุนส่วนตัว — ตั้งค่าพร้อมใช้งานทันที",
        "ระบบติดตามรายรับ-รายจ่าย ธุรกิจและส่วนตัว",
        "Dashboard เป้าหมาย รายได้ และกระแสเงินสด",
        "ระบบ CRM ติดตามลูกค้าสำหรับธุรกิจ SME",
        "บอกความต้องการ — เราออกแบบให้ครบในชีทเดียว",
    ],
}

COVER_CONTENT = {
    "label":    "PREMIUM",
    "sub":      "ออกแบบตามความต้องการของคุณ",
    "title":    "บริการพรีเมียม",
    "cta_lines": [
        "คุณมีไอเดีย เรามีทีมงาน",
        "ปรึกษาก่อน แล้วทำด้วยกัน",
        "Google Sheets × AI ตามแบบที่คุณต้องการ",
    ],
}

def render_slide(out_path):
    c = SLIDE_CONTENT
    img = Image.new("RGB", (W, H), BG)
    apply_bg_left_heavy(img, load_bg())
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 4, H], fill=GOLD)
    draw_brand_badge(img, draw)
    draw_label_badge(draw, c["label"], 44, 116)
    draw.text((44, 162), c["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
    draw.text((40, 198), c["title"], font=fnt(F_KRUNGTHEP, 86), fill=WHITE)

    bullet_y = 368
    for feat in c["features"]:
        draw_feature_bullet(draw, 44, bullet_y, feat)
        bullet_y += 48

    draw_accent_line(draw, H - 100)
    draw_accent_line(draw, H - 106, length=180)

    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H - 76, "CUSTOM SYSTEMS, BUILT WITH GOOGLE SHEETS & AI", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H - 50, "TELL US WHAT YOU NEED — WE BUILD IT TOGETHER", f2, OFFWHITE, tracking=2)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")

def render_cover(out_path):
    c = COVER_CONTENT
    img = Image.new("RGB", (W, H), BG)
    apply_bg_left_heavy(img, load_bg())
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 4, H], fill=GOLD)
    draw_brand_badge(img, draw)
    draw_label_badge(draw, c["label"], 44, 116)
    draw.text((44, 162), c["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
    draw.text((40, 198), c["title"], font=fnt(F_KRUNGTHEP, 86), fill=WHITE)

    # CTA block — larger line spacing, first line in gold
    cta_y = 370
    for i, line in enumerate(c["cta_lines"]):
        color = GOLD if i == 0 else WHITE
        draw.text((44, cta_y), line, font=fnt(F_KRUNGTHEP, 28 if i == 0 else 26), fill=color)
        cta_y += 52 if i == 0 else 44

    draw_accent_line(draw, H - 100)
    draw_accent_line(draw, H - 106, length=180)

    # Cover-specific bottom tagline
    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H - 76, "CUSTOM SYSTEMS, BUILT WITH GOOGLE SHEETS & AI", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H - 50, "TELL US WHAT YOU NEED — WE BUILD IT TOGETHER", f2, OFFWHITE, tracking=2)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")

if __name__ == "__main__":
    render_slide(SLIDE_OUT)
    render_cover(COVER_OUT)
    print("Done.")
