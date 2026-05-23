# etsy-listing

Generate SEO-optimized Etsy listing content that also maps accurately to Etsy API fields.

## Input
- Product name and description
- Target buyer
- Key features and benefits
- Price

## Output
Complete listing JSON with all fields below — ready to post manually or via the Etsy API.

---

## SEO Content

### Title Rules
- Lead with the most searched keyword — not the brand name
- Comma-separate keyword clusters; each targets a different search query
- Max 140 characters
- No emojis, no filler words ("ultimate", "amazing")
- Allowed characters: letters, numbers, punctuation, ™, ©, ® — %, :, &, + can only appear once each
- Example: `1970s Brain Training Activity Pack, Large Print Memory Games for Seniors, Printable Nostalgia Puzzle Book, Caregiver Gift`

### Body Rules
- First sentence must be keyword-rich — Google uses it as the meta description for the listing page
- Follow with buyer pain points, then features bullet list, then delivery info
- Use short paragraphs and bullet points — not walls of text
- End with a reassurance statement: "Instant download. No subscription. Print as many times as you like."

### Tag Rules
- Exactly 13 tags
- Max 20 characters each
- Allowed: letters, numbers, whitespace, `-`, `'`, ™, ©, ® — no other special characters
- Match real search terms buyers type
- Cover: product type, format, audience, use case, era/theme
- No duplicates with title keywords (Etsy combines title + tags for search ranking)

### Styles (Boosts Filtered Search)
- Up to 2 style strings, max 45 characters each, letters/numbers/whitespace only
- Choose styles that match the product feel — e.g. `"Vintage"`, `"Nostalgic"`

---

## Etsy API Fields (Required for Accuracy)

These fields must be included in the listing JSON. They affect category placement, search filters, and listing validity.

| Field | Value | Notes |
|-------|-------|-------|
| `type` | `"download"` | Digital product |
| `who_made` | `"i_did"` | Original digital product |
| `when_made` | `"made_to_order"` | Created digitally on demand |
| `is_supply` | `false` | Finished product, not a craft supply |
| `quantity` | `999` | Unlimited digital stock |
| `materials` | `["PDF"]` | Appears in material-filtered searches |
| `should_auto_renew` | `true` | Renews every 4 months automatically |
| `taxonomy_id` | integer | **Look up once** using `getSellerTaxonomyNodes` via Etsy MCP — hardcode after found |

---

## Example JSON Output

```json
{
  "title": "1970s Brain Training Activity Pack, Large Print Memory Games for Seniors, Printable Nostalgia Puzzle Book, Caregiver Gift",
  "description": "...",
  "price": 14.99,
  "quantity": 999,
  "type": "download",
  "who_made": "i_did",
  "when_made": "made_to_order",
  "is_supply": false,
  "taxonomy_id": null,
  "tags": ["large print", "memory games", "brain activity", "1970s gift", "printable puzzle", "seniors gift", "activity book", "nostalgia game", "large print puzzle", "caregiver gift", "printable", "word search", "crossword"],
  "styles": ["Vintage", "Nostalgic"],
  "materials": ["PDF"],
  "should_auto_renew": true,
  "language": "en"
}
```
