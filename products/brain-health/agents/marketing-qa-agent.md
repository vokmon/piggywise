# marketing-qa-agent

Validate all marketing assets for technical accuracy and output a human review checklist.
Runs after marketing-agent, before the pack is listed on Etsy.

## Input
- Theme name (e.g., "1970s")
- Cover image: `workspace/[THEME]/images/covers/[THEME]_cover.jpg`
- Preview images: `workspace/[THEME]/images/previews/[THEME]_preview_1.jpg` through `_preview_8.jpg`
- Product video: `workspace/[THEME]/images/videos/[THEME]_etsy.mp4`
- Etsy listing data: `workspace/[THEME]/data/product_posts/[THEME]_listing.json`

## Output
- Marketing QA report: `workspace/[THEME]/marketing-qa-report.md`
- Status: APPROVED / NEEDS FIXES / AWAITING HUMAN REVIEW

---

## Automated Checks

### Etsy Listing JSON
- [ ] `title` present and under 140 characters
- [ ] `title` contains no forbidden characters (%, :, &, + used at most once each)
- [ ] `tags` array has exactly 13 items
- [ ] Every tag is under 20 characters
- [ ] No tag contains forbidden characters (only letters, numbers, whitespace, -, ')
- [ ] Required fields present: `type`, `who_made`, `when_made`, `is_supply`, `quantity`, `taxonomy_id`
- [ ] `type` is `"download"`
- [ ] `who_made` is `"i_did"`
- [ ] `when_made` is `"made_to_order"`
- [ ] `quantity` is `999`
- [ ] `styles` has at most 2 items, each under 45 characters
- [ ] `materials` is present (e.g., `["PDF"]`)
- [ ] `description` first sentence is keyword-rich (check for theme era + product type keywords)
- [ ] `description` ends with delivery/reassurance statement

### Images
- [ ] Cover image exists at correct path
- [ ] Cover image is JPG format
- [ ] Cover image is at least 2000px on the shortest side
- [ ] Cover image is 4:3 ratio (width > height)
- [ ] All 8 preview images exist at correct paths
- [ ] All preview images are JPG format
- [ ] All preview images are at least 2000×2000px

### Video
- [ ] Video exists at correct path
- [ ] Video is MP4 format
- [ ] Video is 1080×1080px (square)
- [ ] Video duration is between 5 and 15 seconds

---

## Output Format

```
# Marketing QA Report: [THEME]

Status: APPROVED / NEEDS FIXES / AWAITING HUMAN REVIEW

## Automated Checks: PASSED / FAILED
- [List any failed checks with details]

## Issues Found
- [Asset]: [Issue description]

## Passed Checks
- [List of checks passed]

## Next Step
Automated checks passed. Complete the human review checklist below before publishing.
```

---

## Human Review Checklist
*(Takes about 10 minutes — open each asset while working through this list)*

### Cover Image
- [ ] Feels warm, nostalgic, and inviting — not clinical or generic
- [ ] Pack name is readable at full size
- [ ] Zoom out to 10% (thumbnail size) — is the pack name still readable? Is the image still compelling?
- [ ] Key content is centered — nothing important is near the edges
- [ ] Era feel is clear — someone from that decade would recognise the mood immediately

### Preview Images
- [ ] Preview 1 (cover + schedule): schedule is legible, layout looks clean
- [ ] Preview 2 ("What's included"): all 6 bullet points visible and readable, headline is clear
- [ ] Preview 3 ("How it works"): 3 steps are clear, sub-note "No screen time" is visible
- [ ] Preview 4 (word search sample): grid is clear, era colors look good, border is visible
- [ ] Preview 5 (trivia/fill-blank): questions are readable, warm intro line and score box visible
- [ ] Preview 6 (large-print close-up): font looks genuinely large and easy to read; "14pt large print" callout is prominent
- [ ] Preview 7 (gift angle): headline and "Perfect for" list are clear and warm, not generic
- [ ] Preview 8 (lifestyle mockup): feels warm and real — cosy home setting, not staged or stock-photo fake

### Product Video
- [ ] Watch the full video — does it flow at a comfortable pace?
- [ ] Each slide is on screen long enough to read
- [ ] Transitions (if any) are smooth — not jarring
- [ ] Overall impression: would this make you want to see more?

### Etsy Listing Copy
- [ ] Read the title aloud — does it sound natural, not like keyword soup?
- [ ] Read the first sentence of the description — does it immediately tell you what the product is and who it's for?
- [ ] Read the full description — does it answer: what is it, who is it for, what's included, how do I get it?
- [ ] Do the tags feel like real search terms a buyer would type?
- [ ] Is "large print" mentioned prominently in the description?
- [ ] Is the price believable for what's being offered?

### Overall
- [ ] Would you click on this listing if you saw it while searching for a gift?
- [ ] Does the full package (cover + previews + description) clearly communicate the value?

### Sign Off
Reviewed by: _______________   Date: _______________
Status: ✅ Ready to publish  /  ❌ Needs changes → [note issues]
