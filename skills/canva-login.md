# canva-login

Authenticate with Canva using email/password credentials from environment variables. Called by build skills before copying a public template into the workspace.

## Steps

1. Read credentials from .env: `CANVA_EMAIL` and `CANVA_PASSWORD`

2. Check for credentials:

   ```bash
   echo $CANVA_EMAIL
   echo $CANVA_PASSWORD
   ```

3. If both are set:
   - Navigate to `https://www.canva.com/login`
   - Enter `$CANVA_EMAIL` in the email field and click "Continue"
   - Enter `$CANVA_PASSWORD` in the password field and click "Log in"
   - Wait for redirect to the Canva home page (`https://www.canva.com/`)
   - Return `{ "logged_in": true }`

4. If credentials are not set: return `{ "logged_in": false }`.

## Output

```json
{ "logged_in": true }
```

or

```json
{ "logged_in": false }
```

## Notes

- If `logged_in: false`, the calling skill must stop and ask the human to set `CANVA_EMAIL` and `CANVA_PASSWORD` in `.env` before continuing.
- Do not navigate anywhere after login — the calling skill handles all subsequent navigation.
- If already logged in (session still active), the redirect to home happens immediately — treat this as a successful login.
