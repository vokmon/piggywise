# etsy-cover-image

Specs and guidelines for creating Etsy listing cover images.
Use this for any product sold on Etsy — cover image only (not preview images).

---

## How Etsy Displays the Cover Image

| Context | Display |
|---------|---------|
| Search results / shop page | Cropped to **square (1:1)** from center |
| Product detail page | Full image shown at uploaded ratio, no crop |

Etsy provides a thumbnail adjustment tool after upload to fine-tune the square crop position.

---

## Recommended Format
- **Size:** 2000×1500px (4:3 landscape)
- **File type:** JPG
- **Why 4:3:** Looks great on the product detail page; provides enough width so the background fills naturally without empty space

---

## Safe Zone Rule
The center **1500×1500px** area is what appears in the square thumbnail on search results.

All key content must stay inside this zone:
- Product name / title text
- Main visual subject
- Any tagline or key selling point

Background color or texture must extend to all four edges so the full 4:3 image looks complete on the detail page.

---

## Design Checklist
- [ ] Image is 2000×1500px (4:3 landscape)
- [ ] All key text and visuals are within the center 1500×1500px safe zone
- [ ] Background fills the full width — no empty strips on left/right
- [ ] After upload: use Etsy's thumbnail tool to confirm the square crop looks good
- [ ] No important content within 100px of any edge

---

## Usage
The calling skill or agent provides:
- Visual style, colors, and subject matter (product-specific)
- Text to display (product name, tagline)

This skill provides the format constraints only.
Use `skills/generate-image.md` to generate the actual image.
