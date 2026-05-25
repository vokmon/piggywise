# record-video

Record a browser session as a `.webm` video using Playwright. Use this for marketing clips, tutorials, and research walkthroughs.

Uses the `playwright-recorder` MCP server (`mcp__playwright-recorder__*`), not the regular `playwright` server. The recorder uses Playwright's bundled Chromium with `--sandbox` and `--caps=devtools`, which supports video recording.

Follows `skills/playwright.md` for general browser rules.

---

## Input

- `filename` — output filename without path, e.g. `adhd-planner-trends.webm`
- `output_dir` — where to save the file, e.g. `assets/videos/`
- `size` — video dimensions (default: `1280x720`)
- `steps` — the navigation and interaction steps to record (described by the caller)

---

## Steps

### 1. Start recording

Call `browser_start_video` **before any navigation**:
- `filename`: the provided filename
- `size`: `{ width: 1280, height: 720 }` (or caller-specified)

### 2. Execute steps

Perform all navigation and interaction steps described by the caller.

### 3. Stop recording

Call `browser_stop_video`.

### 4. Close browser

Call `browser_close`.

### 5. Move to output_dir

```bash
mv .playwright-mcp/{filename} {output_dir}/{filename}
```

### 6. Clean up

```bash
find .playwright-mcp -delete
```

### 7. Report

Confirm the saved path and file size.

---

## Rules

- Always call `browser_start_video` **before** the first navigation — starting it on an already-loaded page results in no video recorded.
- If the first navigation returns an error page (4xx, 5xx, captcha): stop recording immediately, close browser, clean up, and report failure. Do not continue — a broken first navigation kills the recording context.
- Keep recordings focused — stop as soon as the content is captured.
- Do not record login screens or pages with personal data.
- Google Trends rate-limits automated browsers — if it returns 429, wait a few minutes before retrying.

---

## Output

```
Saved: {output_dir}/{filename} ({size_kb}KB)
```
