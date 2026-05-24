# pinterest-lookup

Authenticate with Pinterest using email/password credentials from environment variables.

## Steps

1. Check for credentials:
   ```bash
   echo $PINTEREST_EMAIL
   echo $PINTEREST_PASSWORD
   ```

2. If both are set:
   - Navigate to `https://www.pinterest.com/login/`
   - Fill the email field with `$PINTEREST_EMAIL` and the password field with `$PINTEREST_PASSWORD`
   - Click "Log in" and wait for the redirect back to `https://www.pinterest.com/`
   - Return `{ "logged_in": true }`

3. If credentials are not set: return `{ "logged_in": false }`.

## Output

```json
{ "logged_in": true }
```
or
```json
{ "logged_in": false }
```

## Notes
- If `logged_in: false`, the calling skill must handle its own fallback (typically WebSearch).
- Do not navigate to Pinterest Trends after login — the calling skill handles all subsequent navigation.
