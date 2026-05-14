#!/usr/bin/env python3
"""
Generate product cover images for PiggyWise — 4 products × 2 languages = 8 images.

Background images:
  Drop AI-generated backgrounds into images/cover/bg/ named by product key:
    retire_smooth.png, hybrid_wealth.png, aggressive_go.png, premium_setup.png
  If a background exists it is used (with dark overlay); otherwise falls back
  to the procedural gold motif.
"""

import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

# ── Brand ──────────────────────────────────────────────────────────────────
BG        = (13,  13,  13)
GOLD      = (212, 160, 23)
GOLD_MID  = (160, 120, 18)
GOLD_DIM  = (90,  68,  10)
WHITE     = (255, 255, 255)
OFFWHITE  = (232, 224, 208)
SURFACE   = (26,  26,  26)

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
ICON_PATH = "/Users/arnon/vokmon/study/piggywise/images/logo/piggywise-icon.png"
BG_DIR    = "/Users/arnon/vokmon/study/piggywise/images/bg"
OUT_DIR   = "/Users/arnon/vokmon/study/piggywise/images/cover"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BG_DIR, exist_ok=True)

icon_src = Image.open(ICON_PATH).convert("RGBA")

def get_icon(size):
    return icon_src.resize((size, size), Image.LANCZOS)

# ── Letter-tracking (EN only — never split Thai combining chars) ───────────
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

# ── AI background loader ────────────────────────────────────────────────────
def load_ai_bg(product_key):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(BG_DIR, product_key + ext)
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            return img.resize((W, H), Image.LANCZOS)
    return None

