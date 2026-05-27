# design-swipe

Router. Delegates to the correct type-specific skill based on `product_type`.

## Input

- `product_type` — string identifying the product type (supported types listed in the routing table below)
- `keyword` — the validated keyword (used as search seed)
- `style_signals` — any preliminary style observations from reverse-engineer (optional, used to focus search)

## Routing

| product_type    | skill                                        |
|-----------------|----------------------------------------------|
| `google-sheets` | `pipeline/03-build/skills/study/design-swipe/google-sheets.md` |
| `notion`        | `pipeline/03-build/skills/study/design-swipe/notion.md`        |
| `canva`         | `pipeline/03-build/skills/study/design-swipe/canva.md`         |

Pass all input fields through to the type-specific skill unchanged.

If `product_type` is not in the routing table: stop and ask the human before proceeding.

## Output

Returns the type-specific skill output unchanged. See the routed skill for the output schema.
