# reverse-engineer

Router. Delegates to the correct type-specific skill based on `product_type`.

## Input

- `product_type` — string identifying the product type (supported types listed in the routing table below)
- `competitor_urls` — array of Etsy listing URLs (up to `max_competitors`)
- `max_competitors` — maximum number of competitors to study (passed from poc-agent)
- `keyword` — the validated keyword from Stage 02

## Routing

| product_type    | skill                                            |
|-----------------|--------------------------------------------------|
| `google-sheets` | `skills/study/reverse-engineer/google-sheets.md` |
| `notion`        | `skills/study/reverse-engineer/notion.md`        |
| `canva`         | `skills/study/reverse-engineer/canva.md`         |

Pass all input fields through to the type-specific skill unchanged.

If `product_type` is not in the routing table: stop and ask the human before proceeding.

## Output

Returns the type-specific skill output unchanged. See the routed skill for the output schema.
