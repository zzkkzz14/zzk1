# Shared Technical Standards

Common technical constraints for PPT Master.

## 1. SVG Banned Features Blacklist

### 1.0 Text characters: must be well-formed XML

SVG is strict XML. Two rules for all text and attribute values:

| Character category | Required form | Forbidden form |
|---|---|---|
| Typography & symbols (+mdash;, +ndash;, +copy;, +reg;, +rarr;, +middot;, +nbsp;, +hellip;, +bull;+) | **Raw Unicode characters** | HTML named entities |
| XML reserved characters (+amp;, +lt;, +gt;, +quot;, +apos;) | **XML entities only** | Bare + + + |

**Structural blacklist**:

| Banned Feature | Description |
|----------------|-------------|
| `mask` | Masks |
| `<style>` | Embedded stylesheets |
| `class` | CSS selector attributes |
| External CSS | External stylesheet links |
| `<foreignObject>` | Embedded external content |
| `<symbol>` + `<use>` | Symbol reference reuse |
| `textPath` | Text along a path |
| `@font-face` | Custom font declarations |
| `<animate*>` / `<set>` | SVG animations |
| `<script>` / event attributes | Scripts and interactivity |
| `<iframe>` | Embedded frames |

### 1.1 Line-end Markers (Conditionally Allowed)

`marker-start` and `marker-end` on `<line>` and `<path>` elements are allowed **only** when:

- Marker `<marker>` element defined inside `<defs>`
- `orient="auto"`
- Marker shape is one of: closed 3-vertex path/polygon (triangle), closed 4-vertex path/polygon (diamond), `<circle>` / `<ellipse>` (oval)
- Marker child's `fill` **matches** the parent line's `stroke` color
- `markerWidth` / `markerHeight` roughly in `3-15` range

### 1.2 clipPath on `<image>` (Conditionally Allowed)

`clipPath` on `<image>` is conditionally allowed for non-rectangular image crops (circle/rounded/hexagon). The converter maps qualifying clip shapes to native DrawingML picture geometry.

## 2. Transparency and Opacity

- Use `fill-opacity` / `stop-opacity` for transparency
- Do NOT use `rgba()` or `rgb()` color functions with alpha channel
- All transparency must be expressed via opacity attributes on fills and strokes

## 3. Gradients

- Use `<linearGradient>` / `<radialGradient>` / `<conicGradient>` for gradient fills
- Gradient stops must use `stop-opacity` for transparency, NOT `rgba()`
- For image gradient overlays, use stacked `<rect>` with gradients instead of `<mask>`

## 4. Filters

- `<feDropShadow>` / `<feGaussianBlur>` are accepted but PPT export is inconsistent
- Bake into the source image when fidelity is critical

## 5. Pattern Fill

`<pattern>` fills are conditionally allowed when:

- Pattern has `data-pptx-pattern` attribute with valid OOXML preset value
- Pattern geometry is simple (converter emits named PPTX preset only)

**Valid `data-pptx-pattern` values**:

| Category | Values |
|---|---|
| Grids | `smGrid`, `lgGrid`, `dotGrid` |
| Diagonal lines | `ltUpDiag`, `ltDnDiag`, `dkUpDiag`, `dkDnDiag`, `wdUpDiag`, `wdDnDiag`, `dashUpDiag`, `dashDnDiag`, `diagCross` |
| Horizontal / vertical lines | `horz`, `vert`, `ltHorz`, `ltVert`, `dkHorz`, `dkVert`, `narHorz`, `narVert`, `dashHorz`, `dashVert`, `cross` |
| Percent fills | `pct5` through `pct90` |
| Checks & confetti | `smCheck`, `lgCheck`, `smConfetti`, `lgConfetti` |
| Decorative | `horzBrick`, `diagBrick`, `weave`, `plaid`, `trellis`, `zigZag`, `wave`, `sphere`, `divot`, `shingle`, `solidDmnd`, `openDmnd`, `dotDmnd` |

## 6. Image Overlay Techniques

Replace `<mask>` effects:

- Image gradient overlay (vignette/fade/tint) + stacked `<rect>` with `<linearGradient>`/`<radialGradient>`
- Non-rectangular image crop (circle/rounded/hexagon) + `clipPath` on `<image>`
- Inner glow / soft-edge + `<filter>` with `<feGaussianBlur>`
- Drop shadow + filter shadow or layered rect

## 7. Element Rotation

Rotation converts to native PPTX `<a:xfrm rot="...">`. Supported on all element types.

```xml
<rect x="100" y="100" width="60" height="60" fill="#1A73E8" fill-opacity="0.1"
  transform="rotate(45, 130, 130)"/>
```

## 8. Arc Paths + Donut / Pie Charts

Calculate arc endpoint coordinates precisely with trigonometry.

**Calculation formula** (center `cx,cy`, radius `r`, angle `+` in degrees):
```
x = cx + r + cos(+ + + / 180)
y = cy + r + sin(+ + + / 180)
```

**Key rules**:
1. Start at **-90+** (12 o'clock position) and go clockwise
2. Each sector spans `percentage + 360+`
3. Use **large-arc flag = 1** when the sector is > 180+, **0** otherwise
4. sweep-direction = 1 (clockwise) for outer arc, 0 (counter-clockwise) for inner arc returning
5. **Always verify** that the sum of all sector angles equals 360+

## 9. Project Directory Structure

```
project/
+-- svg_output/    # Raw SVGs (Executor output, contains placeholders)
+-- svg_final/     # Post-processed final SVGs (finalize_svg.py output)
+-- images/        # Image assets (user-provided + AI-generated)
+-- notes/         # Speaker notes (.md files matching SVG names)
|   +-- total.md   # Complete speaker notes document (before splitting)
+-- templates/     # Project templates (if any)
+-- *.pptx         # Exported PPT file
```
