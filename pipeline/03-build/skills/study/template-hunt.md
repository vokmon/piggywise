# template-hunt

Router. Delegates to the correct type-specific skill based on `product_type`.

## Input

- `product_type` — string identifying the product type (supported types listed in the routing table below)
- `feature_spec` — always `null` at call time (template-hunt runs in Step 4, before synthesis in Step 6); search is done by keyword instead
- `max_templates` — maximum number of candidates to evaluate (passed from build-agent)
- `keyword` — the validated keyword from Stage 02

## Routing

| product_type    | skill                                                                 |
|-----------------|-----------------------------------------------------------------------|
| `google-sheets` | `pipeline/03-build/skills/study/template-hunt/google-sheets.md` |
| `notion`        | `pipeline/03-build/skills/study/template-hunt/notion.md`        |
| `canva`         | `pipeline/03-build/skills/study/template-hunt/canva.md`         |

Pass all input fields through to the type-specific skill unchanged.

If `product_type` is not in the routing table: stop and ask the human before proceeding.

## Output

Returns the type-specific skill output unchanged. See the routed skill for the output schema.
