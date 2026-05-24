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
- No years (e.g. "2026") — they date the listing and require annual edits; use evergreen descriptors instead
- Allowed characters: letters, numbers, punctuation, ™, ©, ® — %, :, &, + can only appear once each
- Example: `AI Portfolio Tracker Google Sheets Template, Stock and Crypto DCA System, Investment Dashboard for Beginners`

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
  "title": "AI Portfolio Tracker Google Sheets Template, Stock and Crypto DCA System, Investment Dashboard for Beginners",
  "description": "...",
  "price": 14.99,
  "quantity": 999,
  "type": "download",
  "who_made": "i_did",
  "when_made": "made_to_order",
  "is_supply": false,
  "taxonomy_id": null,
  "tags": ["google sheets", "portfolio tracker", "DCA template", "stock tracker", "crypto tracker", "investment tool", "AI prompts", "finance template", "spreadsheet", "passive income", "beginner investing", "budget tool", "digital download"],
  "styles": ["Modern", "Minimalist"],
  "materials": ["Google Sheets"],
  "should_auto_renew": true,
  "language": "en"
}
```
