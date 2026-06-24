---
name: ppt-master
description: >
  AI-driven multi-format SVG content generation system. Converts source documents
  (PDF/DOCX/URL/Markdown) into high-quality SVG pages and exports to PPTX through
  multi-role collaboration. Use when user asks to "create PPT", "make presentation",
  "生成PPT", "做PPT", "制作演示文稿", or mentions "ppt-master".
---

# PPT Master Skill

> AI-driven multi-format SVG content generation system. Converts source documents into high-quality SVG pages through multi-role collaboration and exports to PPTX.

**Core Pipeline**: `Source Document -> Create Project -> [Template] -> Strategist -> [Image_Generator] -> Executor Live Preview -> Quality Check -> Post-processing -> Export`

## Critical Rules

1. **SERIAL EXECUTION** - Steps MUST be executed in order; the output of each step is the input for the next
2. **BLOCKING = HARD STOP** - Steps marked BLOCKING require a full stop; wait for explicit user response
3. **NO CROSS-PHASE BUNDLING** - Cross-phase bundling is FORBIDDEN
4. **GATE BEFORE ENTRY** - Each Step has prerequisites that MUST be verified before starting
5. **NO SPECULATIVE EXECUTION** - Pre-preparing content for subsequent Steps is FORBIDDEN
6. **NO SUB-AGENT SVG GENERATION** - SVG generation MUST be completed by the current main agent end-to-end
7. **SEQUENTIAL PAGE GENERATION ONLY** - SVG pages MUST be generated sequentially page by page
8. **SPEC_LOCK RE-READ PER PAGE** - Before generating each SVG page, read spec_lock.md for colors/fonts/icons/images
9. **SVG MUST BE HAND-WRITTEN** - Every SVG page is written by the main agent directly, NOT script-generated

## Language & Communication

- **Response language**: match the user's input and source materials
- **Template format**: design_spec.md MUST follow its original English template structure

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `scripts/source_to_md/pdf_to_md.py` | PDF to Markdown |
| `scripts/source_to_md/doc_to_md.py` | Documents to Markdown |
| `scripts/svg_to_pptx.py` | SVG to PPTX export |
| `scripts/finalize_svg.py` | Post-process SVG files |
| `scripts/analyze_images.py` | Analyze user-provided images |
| `scripts/image_gen.py` | AI image generation |
| `scripts/image_search.py` | Web image search |
| `scripts/notes_to_audio.py` | Speaker notes to audio |
| `scripts/live_preview.py` | Live preview HTTP server |
| `scripts/animation_config.py` | Animation configuration |

## Project Structure

```
project/
+-- svg_output/    # Raw SVGs (Executor output)
+-- svg_final/     # Post-processed final SVGs
+-- images/        # Image assets
+-- notes/         # Speaker notes
+-- templates/     # Project templates
+-- *.pptx         # Exported PPT file
```

## SVG Technical Standards

### Banned Features

- `mask` - Use gradient overlays or clipPath instead
- `<style>` - Use inline attributes
- `class` - Use id or inline styles
- External CSS - Use inline styles only
- `<foreignObject>` - Not supported
- `<symbol>` + `<use>` - Not supported
- `textPath` - Not supported
- `@font-face` - Use system fonts
- `<animate*>` / `<set>` - Use PPTX animations instead
- `<script>` / event attributes - Not supported

### Character Encoding

- Use raw Unicode characters for typography (+mdash;, +copy;, +rarr;, etc.)
- Use XML entities for reserved characters (+amp;, +lt;, +gt;, +quot;, +apos;)

### Image Embedding

- Use external references in `svg_output/`: `<image href="../images/img.png" x="0" y="0" width="1280" height="720"/>`
- Use base64 embedding in `svg_final/` for delivery
- Supports: PNG, JPEG, GIF, WebP, SVG

### Canvas Formats

| Format | viewBox | Ratio | Use Case |
|--------|---------|-------|----------|
| PPT 16:9 | `0 0 1280 720` | 16:9 | Business presentations |
| PPT 4:3 | `0 0 1024 768` | 4:3 | Traditional projectors |
| Xiaohongshu | `0 0 1242 1660` | 3:4 | Image-text sharing |
| WeChat Moments | `0 0 1080 1080` | 1:1 | Square posters |
| Story/TikTok | `0 0 1080 1920` | 9:16 | Vertical stories |

## Animation System

### Page Transitions

```bash
python3 svg_to_pptx.py <project> -t fade --transition-duration 0.4
```

Effects: fade, push, wipe, split, strips, cover, random

### Per-Element Animations

Disabled by default. Enable with:

```bash
python3 svg_to_pptx.py <project> -a auto
```

Effects: fade, wipe, fly, zoom, dissolve, circle, box, diamond, wheel, blinds, checkerboard, cut, random_bars, wedge, expand, swivel

### Animation Triggers

- `on-click` - Presenter-paced reveals
- `with-previous` - All groups animate together
- `after-previous` - Cascade after previous (default)

## QA Checklist

Before delivery:

1. Check for unintended overlap between elements
2. Verify font sizes meet minimum requirements (50pt titles, 35pt slide titles, 24pt subheadings, 16pt body)
3. Ensure no banned SVG features are used
4. Verify all images are properly embedded or referenced
5. Check text wrapping and line breaks
6. Test animations if enabled
7. Verify speaker notes if generated

## Role Switching

Before switching roles, read the corresponding reference file:

```markdown
## [Role Switch: <Role Name>]
Reading role definition: references/<filename>.md
Current task: <brief description>
```

## Notes

- Local preview: `python3 -m http.server -d <project_path>/svg_final 8000`
- Troubleshooting: check `docs/faq.md` for known solutions
- For narrated decks, use `generate-audio` workflow
- For custom animations, use `customize-animations` workflow
