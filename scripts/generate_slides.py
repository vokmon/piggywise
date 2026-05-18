#!/usr/bin/env python3
"""
Generate product listing slides for PiggyWise — 7 slide types.

Slide 1 (features): 4 products × 2 languages = 8 images
  Background: images/bg/<product_key>.png (same as covers)
  Output:     images/slides/<product_key>/slide1_features_<lang>.png

Slides 2–7 (shared): 6 types × 2 languages = 12 images
  Background: images/bg/slides/<slide_key>.png
  Output:     images/slides/shared/slide<n>_<slide_key>_<lang>.png

Total: 20 images
"""

import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

# ── Brand ──────────────────────────────────────────────────────────────────
BG       = (13,  13,  13)
GOLD     = (212, 160, 23)
GOLD_MID = (160, 120, 18)
GOLD_DIM = (90,  68,  10)
WHITE    = (255, 255, 255)
OFFWHITE = (232, 224, 208)
SURFACE  = (26,  26,  26)

W, H = 1280, 720

# ── Fonts ──────────────────────────────────────────────────────────────────
F_FUTURA       = ("/System/Library/Fonts/Supplemental/Futura.ttc",   2)
F_AVENIR_HEAVY = ("/System/Library/Fonts/Avenir Next.ttc",           8)
F_AVENIR_MED   = ("/System/Library/Fonts/Avenir Next.ttc",           5)
F_AVENIR_DEMI  = ("/System/Library/Fonts/Avenir Next.ttc",           2)
F_KRUNGTHEP    = ("/System/Library/Fonts/Supplemental/Krungthep.ttf",0)
F_SILOM        = ("/System/Library/Fonts/Supplemental/Silom.ttf",    0)

def fnt(spec, size):
    path, index = spec
    return ImageFont.truetype(path, size, index=index)

# ── Assets ─────────────────────────────────────────────────────────────────
BASE_DIR  = "/Users/arnon/vokmon/study/piggywise"
ICON_PATH = os.path.join(BASE_DIR, "logo/piggywise-icon.png")
BG_DIR    = os.path.join(BASE_DIR, "images/bg")
SLIDES_BG = os.path.join(BASE_DIR, "images/bg/slides")
OUT_BASE  = os.path.join(BASE_DIR, "images/slides")

icon_src = Image.open(ICON_PATH).convert("RGBA")

def get_icon(size):
    return icon_src.resize((size, size), Image.LANCZOS)

# ── Text helpers ────────────────────────────────────────────────────────────
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

def text_width(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0]

def text_height(font_obj, size=None):
    # approximate line height
    return int((size or 20) * 1.4)

# ── Background loader + overlay ─────────────────────────────────────────────
def load_bg(path):
    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
        return img.resize((W, H), Image.LANCZOS)
    return None

