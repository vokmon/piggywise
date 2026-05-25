# notion-login

Authenticate with Notion using email/password credentials from environment variables. Called by build skills before duplicating a public template into the workspace.

## Steps

1. Read credentials from .env: `NOTION_EMAIL` and `NOTION_PASSWORD`

2. Check for credentials:

   ```bash
   echo $NOTION_EMAIL
   echo $NOTION_PASSWORD
   ```

3. If both are set:
   - Navigate to `https://www.notion.so/login`
   - Enter `$NOTION_EMAIL` in the email field and click "Continue with email"
   - Enter `$NOTION_PASSWORD` in the password field and click "Continue"
   - Wait for redirect to the Notion workspace (`https://www.notion.so/`)
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

- If `logged_in: false`, the calling skill must stop and ask the human to set `NOTION_EMAIL` and `NOTION_PASSWORD` in `.env` before continuing.
- Do not navigate anywhere after login — the calling skill handles all subsequent navigation.
- If already logged in (session still active), the redirect to workspace happens immediately — treat this as a successful login.
