# canva-design

Interact with Canva via MCP to create and edit designs.

## Available MCP Tools
- `mcp__canva__search-designs` — find existing designs
- `mcp__canva__generate-design` — create a new design
- `mcp__canva__create-design-from-brand-template` — use brand template
- `mcp__canva__get-design-content` — read design content
- `mcp__canva__perform-editing-operations` — edit design elements
- `mcp__canva__export-design` — export as PNG, JPG, or PDF
- `mcp__canva__upload-asset-from-url` — upload image asset

## General Steps
1. Search for an existing design to reuse or create a new one
2. Set canvas dimensions to match the target format
3. Apply content, typography, and colors as specified by the calling skill or agent
4. Export in the required format and resolution

## Export Formats
- Print PDF → `mcp__canva__export-design` with format `pdf`
- Etsy cover/preview → JPG, minimum 2000px on the shortest side
- Web image → PNG or JPG at screen resolution
