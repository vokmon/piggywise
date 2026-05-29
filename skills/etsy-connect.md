# etsy-connect

Handles Etsy API authentication and provides standard call patterns. Used by any stage that makes write calls to the Etsy API.

All credentials live in `.env` at the repo root.

---

## Credentials reference

| Variable | Description |
|---|---|
| `ETSY_KEYSTRING` | App API key |
| `ETSY_SECRETSTRING` | App shared secret |
| `ETSY_ACCESS_TOKEN` | OAuth access token — expires in 1 hour |
| `ETSY_REFRESH_TOKEN` | OAuth refresh token — expires in 90 days |
| `ETSY_SHOP_ID` | Numeric shop ID (65951729 for PiggyWise) |
| `ETSY_USER_ID` | Numeric user ID (1241896221 for PiggyWise) |

---

## Step 1 — Refresh the access token

Run this at the start of every session before making any write calls. The access token expires after 1 hour; refreshing is safe to do unconditionally.

```bash
source .env

RESPONSE=$(curl -s -X POST "https://api.etsy.com/v3/public/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=${ETSY_KEYSTRING}" \
  -d "refresh_token=${ETSY_REFRESH_TOKEN}")

NEW_ACCESS_TOKEN=$(echo $RESPONSE | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
NEW_REFRESH_TOKEN=$(echo $RESPONSE | python3 -c "import json,sys; print(json.load(sys.stdin)['refresh_token'])")

# Update .env in-place
sed -i '' "s|ETSY_ACCESS_TOKEN=.*|ETSY_ACCESS_TOKEN=${NEW_ACCESS_TOKEN}|" .env
sed -i '' "s|ETSY_REFRESH_TOKEN=.*|ETSY_REFRESH_TOKEN=${NEW_REFRESH_TOKEN}|" .env

echo "Token refreshed: ${NEW_ACCESS_TOKEN:0:30}..."
```

If the refresh fails (expired refresh token), the OAuth flow must be repeated:
1. Generate new PKCE code_verifier + code_challenge (see `essentials/authentication` guide)
2. Open `https://www.etsy.com/oauth/connect?...` in browser with scopes `listings_w listings_r shops_r`
3. Capture redirect URL, extract `code=` parameter
4. Exchange code for tokens via POST to `https://api.etsy.com/v3/public/oauth/token`
5. Save new ETSY_ACCESS_TOKEN and ETSY_REFRESH_TOKEN to `.env`

---

## Standard request headers

Every Etsy API request requires both headers:

```
x-api-key: {ETSY_KEYSTRING}:{ETSY_SECRETSTRING}
Authorization: Bearer {ETSY_ACCESS_TOKEN}
```

Read-only public endpoints only need `x-api-key`. Write endpoints require both.

---

## Test connection

```bash
source .env
curl -s "https://openapi.etsy.com/v3/application/openapi-ping" \
  -H "x-api-key: ${ETSY_KEYSTRING}:${ETSY_SECRETSTRING}" | python3 -m json.tool
```

Expected: `{"application_id": ...}`

---

## Notes

- The `ETSY_KEYSTRING:ETSY_SECRETSTRING` format in `x-api-key` is required — not just the keystring alone
- Access token prefix is the user ID (e.g. `1241896221.xxx`) — do not strip it
- Refresh token also rotates on each refresh — always save both the new access and refresh tokens
