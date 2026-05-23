# generate-video

Assemble a short slideshow MP4 from a sequence of images using ffmpeg.
Suitable for Etsy product videos (max 15 seconds) and social media previews.

## Usage

The video mixes aspect ratios: the cover is 4:3 (2000×1500px) and preview images are 1:1 (2000×2000px).
Process each image individually, then concatenate.

### Step 1 — Convert each image to a square 1080×1080 clip

For 4:3 images (cover): center-crop to square, then scale
```bash
ffmpeg -loop 1 -t 3 -i cover.jpg \
  -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080" \
  -c:v libx264 -pix_fmt yuv420p cover_clip.mp4
```

For 1:1 images (previews): scale directly
```bash
ffmpeg -loop 1 -t 3 -i preview.jpg \
  -vf "scale=1080:1080" \
  -c:v libx264 -pix_fmt yuv420p preview_clip.mp4
```

### Step 2 — Concatenate all clips
```bash
# Create a list file
echo "file 'cover_clip.mp4'
file 'preview2_clip.mp4'
file 'preview4_clip.mp4'
file 'preview6_clip.mp4'
file 'preview8_clip.mp4'" > clips.txt

ffmpeg -f concat -safe 0 -i clips.txt -c copy output.mp4
```

### Step 3 — Clean up
Delete all `*_clip.mp4` and `clips.txt` intermediate files.

## Steps
1. Collect input images in display order
2. Convert each image to a 3-second 1080×1080 clip (use crop for 4:3, scale for 1:1)
3. Write a concat list file and join all clips
4. Move output to `images/videos/[THEME]_etsy.mp4`
5. Delete all intermediate clip files and the list file

## Parameters
- `-loop 1 -t N` — hold still image for N seconds per slide
- `crop=min(iw\,ih):min(iw\,ih)` — center-crop to largest square (no black bars)
- `scale=1080:1080` — resize to Etsy square format
- `-pix_fmt yuv420p` — required for broad compatibility (Etsy, social platforms)

## Output Location
- Etsy product video → `images/videos/[THEME]_etsy.mp4`

## Notes
- ffmpeg must be installed: `brew install ffmpeg`
- No audio needed — Etsy automatically strips audio before publishing anyway
- Total duration must be 5–15 seconds; 5 slides × 3s = 15s (at the limit — reduce to 2s per slide if needed)

## Why Square for Etsy
Etsy crops video thumbnails to square (1:1) on search and shop pages — same behaviour as cover images.
Unlike cover images (where 4:3 is preferred for the detail page), **square is the recommended format for videos** because:
- No letterboxing on mobile (25–40% higher engagement than landscape)
- Thumbnail and full video look identical — no cropping surprise
- Max file size 100MB; length must be 5–15 seconds
