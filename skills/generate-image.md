# generate-image

Generate images using codex for covers, marketing assets, and layouts.

## Usage
```bash
echo "<detailed image prompt>" | codex exec
```

## Steps
1. Write a detailed prompt describing the image — style, dimensions, colors, content, mood
2. Run: `echo "<prompt>" | codex exec`
3. Move output image to the appropriate folder under the product's `images/` directory
4. Delete the generated image from the codex output location

## Prompt Tips
- Be specific: include style, colors, dimensions, text to display, and mood
- Describe the subject, background, composition, lighting, and any text overlays
- State the intended use: cover image, preview, mock-up, icon, etc.

## Output Location
- Etsy covers → `images/covers/`
- Preview images → `images/previews/`
