# launch-agent

Publishes a product to Etsy: uploads all marketing assets, creates the listing, and saves the listing URL to `product.json`. Leaves the listing in **draft** state — human publishes from the Etsy seller dashboard after review.

---

## How to invoke

> `/launch "{slug}"`

---

## Parameters

- `slug` — product slug matching the folder name under `output/` and `products/`

---

## Inputs

| Source | Used for |
|---|---|
| `output/{slug}/05-marketing/notion-freelancer-crm-template-listing.json` | listing copy: title, description, tags, price |
| `output/{slug}/05-marketing/canva/` | product images (PNG files) |
| `output/{slug}/05-marketing/canva/etsy-demo-video-frame.mp4` | demo video |
| `products/{slug}/delivery/` | buyer download file |
| `product.json` | slug, product_type, pipeline state |

**Image rank order:** images are uploaded in filename sort order. Ensure cover image sorts first (e.g. `cover.png` or `01-cover.png`).

---

## Steps

### Step 1 — Load inputs

Read `product.json`. Confirm:
- `pipeline_status.stage` is `05-marketing` and `status` is `complete`
- If not complete: stop and tell the human to finish Stage 05 first

Read `output/{slug}/05-marketing/{slug}-listing.json`. Extract title, description, tags, price, who_made, when_made, type, materials, styles.

Check that the following exist and are non-empty:
- At least one PNG in `output/{slug}/05-marketing/canva/`
- `products/{slug}/delivery/` contains the buyer download file

If anything is missing: list what's missing and stop.

### Step 2 — Refresh Etsy token

Follow `skills/etsy-connect.md` → **Step 1** (token refresh).

Run the test connection ping to confirm credentials are valid before proceeding.

### Step 3 — Create draft listing

Run `skills/listing-creator.md`:

| Input | Value |
|---|---|
| `slug` | from agent param |
| `listing_json_path` | `output/{slug}/05-marketing/{slug}-listing.json` |
| `images_dir` | `output/{slug}/05-marketing/canva/` |
| `video_path` | `output/{slug}/05-marketing/canva/etsy-demo-video-frame.mp4` (skip if not found) |
| `delivery_file_path` | file found in `products/{slug}/delivery/` |
| `taxonomy_id` | `12476` for Notion/productivity templates; verify for other types |

Record the `listing_id` and `url` returned.

### Step 4 — Save to product.json

Update `product.json`:

```json
{
  "pipeline_status": {
    "stage": "06-launch",
    "status": "complete"
  },
  "etsy": {
    "listing_id": 4513026646,
    "listing_url": "https://www.etsy.com/listing/4513026646/...",
    "state": "draft",
    "launched_at": null
  }
}
```

### Step 5 — Report to human

```
Draft listing created for: {slug}

Listing ID:  {listing_id}
Etsy URL:    {url}
State:       draft

Images uploaded:  {n}
Video uploaded:   yes / no
Delivery file:    {filename}

Open the Etsy seller dashboard to review the draft, then publish when ready.
Next: /iterate "{slug}" to begin monitoring performance.
```

---

## Skills used

- `skills/etsy-connect.md` — token refresh + auth patterns
- `skills/listing-creator.md` — upload assets + create listing

---

## Notes

- This agent never publishes — always leaves the listing in `draft`. Human reviews and publishes from Etsy dashboard.
- If the access token has expired and the refresh token is also expired (90 days), re-run the full OAuth flow documented in `skills/etsy-connect.md`.
- The Etsy MCP (`mcp__etsy__*`) is a documentation reference only — all actual API calls use curl/Python via the credentials in `.env`.
