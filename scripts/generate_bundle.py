#!/usr/bin/env python3
"""
Generate Bundle pack cover + slide 1 in both EN and TH.
Background: images/bg/premium_setup.png

Outputs:
  images/slides/bundle/slide1_bundle_th.png
  images/slides/bundle/slide1_bundle_en.png
  images/cover/cover_bundle_th.png
  images/cover/cover_bundle_en.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR  = "/Users/arnon/vokmon/study/piggywise"
BG_PATH   = os.path.join(BASE_DIR, "images/bg/premium_setup.png")
ICON_PATH = os.path.join(BASE_DIR, "logo/piggywise-icon.png")
SLIDES_DIR = os.path.join(BASE_DIR, "images/slides/bundle")
COVERS_DIR = os.path.join(BASE_DIR, "images/cover")

W, H = 1280, 720

BG       = (13,  13,  13)
GOLD     = (212, 160, 23)
WHITE    = (255, 255, 255)
OFFWHITE = (232, 224, 208)
DIM      = (170, 162, 148)

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

def draw_product_row(draw, x, y, name, desc, is_thai):
    f_name = fnt(F_KRUNGTHEP, 24) if is_thai else fnt(F_AVENIR_HEAVY, 22)
    f_desc = fnt(F_KRUNGTHEP, 22) if is_thai else fnt(F_AVENIR_HEAVY, 20)
    dot_r = 5
    dot_cx = x + dot_r
    dot_cy = y + 16
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=GOLD)
    tx = x + dot_r * 2 + 14
    if is_thai:
        draw.text((tx, y), name, font=f_name, fill=GOLD)
        name_w = draw.textbbox((0, 0), name, font=f_name)[2]
        draw.text((tx + name_w + 10, y + 2), desc, font=f_desc, fill=OFFWHITE)
    else:
        draw_tracked(draw, tx, y, name, f_name, GOLD, tracking=2)
        name_w = tracked_width(draw, name, f_name, tracking=2)
        draw_tracked(draw, tx + name_w + 10, y + 2, desc, f_desc, OFFWHITE, tracking=1)

CONTENT = {
    "th": {
        "slide": {
            "label": "BUNDLE",
            "sub":   "3 พอร์ต ครบทุกเป้าหมาย",
            "title": "3-in-1 Bundle",
            "products": [
                ("Aggressive Go",  "— พอร์ตสายรุก หุ้น + คริปโต"),
                ("Hybrid Wealth",  "— เติบโต + ปันผล ควบคู่กัน"),
                ("Retire Smooth",  "— วางแผนเกษียณระยะยาว"),
            ],
            "deliverables": [
                "Google Sheets Templates ทั้ง 3 ระบบ",
                "AI Prompt Library + คู่มือ PDF + Checklist รายเดือน",
                "เลือกใช้ 1 พอร์ตก่อน สลับได้ตามเป้าหมาย",
            ],
        },
        "cover": {
            "label": "BUNDLE",
            "sub":   "ลงทุนสม่ำเสมอ ทุกเป้าหมาย",
            "title": "3-in-1 Bundle",
            "hook_lines": [
                "ชีวิตเปลี่ยน — พอร์ตต้องตามทัน",
                "3 กลยุทธ์ ตอบทุกเป้าหมายการเงิน",
                "เริ่มจาก 1 พอร์ต แล้วสลับได้เสมอ",
            ],
        },
    },
    "en": {
        "slide": {
            "label": "BUNDLE",
            "sub":   "ALL THREE STRATEGIES, ONE PACK",
            "title": "3-in-1 Bundle",
            "products": [
                ("Aggressive Go",  "— High-growth: stocks + crypto"),
                ("Hybrid Wealth",  "— Growth + dividend income"),
                ("Retire Smooth",  "— Long-term retirement plan"),
            ],
            "deliverables": [
                "All 3 Google Sheets Templates",
                "AI Prompt Library + PDF Guide + Monthly Checklist",
                "Start with 1, switch anytime as your goals evolve",
            ],
        },
        "cover": {
            "label": "BUNDLE",
            "sub":   "INVEST WITH PURPOSE, EVERY GOAL",
            "title": "3-in-1 Bundle",
            "hook_lines": [
                "Goals change — your portfolio should too",
                "3 strategies for every financial goal",
                "Start with one, switch whenever you're ready",
            ],
        },
    },
}

def render_slide(lang):
    c = CONTENT[lang]["slide"]
    is_thai = lang == "th"
    out_path = os.path.join(SLIDES_DIR, f"slide1_bundle_{lang}.png")

    img = Image.new("RGB", (W, H), BG)
    apply_bg_left_heavy(img, load_bg())
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 4, H], fill=GOLD)
    draw_brand_badge(img, draw)
    draw_label_badge(draw, c["label"], 44, 116)

    if is_thai:
        draw.text((44, 162), c["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
        draw.text((40, 198), c["title"], font=fnt(F_KRUNGTHEP, 86), fill=WHITE)
    else:
        draw_tracked(draw, 44, 163, c["sub"], fnt(F_AVENIR_HEAVY, 18), GOLD, tracking=4)
        draw.text((40, 198), c["title"], font=fnt(F_AVENIR_HEAVY, 86), fill=WHITE)

    y = 358
    for name, desc in c["products"]:
        draw_product_row(draw, 44, y, name, desc, is_thai)
        y += 44

    draw.rectangle([44, y + 4, 44 + 400, y + 6], fill=(80, 70, 55))
    y += 18
    f_del = fnt(F_KRUNGTHEP, 20) if is_thai else fnt(F_AVENIR_HEAVY, 18)
    for item in c["deliverables"]:
        if is_thai:
            draw.text((56, y), f"• {item}", font=f_del, fill=DIM)
        else:
            draw_tracked(draw, 56, y, f"• {item}", f_del, DIM, tracking=1)
        y += 34

    draw_accent_line(draw, H - 100)
    draw_accent_line(draw, H - 106, length=180)
    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H - 76, "THREE STRATEGIES. ONE PACK. YOUR GOALS.", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H - 50, "INTELLIGENT INVESTING AT EVERY STAGE OF LIFE", f2, OFFWHITE, tracking=2)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")

def render_cover(lang):
    c = CONTENT[lang]["cover"]
    is_thai = lang == "th"
    out_path = os.path.join(COVERS_DIR, f"cover_bundle_{lang}.png")

    img = Image.new("RGB", (W, H), BG)
    apply_bg_left_heavy(img, load_bg())
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 4, H], fill=GOLD)
    draw_brand_badge(img, draw)
    draw_label_badge(draw, c["label"], 44, 116)

    if is_thai:
        draw.text((44, 162), c["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
        draw.text((40, 198), c["title"], font=fnt(F_KRUNGTHEP, 86), fill=WHITE)
    else:
        draw_tracked(draw, 44, 163, c["sub"], fnt(F_AVENIR_HEAVY, 18), GOLD, tracking=4)
        draw.text((40, 198), c["title"], font=fnt(F_AVENIR_HEAVY, 86), fill=WHITE)

    hook_y = 370
    for i, line in enumerate(c["hook_lines"]):
        color = GOLD if i == 0 else WHITE
        if is_thai:
            size = 30 if i == 0 else 26
            draw.text((44, hook_y), line, font=fnt(F_KRUNGTHEP, size), fill=color)
            hook_y += 52 if i == 0 else 44
        else:
            size = 26 if i == 0 else 22
            draw_tracked(draw, 44, hook_y, line, fnt(F_AVENIR_HEAVY, size), color, tracking=2)
            hook_y += 48 if i == 0 else 40

    draw_accent_line(draw, H - 100)
    draw_accent_line(draw, H - 106, length=180)
    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H - 76, "THREE STRATEGIES. ONE PACK. YOUR GOALS.", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H - 50, "INTELLIGENT INVESTING AT EVERY STAGE OF LIFE", f2, OFFWHITE, tracking=2)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")

if __name__ == "__main__":
    for lang in ("th", "en"):
        render_slide(lang)
        render_cover(lang)
    print("Done.")