def apply_bg_left_heavy(base_img, ai_bg):
    """Heavy dark on left (text), light on right — same as covers."""
    base_img.paste(ai_bg, (0, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(W):
        text_fade = max(0.0, 1.0 - (x / 680) ** 1.8)
        alpha = int(25 + 175 * text_fade)
        d.line([(x, 0), (x, H)], fill=(13, 13, 13, alpha))
    base_img.paste(overlay, mask=overlay.split()[3])

def apply_bg_full_overlay(base_img, ai_bg, alpha_base=160):
    """Uniform dark overlay — for shared slides where text is centered."""
    base_img.paste(ai_bg, (0, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, alpha_base))
    base_img.paste(overlay, mask=overlay.split()[3])

def procedural_bg(img):
    draw = ImageDraw.Draw(img)
    for x in range(820):
        t = (x / 820) ** 1.8
        c = tuple(int(SURFACE[i] + (BG[i] - SURFACE[i]) * t) for i in range(3))
        draw.line([(x, 0), (x, H)], fill=c)

# ── Chrome elements ─────────────────────────────────────────────────────────
def draw_brand_badge(img, draw):
    icon = get_icon(52)
    img.paste(icon, (44, 30), icon)
    f = fnt(F_AVENIR_HEAVY, 20)
    draw_tracked(draw, 108, 42, "PIGGYWISE", f, GOLD, tracking=3)

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

# ── Slide 1: Features ────────────────────────────────────────────────────────
#
# Layout (left-heavy, same as covers):
#   Brand badge top-left
#   Product label badge
#   Sub-label (template/service)
#   Title (large)
#   Feature bullets (4 rows with gold dots)
#   Accent line + bottom tagline

def draw_feature_bullet(draw, x, y, text, is_thai=False):
    dot_r = 5
    dot_cx = x + dot_r
    dot_cy = y + 14
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=GOLD)
    tx = x + dot_r * 2 + 14
    if is_thai:
        draw.text((tx, y), text, font=fnt(F_KRUNGTHEP, 24), fill=WHITE)
    else:
        draw_tracked(draw, tx, y + 1, text, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
with open(os.path.join(_DATA_DIR, "slides.json"), encoding="utf-8") as _f:
    _slides = json.load(_f)

SLIDE1_PRODUCTS = _slides["slide1"]


def render_slide1(product, lang):
    data = product[lang]
    is_thai = lang == "th"
    is_premium = product["premium"]

    img = Image.new("RGB", (W, H), BG)

    ai_bg = load_bg(os.path.join(BG_DIR, product["key"] + ".png"))
    if ai_bg:
        apply_bg_left_heavy(img, ai_bg)
    else:
        procedural_bg(img)

    draw = ImageDraw.Draw(img)

    if is_premium:
        draw.rectangle([0, 0, 4, H], fill=GOLD)

    draw_brand_badge(img, draw)
    draw_label_badge(draw, data["label"], 44, 116)

    # Sub-label
    if is_thai:
        draw.text((44, 162), data["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
    else:
        draw_tracked(draw, 44, 163, data["sub"], fnt(F_AVENIR_HEAVY, 24), GOLD, tracking=4)

    # Title
    if is_thai:
        draw.text((40, 198), data["title"], font=fnt(F_KRUNGTHEP, 86), fill=WHITE)
    else:
        draw.text((40, 194), data["title"], font=fnt(F_AVENIR_HEAVY, 80), fill=WHITE)

    # Feature bullets
    bullet_y = 360 if not is_thai else 368
    bullet_gap = 48
    for feat in data["features"]:
        draw_feature_bullet(draw, 44, bullet_y, feat, is_thai)
        bullet_y += bullet_gap

    draw_accent_line(draw, H - 100)
    if is_premium:
        draw_accent_line(draw, H - 106, length=180)

    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, product["key"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"slide1_features_{lang}.png")
    img.save(out_path, "PNG")
    src = "AI bg" if ai_bg else "procedural"
    print(f"  [{src}] {out_path}")


# ── Shared slides 2–7 ────────────────────────────────────────────────────────
#
# Layout: centered title, body text, brand badge top-left
# Each slide has a specific structure.

def centered_x(draw, text, font_obj, tracking=0):
    if tracking:
        w = tracked_width(draw, text, font_obj, tracking)
    else:
        w = text_width(draw, text, font_obj)
    return (W - w) // 2

def draw_section_header(draw, img, title_en, title_th, is_thai, y=80):
    """Large centered slide title."""
    if is_thai:
        f = fnt(F_KRUNGTHEP, 62)
        tw = text_width(draw, title_th, f)
        draw.text(((W - tw) // 2, y), title_th, font=f, fill=WHITE)
    else:
        f = fnt(F_AVENIR_HEAVY, 58)
        tw = tracked_width(draw, title_en, f, tracking=2)
        draw_tracked(draw, (W - tw) // 2, y, title_en, f, WHITE, tracking=2)
    draw_accent_line(draw, y + 80, x=(W - 200) // 2, length=200)


# ── Slide 2: How It Works ────────────────────────────────────────────────────
SLIDE2 = _slides["slide2"]

def render_slide2(lang):
    data = SLIDE2[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "how_it_works.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=160)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 90
    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 58), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    item_y = title_y + 116
    row_h = 152
    circle_r = 22

    for i, (num, step_title, body) in enumerate(data["steps"]):
        iy = item_y + i * row_h
        draw.ellipse([lx, iy + 4, lx + circle_r * 2, iy + 4 + circle_r * 2], fill=GOLD)
        f_num = fnt(F_AVENIR_HEAVY, 16)
        nb = draw.textbbox((0, 0), num, font=f_num)
        nw, nh = nb[2] - nb[0], nb[3] - nb[1]
        draw.text((lx + circle_r - nw // 2, iy + 4 + circle_r - nh // 2 - 1), num, font=f_num, fill=BG)
        tx = lx + circle_r * 2 + 18
        if is_thai:
            draw.text((tx, iy), step_title, font=fnt(F_KRUNGTHEP, 27), fill=WHITE)
            draw.text((tx, iy + 44), body, font=fnt(F_KRUNGTHEP, 24), fill=OFFWHITE)
        else:
            draw_tracked(draw, tx, iy + 2, step_title, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)
            draw_tracked(draw, tx, iy + 44, body, fnt(F_AVENIR_HEAVY, 24), OFFWHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"slide2_how_it_works_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")


# ── Slide 3: Fits Your Life ──────────────────────────────────────────────────
SLIDE3 = _slides["slide3"]

def render_slide3(lang):
    data = SLIDE3[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "fits_your_life.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=160)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 90
    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 58), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    item_y = title_y + 116
    row_h = 152
    circle_r = 18

    for i, (title, body) in enumerate(data["points"]):
        iy = item_y + i * row_h
        draw.ellipse([lx, iy + 8, lx + circle_r * 2, iy + 8 + circle_r * 2], fill=GOLD)
        tx = lx + circle_r * 2 + 18
        if is_thai:
            draw.text((tx, iy), title, font=fnt(F_KRUNGTHEP, 27), fill=WHITE)
            draw.text((tx, iy + 44), body, font=fnt(F_KRUNGTHEP, 24), fill=OFFWHITE)
        else:
            draw_tracked(draw, tx, iy + 2, title, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)
            draw_tracked(draw, tx, iy + 44, body, fnt(F_AVENIR_HEAVY, 24), OFFWHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    out_path = os.path.join(out_dir, f"slide3_fits_your_life_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")

# ── Slide 4: AI Platform ─────────────────────────────────────────────────────
SLIDE4 = _slides["slide4"]

def render_slide4(lang):
    data = SLIDE4[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "ai_platform.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=170)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 104

    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 60), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    intro_y = title_y + 96
    if is_thai:
        draw.text((lx, intro_y), data["intro"], font=fnt(F_KRUNGTHEP, 24), fill=WHITE)
    else:
        draw_tracked(draw, lx, intro_y, data["intro"], fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)

    list_start = intro_y + 72
    col1_x = lx
    col2_x = lx + 560
    row_h = 70
    items = data["items"]
    half = (len(items) + 1) // 2

    for i, item in enumerate(items):
        ix = col1_x if i < half else col2_x
        iy = list_start + (i % half) * row_h
        draw.ellipse([ix, iy + 10, ix + 13, iy + 23], fill=GOLD)
        if is_thai:
            draw.text((ix + 24, iy), item, font=fnt(F_KRUNGTHEP, 27), fill=WHITE)
        else:
            draw_tracked(draw, ix + 24, iy + 2, item, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    out_path = os.path.join(out_dir, f"slide4_ai_platform_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")


# ── Slide 5: Data Security ────────────────────────────────────────────────────
SLIDE5 = _slides["slide5"]

def render_slide5(lang):
    data = SLIDE5[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "data_security.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=160)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 90
    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 58), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    # 3 items stacked vertically — generous spacing, no subtitle clutter
    item_y = title_y + 116
    row_h = 152
    circle_r = 18

    for i, (title, body) in enumerate(data["points"]):
        iy = item_y + i * row_h
        draw.ellipse([lx, iy + 8, lx + circle_r * 2, iy + 8 + circle_r * 2], fill=GOLD)
        tx = lx + circle_r * 2 + 18
        if is_thai:
            draw.text((tx, iy), title, font=fnt(F_KRUNGTHEP, 27), fill=WHITE)
            draw.text((tx, iy + 44), body, font=fnt(F_KRUNGTHEP, 24), fill=OFFWHITE)
        else:
            draw_tracked(draw, tx, iy + 2, title, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)
            draw_tracked(draw, tx, iy + 44, body, fnt(F_AVENIR_HEAVY, 24), OFFWHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    out_path = os.path.join(out_dir, f"slide5_data_security_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")


# ── Slide 6: What You Receive ─────────────────────────────────────────────────
SLIDE6 = _slides["slide6"]

def render_slide6(lang):
    data = SLIDE6[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "what_you_receive.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=160)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 90
    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 58), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    # 4 items — tighter row height to fit
    item_y = title_y + 116
    row_h = 110
    circle_r = 22
    nums = ["01", "02", "03", "04"]

    for i, (title, body) in enumerate(data["items"]):
        iy = item_y + i * row_h
        draw.ellipse([lx, iy + 4, lx + circle_r * 2, iy + 4 + circle_r * 2], fill=GOLD)
        f_num = fnt(F_AVENIR_HEAVY, 16)
        nb = draw.textbbox((0, 0), nums[i], font=f_num)
        nw, nh = nb[2] - nb[0], nb[3] - nb[1]
        draw.text((lx + circle_r - nw // 2, iy + 4 + circle_r - nh // 2 - 1), nums[i], font=f_num, fill=BG)
        tx = lx + circle_r * 2 + 18
        if is_thai:
            draw.text((tx, iy), title, font=fnt(F_KRUNGTHEP, 27), fill=WHITE)
            draw.text((tx, iy + 42), body, font=fnt(F_KRUNGTHEP, 24), fill=OFFWHITE)
        else:
            draw_tracked(draw, tx, iy + 2, title, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)
            draw_tracked(draw, tx, iy + 42, body, fnt(F_AVENIR_HEAVY, 24), OFFWHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    out_path = os.path.join(out_dir, f"slide6_what_you_receive_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")


# ── Slide 7: Who It's For ─────────────────────────────────────────────────────
SLIDE7 = _slides["slide7"]

def render_slide7(lang):
    data = SLIDE7[lang]
    is_thai = lang == "th"

    img = Image.new("RGB", (W, H), BG)
    ai_bg = load_bg(os.path.join(SLIDES_BG, "who_its_for.png"))
    if ai_bg:
        apply_bg_full_overlay(img, ai_bg, alpha_base=160)
    draw = ImageDraw.Draw(img)
    draw_brand_badge(img, draw)

    lx = 72
    title_y = 90
    if is_thai:
        draw.text((lx, title_y), data["title"], font=fnt(F_KRUNGTHEP, 58), fill=WHITE)
    else:
        draw_tracked(draw, lx, title_y, data["title"], fnt(F_AVENIR_HEAVY, 52), WHITE, tracking=3)

    draw_accent_line(draw, title_y + 76, x=lx, length=240)

    item_y = title_y + 116
    row_h = 152
    circle_r = 18

    for i, (label, desc) in enumerate(data["personas"]):
        iy = item_y + i * row_h
        draw.ellipse([lx, iy + 8, lx + circle_r * 2, iy + 8 + circle_r * 2], fill=GOLD)
        tx = lx + circle_r * 2 + 18
        if is_thai:
            draw.text((tx, iy), label, font=fnt(F_KRUNGTHEP, 27), fill=GOLD)
            draw.text((tx, iy + 44), desc, font=fnt(F_KRUNGTHEP, 24), fill=WHITE)
        else:
            draw_tracked(draw, tx, iy + 2, label, fnt(F_AVENIR_HEAVY, 24), GOLD, tracking=1)
            draw_tracked(draw, tx, iy + 44, desc, fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)

    draw_accent_line(draw, H - 100)
    draw_bottom_tagline(draw)

    out_dir = os.path.join(OUT_BASE, "shared")
    out_path = os.path.join(out_dir, f"slide7_who_its_for_{lang}.png")
    img.save(out_path, "PNG")
    print(f"  [shared] {out_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating PiggyWise product listing slides...")

    print("\n── Slide 1: Features (4 products × 2 langs = 8 images) ──")
    for product in SLIDE1_PRODUCTS:
        for lang in ("en", "th"):
            render_slide1(product, lang)

    print("\n── Shared Slides 2–7 (6 × 2 langs = 12 images) ──")
    for lang in ("en", "th"):
        render_slide2(lang)
        render_slide3(lang)
        render_slide4(lang)
        render_slide5(lang)
        render_slide6(lang)
        render_slide7(lang)

    print(f"\nDone — 20 slides in {OUT_BASE}")
