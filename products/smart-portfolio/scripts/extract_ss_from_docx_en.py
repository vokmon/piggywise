#!/usr/bin/env python3
"""
Extract screenshot panels from Images_en.docx, composite with banner, save to images/ss/en/.
Layout per output image: banner at top + panels in columns (natural sizes, no upscaling).
"""

import os, re, io, zipfile
from PIL import Image

DOCX    = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp", "Images_en.docx")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "ss", "en")
GAP     = 16   # px gap between columns
BG      = (255, 255, 255)

OUTPUT_NAMES = [
    "1_setup.png",
    "2_notification_setup.png",
    "3_update_port.png",
    "4_tax_consult.png",
    "5_health_check.png",
    "6_market.png",
    "7_news.png",
    "8_budget_consult.png",
]

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with zipfile.ZipFile(DOCX) as z:
        xml  = z.read("word/document.xml").decode("utf-8")
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8")

        rid_map = {rid: fname for rid, fname in
                   re.findall(r'Id="rId(\d+)"[^>]*Target="media/(image\d+\.png)"', rels)}

        banner = Image.open(io.BytesIO(z.read("word/media/image22.png"))).convert("RGBA")

        rows = re.findall(r'<w:tr[ >].*?</w:tr>', xml, re.DOTALL)
        pages = []
        for row in rows:
            rids = re.findall(r'r:embed="rId(\d+)"', row)
            group = []
            for rid in rids:
                fname = rid_map.get(rid)
                if fname:
                    img = Image.open(io.BytesIO(z.read(f"word/media/{fname}"))).convert("RGBA")
                    group.append(img)
            if group:
                pages.append(group)

    print(f"Banner: {banner.size}")
    print(f"Total pages: {len(pages)}")

    # Determine standard column width from widest panel across all pages
    col_w = max(p.size[0] for group in pages for p in group)

    for page_idx, group in enumerate(pages):
        panels = []
        for p in group:
            pw, ph = p.size
            # Scale down if wider than col_w; never upscale
            if pw > col_w:
                new_h = int(ph * col_w / pw)
                p = p.resize((col_w, new_h), Image.LANCZOS)
                pw, ph = p.size
            panels.append(p)

        row_h = max(p.size[1] for p in panels)
        total_w = col_w * len(panels) + GAP * (len(panels) - 1)

        # Scale banner to canvas width
        bw, bh = banner.size
        banner_scaled = banner.resize((total_w, int(bh * total_w / bw)), Image.LANCZOS)

        total_h = banner_scaled.size[1] + row_h
        canvas = Image.new("RGBA", (total_w, total_h), BG + (255,))

        canvas.paste(banner_scaled, (0, 0), banner_scaled)

        x = 0
        for p in panels:
            canvas.paste(p, (x, banner_scaled.size[1]), p)
            x += col_w + GAP

        out_name = OUTPUT_NAMES[page_idx] if page_idx < len(OUTPUT_NAMES) else f"{page_idx+1}.png"
        out_path = os.path.join(OUT_DIR, out_name)
        canvas.convert("RGB").save(out_path)
        print(f"  ✓ {out_name}: {canvas.size}")

    print("Done.")

if __name__ == "__main__":
    main()
