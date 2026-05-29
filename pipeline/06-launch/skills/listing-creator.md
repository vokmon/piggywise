# listing-creator

Creates a draft Etsy listing with all assets: images, video, and digital delivery file. Uses the Etsy REST API directly via Python/curl.

Requires `skills/etsy-connect.md` — run token refresh before calling this skill.

---

## Input

| Field | Source | Description |
|---|---|---|
| `slug` | agent | Product slug |
| `listing_json_path` | agent | Path to `{slug}-listing.json` |
| `images_dir` | agent | Local folder with PNG images (rank order = filename sort order) |
| `video_path` | agent | Path to demo `.mp4` (optional — skip if none) |
| `delivery_file_path` | agent | Path to the buyer download file (PDF, zip, etc.) |
| `taxonomy_id` | agent | Etsy taxonomy ID — see taxonomy note below |

**Taxonomy note:** For Notion/productivity templates, use `12476` (Planner Templates under Paper & Party Supplies > Stationery > Design & Templates). Verify via `GET /v3/application/seller-taxonomy/nodes` if the product type differs.

---

## Steps

### Step 1 — Create draft listing

```python
import urllib.request, urllib.parse, json, os

ACCESS_TOKEN = os.environ["ETSY_ACCESS_TOKEN"]
API_KEY = f"{os.environ['ETSY_KEYSTRING']}:{os.environ['ETSY_SECRETSTRING']}"
SHOP_ID = os.environ["ETSY_SHOP_ID"]

with open(listing_json_path) as f:
    listing = json.load(f)

fields = [
    ("quantity",        str(listing["quantity"])),
    ("title",           listing["title"]),
    ("description",     listing["description"]),
    ("price",           str(listing["price"])),
    ("who_made",        listing["who_made"]),
    ("when_made",       listing["when_made"]),
    ("taxonomy_id",     str(taxonomy_id)),
    ("type",            listing.get("type", "download")),
    ("is_supply",       str(listing.get("is_supply", False)).lower()),
    ("should_auto_renew", str(listing.get("should_auto_renew", True)).lower()),
    ("language",        listing.get("language", "en")),
]
for style in listing.get("styles", []):
    fields.append(("styles[]", style))
for material in listing.get("materials", []):
    fields.append(("materials[]", material))
for tag in listing.get("tags", []):
    fields.append(("tags[]", tag))

body = urllib.parse.urlencode(fields).encode()
req = urllib.request.Request(
    f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/listings",
    data=body,
    method="POST",
    headers={
        "x-api-key": API_KEY,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    listing_id = result["listing_id"]
    print(f"Draft created: listing_id={listing_id}")
```

Record `listing_id` — needed for all subsequent steps.

---

### Step 2 — Upload images

Images are uploaded as `multipart/form-data`. Sort files in the images directory alphabetically — the sort order determines rank (1 = cover/first image shown).

```bash
source .env

LISTING_ID=<from step 1>
RANK=1

for IMG in $(ls {images_dir}/*.png | sort); do
  echo "Uploading rank $RANK: $IMG"
  curl -s -X POST \
    "https://openapi.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings/${LISTING_ID}/images" \
    -H "x-api-key: ${ETSY_KEYSTRING}:${ETSY_SECRETSTRING}" \
    -H "Authorization: Bearer ${ETSY_ACCESS_TOKEN}" \
    -F "image=@${IMG}" \
    -F "rank=${RANK}" \
    -F "overwrite=true" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  → image_id={d.get(\"listing_image_id\")} rank={d.get(\"rank\")}')"
  RANK=$((RANK + 1))
done
```

Max 10 images. Upload the cover image first (rank 1).

---

### Step 3 — Upload video (if provided)

```bash
source .env

curl -s -X POST \
  "https://openapi.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings/${LISTING_ID}/videos" \
  -H "x-api-key: ${ETSY_KEYSTRING}:${ETSY_SECRETSTRING}" \
  -H "Authorization: Bearer ${ETSY_ACCESS_TOKEN}" \
  -F "video=@{video_path}" \
  -F "name=demo" | python3 -m json.tool
```

Etsy video constraints: max 15 seconds, max 100MB. Audio is muted automatically.

---

### Step 4 — Upload delivery file

For digital listings, upload the buyer download file (typically a PDF with the template link and setup guide):

```bash
source .env

curl -s -X POST \
  "https://openapi.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings/${LISTING_ID}/files" \
  -H "x-api-key: ${ETSY_KEYSTRING}:${ETSY_SECRETSTRING}" \
  -H "Authorization: Bearer ${ETSY_ACCESS_TOKEN}" \
  -F "file=@{delivery_file_path}" \
  -F "name={slug}-template.pdf" \
  -F "rank=1" | python3 -m json.tool
```

---

### Step 5 — Verify draft

```bash
source .env

curl -s "https://openapi.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings/${LISTING_ID}" \
  -H "x-api-key: ${ETSY_KEYSTRING}:${ETSY_SECRETSTRING}" \
  -H "Authorization: Bearer ${ETSY_ACCESS_TOKEN}" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(f'state={d[\"state\"]} title={d[\"title\"][:60]}...')"
```

---

## Output

Return to calling agent:

```json
{
  "listing_id": 4513026646,
  "state": "draft",
  "url": "https://www.etsy.com/listing/4513026646/..."
}
```

---

## Notes

- Tags use `tags[]` array format in form encoding — not `tags`
- Images process asynchronously; color/size data may be null immediately after upload — normal
- Video upload endpoint is `/videos` not `/video`
- Delivery file upload converts listing to digital type — always upload after creating the listing