def apply_bg(base_img, ai_bg):
    base_img.paste(ai_bg, (0, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Heavy dark only on the left (text zone), barely anything on the right (pig zone)
    # x=0: alpha ~200  |  x=680: alpha ~25  |  x=1280: alpha ~25
    for x in range(W):
        text_fade = max(0.0, 1.0 - (x / 680) ** 1.8)
        alpha = int(25 + 175 * text_fade)
        d.line([(x, 0), (x, H)], fill=(13, 13, 13, alpha))
    base_img.paste(overlay, mask=overlay.split()[3])

# ── Procedural fallback motifs ──────────────────────────────────────────────
def motif_retire(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, cy = 1060, H // 2 + 40
    for r, lw, color in [(320,1,(*GOLD_DIM,80)),(240,2,(*GOLD_MID,120)),
                          (160,3,(*GOLD,200)),(80,2,(*GOLD_MID,140))]:
        pts = [(cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
               for a in range(100, 280, 2)]
        if len(pts) > 1:
            d.line(pts, fill=color, width=lw)
    img.paste(overlay, mask=overlay.split()[3])

def motif_hybrid(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    left = 760
    for offset, color in [(0,(*GOLD_DIM,100)),(30,(*GOLD_MID,160)),(60,(*GOLD_DIM,80))]:
        d.line([(left+offset,0),(W,H-(W-left-offset))], fill=color, width=3)
        d.line([(W-offset,0),(left,H-(W-left-offset))], fill=color, width=3)
    d.line([(left,0),(W,H-(W-left))], fill=(*GOLD,220), width=2)
    d.line([(W,0),(left,H-(W-left))], fill=(*GOLD,220), width=2)
    img.paste(overlay, mask=overlay.split()[3])

def motif_aggressive(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, base_y = 1060, 560
    for scale, alpha in [(1.5,60),(1.2,100)]:
        sw,sh = int(40*scale),int(220*scale)
        hw,hh = int(110*scale),int(120*scale)
        d.rectangle([cx-sw//2,base_y-sh,cx+sw//2,base_y], fill=(*GOLD_DIM,alpha))
        d.polygon([(cx,base_y-sh-hh),(cx+hw,base_y-sh),(cx-hw,base_y-sh)],
                  fill=(*GOLD_DIM,alpha))
    d.rectangle([cx-20,base_y-220,cx+20,base_y], fill=(*GOLD_MID,200))
    d.polygon([(cx,base_y-340),(cx+110,base_y-220),(cx-110,base_y-220)],
              fill=(*GOLD,230))
    img.paste(overlay, mask=overlay.split()[3])

def motif_premium(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, cy = 1060, H // 2
    def rot_sq(half, angle, color):
        pts = []
        for dx,dy in [(-half,-half),(half,-half),(half,half),(-half,half)]:
            r = math.radians(angle)
            pts.append((cx+dx*math.cos(r)-dy*math.sin(r),
                        cy+dx*math.sin(r)+dy*math.cos(r)))
        d.polygon(pts, outline=color, width=3)
    for half,angle,col in [(180,45,(*GOLD_DIM,100)),(140,45,(*GOLD_MID,150)),
                            (100,45,(*GOLD,220)),(60,45,(*GOLD,255))]:
        rot_sq(half,angle,col)
    s=22
    d.polygon([(cx,cy-s),(cx+s,cy),(cx,cy+s),(cx-s,cy)], fill=(*GOLD,255))
    img.paste(overlay, mask=overlay.split()[3])

MOTIFS = {"retire":motif_retire,"hybrid":motif_hybrid,
          "aggressive":motif_aggressive,"premium":motif_premium}

# ── Chrome elements ─────────────────────────────────────────────────────────
def draw_brand_badge(img, draw):
    icon = get_icon(52)
    img.paste(icon, (44, 30), icon)
    f = fnt(F_AVENIR_HEAVY, 20)
    draw_tracked(draw, 108, 42, "PIGGYWISE", f, GOLD, tracking=3)

def draw_label_badge(draw, label, y, is_premium=False):
    f = fnt(F_AVENIR_HEAVY, 13)
    tw = tracked_width(draw, label, f, tracking=3)
    px, py = 16, 8
    h = 30
    if is_premium:
        # full gold bar — wider, taller
        draw.rectangle([44, y, 44+tw+px*2, y+h], fill=GOLD)
        draw_tracked(draw, 44+px, y+py-1, label, f, BG, tracking=3)
    else:
        draw.rectangle([44, y, 44+tw+px*2, y+h], fill=GOLD)
        draw_tracked(draw, 44+px, y+py-1, label, f, BG, tracking=3)

def draw_left_gold_bar(draw):
    """Thin vertical gold bar on far left — Premium only."""
    draw.rectangle([0, 0, 4, H], fill=GOLD)

def draw_accent_line(draw, y, length=300):
    draw.rectangle([44, y, 44+length, y+2], fill=GOLD)

# ── Bottom taglines ──────────────────────────────────────────────────────────
def draw_bottom_text(draw):
    f1 = fnt(F_AVENIR_HEAVY, 17)
    f2 = fnt(F_AVENIR_HEAVY, 15)
    draw_tracked(draw, 44, H-76, "INTELLIGENT INVESTING, SIMPLIFIED", f1, WHITE, tracking=2)
    draw_tracked(draw, 44, H-50, "YOUR PERSONAL AI FINANCE COACH", f2, OFFWHITE, tracking=2)

# ── Products ────────────────────────────────────────────────────────────────
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
with open(os.path.join(_DATA_DIR, "covers.json"), encoding="utf-8") as _f:
    PRODUCTS = json.load(_f)

# ── Render ───────────────────────────────────────────────────────────────────
def render_cover(product, lang):
    data = product[lang]
    is_thai = lang == "th"
    is_premium = product["premium"]

    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # background
    ai_bg = load_ai_bg(product["key"])
    if ai_bg:
        apply_bg(img, ai_bg)
    else:
        for x in range(820):
            t = (x/820)**1.8
            c = tuple(int(SURFACE[i]+(BG[i]-SURFACE[i])*t) for i in range(3))
            draw.line([(x,0),(x,H)], fill=c)
        MOTIFS[product["motif"]](img)
    draw = ImageDraw.Draw(img)

    # premium: left gold bar
    if is_premium:
        draw_left_gold_bar(draw)

    draw_brand_badge(img, draw)
    draw_label_badge(draw, data["label"], 116, is_premium)

    # sub-label
    if is_thai:
        draw.text((44, 162), data["sub"], font=fnt(F_KRUNGTHEP, 24), fill=GOLD)
    else:
        draw_tracked(draw, 44, 162, data["sub"], fnt(F_AVENIR_HEAVY, 24), GOLD, tracking=4)

    title_color = WHITE
    if is_thai:
        draw.text((40, 202), data["title"], font=fnt(F_KRUNGTHEP, 96), fill=title_color)
    else:
        draw.text((40, 198), data["title"], font=fnt(F_AVENIR_HEAVY, 90), fill=title_color)

    # tagline
    if is_thai:
        draw.text((44, 420), data["tagline"], font=fnt(F_KRUNGTHEP, 24), fill=WHITE)
    else:
        draw_tracked(draw, 44, 418, data["tagline"], fnt(F_AVENIR_HEAVY, 24), WHITE, tracking=1)

    # accent line(s)
    draw_accent_line(draw, H-100)
    if is_premium:
        draw_accent_line(draw, H-106, length=180)  # double line for premium

    draw_bottom_text(draw)

    out_path = os.path.join(OUT_DIR, f"cover_{product['key']}_{lang}.png")
    img.save(out_path, "PNG")
    src = "AI bg" if ai_bg else "procedural"
    print(f"  [{src}] {out_path}")

if __name__ == "__main__":
    print("Generating PiggyWise cover images...")
    for product in PRODUCTS:
        for lang in ("en", "th"):
            render_cover(product, lang)
    print(f"\nDone — 8 covers in {OUT_DIR}")
