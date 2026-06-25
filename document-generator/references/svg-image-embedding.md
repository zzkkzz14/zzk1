# SVG Image Embedding Guide

## Image Resource List Format

Each image carries an `Acquire Via` field plus a status annotation.

| Filename | Dimensions | Purpose | Type | Acquire Via | Status | Reference |
|----------|------------|---------|------|-------------|--------|-----------|
| cover_bg.png | 1280x720 | Cover background | Background | ai | Pending | Modern tech abstract, deep blue gradient |
| team.jpg | 800x600 | Team photo | Photography | web | Pending | Diverse engineering team in modern office |
| product.png | 600x400 | Page 3 product photo | Photography | user | Existing | - |

### Image Status Enum

| Status | Meaning | Executor Handling |
|--------|---------|-------------------|
| **Pending** | Acquisition needed (`ai` or `web`); not yet attempted | Image Acquisition Phase consumes this |
| **Generated** | AI-generated file exists at expected path | Reference from `../images/` |
| **Sourced** | Web-sourced file exists at expected path | Reference from `../images/`; check license for attribution |
| **Rendered** | Deterministic formula PNG exists | Reference from `../images/`; use `preserveAspectRatio="xMidYMid meet"` |
| **Needs-Manual** | Acquisition attempted once + one retry, failed | Dashed placeholder unless user supplied file |
| **Existing** | User already has image | Place in `images/`, reference with `<image>` |
| **Placeholder** | Intentionally not prepared yet | Dashed border placeholder; replace later |

## Workflow

```
1. Strategist defines image needs -> Add image resource list
2. Image Acquisition (Step 5):
   - Pending + ai  -> Image_Generator runs image_gen.py     -> Generated
   - Pending + web -> Image_Searcher runs image_search.py   -> Sourced
   - formula / user / placeholder rows are skipped
3. Executor generates SVGs (svg_output/)
   - Existing / Generated -> <image href="../images/xxx.png" .../>
   - Sourced + no-attribution -> <image href=...> only
   - Sourced + attribution-required -> <image href=...> + <text> credit
   - Rendered formula -> <image href="../images/formula_001.png" preserveAspectRatio="xMidYMid meet" .../>
   - Placeholder / Needs-Manual -> Dashed border + description text
4. Preview: python3 -m http.server -d <project_path> 8000
5. Post-processing + Export
```

## Method 1: External Reference (Recommended for Generation Phase)

### Syntax

```xml
<image href="../images/image.png" x="0" y="0" width="1280" height="720"
       preserveAspectRatio="xMidYMid slice"/>
```

### Key Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `href` | Image path (relative or absolute) | `"../images/cover.png"` |
| `x`, `y` | Image top-left corner position | `x="0" y="0"` |
| `width`, `height` | Image display dimensions | `width="1280" height="720"` |
| `preserveAspectRatio` | Scaling mode | `"xMidYMid slice"` |

### preserveAspectRatio Common Values

| Value | Effect |
|-------|--------|
| `xMidYMid slice` | Center crop (similar to CSS `cover`) |
| `xMidYMid meet` | Complete display (similar to CSS `contain`) |
| `none` | Stretch to fill, no aspect ratio preservation |

## Method 2: Base64 Embedding (Recommended for Delivery Phase)

```xml
<image href="data:image/png;base64,iVBORw0KGgo..." x="0" y="0" width="1280" height="720"/>
```

### MIME Types

| MIME Type | File Format |
|-----------|-------------|
| `image/png` | PNG |
| `image/jpeg` | JPG/JPEG |
| `image/gif` | GIF |
| `image/webp` | WebP |
| `image/svg+xml` | SVG |

## Best Practices

### Image Optimization

```bash
convert input.png -quality 85 -resize 1920x1080\> output.png  # ImageMagick
pngquant --quality=65-80 input.png -o output.png               # pngquant (recommended)
```

### File Organization

```
project/
+-- images/            # Image assets
+-- sources/           # Source files and their accompanying images
+-- svg_output/        # Raw version (external references)
+-- svg_final/         # Final version (images embedded)
```

### Rounded Corner / Non-rectangular Image Cropping

`clipPath` **on `<image>` elements** is conditionally allowed. Fallback when `clipPath` doesn't fit: bake rounded corners into the source image (PNG with alpha) before embedding.
