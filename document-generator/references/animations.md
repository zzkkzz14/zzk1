# Page Transitions + Per-Element Animations

PPT Master's exported PPTX supports **page transitions** (slide-to-slide) and **per-element entrance animations** (within a slide).

## Defaults

| Layer | Default | Why |
|---|---|---|
| Page transition | `fade`, 0.4s | Calm baseline that suits most decks |
| Per-element animation | **`none` (off)** | Auto-firing element builds reads as "AI deck" tell, so element entrance is opt-in |

## Page Transitions

```bash
python3 svg_to_pptx.py <project> -t fade --transition-duration 0.4
```

Effects: `fade`, `push`, `wipe`, `split`, `strips`, `cover`, `random`

Flags:
- `-t/--transition` + effect name, or `none` to disable. Default: `fade`
- `--transition-duration` + seconds, default `0.4`
- `--auto-advance` + seconds; omit for presenter-controlled advance

## Per-Element Animations

Enable deck-wide with:

```bash
python3 svg_to_pptx.py <project> -a auto
```

### Effects

- `auto` + maps from group id: chart+wipe, card-/step-/pillar-+fly, title/takeaway+fade; image-like ids cycle zoom/dissolve/circle/box/diamond/wheel
- `mixed` + legacy 16-effect cycle
- `random` + samples from legacy pool
- Specific effect: `fade`, `wipe`, `fly`, `zoom`, `dissolve`, `circle`, `box`, `diamond`, `wheel`, `blinds`, `checkerboard`, `cut`, `random_bars`, `wedge`, `expand`, `swivel`

### Animation Triggers

- `on-click` + presenter-paced reveals
- `with-previous` + all groups animate together
- `after-previous` + cascade after previous (default)

Flags:
- `-a/--animation` + effect name, `auto`, `mixed`, `random`, or `none`. Default: `none`
- `--animation-trigger` + Start mode: `on-click`, `with-previous`, or `after-previous`
- `--animation-duration` + per-element entrance seconds, default `0.4`
- `--animation-stagger` + gap between elements in `after-previous` mode, default `0.5`
- `--animation-config` + sidecar path. Default: `<project>/animations.json`

## Anchor Logic

Per-element animations are anchored on **top-level `<g id="...">` content groups** in the SVG.

- Aim for **3-8 content groups per slide**
- **Chrome groups skip the cascade automatically** + groups matching `background`/`bg`/`decoration`/`header`/`footer`/`watermark`/`pagenumber`/`nav`/`logo`/`rule` are excluded
- **Fallback for flat SVGs** (no top-level `<g>` wrappers):
  - + 8 visible top-level primitives + each becomes one anchor
  - > 8 + animation is skipped on that slide

## Custom Object-Level Animation

Create `animations.json` sidecar:

```json
{
  "version": 1,
  "slides": {
    "03_market": {
      "groups": {
        "title": { "effect": "fade", "order": 1 },
        "chart": { "effect": "wipe", "order": 2, "duration": 0.6 },
        "insight": { "effect": "fly", "order": 3, "delay": 0.2 },
        "footer": { "effect": "none" }
      }
    }
  }
}
```

Rules:
- `slides` keys match SVG stems (`03_market.svg` + `03_market`)
- `groups` keys match top-level `<g id="...">` anchors
- `effect: none` removes that group from the entrance sequence
- `order` changes animation order only
- `delay` is seconds before that group starts in `after-previous` mode
- `duration` overrides the per-group entrance duration

## Quick Reference

| Goal | Command |
|---|---|
| Disable transitions | `-t none` |
| Change transition effect | `-t push` |
| Slower transition | `--transition-duration 0.8` |
| Auto-play | `--auto-advance 5` |
| Disable element animation | `-a none` |
| Switch to on-click trigger | `--animation-trigger on-click` |
| Use a single effect | `--animation fade` |
| All groups animate together | `--animation-trigger with-previous` |
| Slower per-element reveal | `--animation-duration 0.5` |
| Wider gap in after-previous | `--animation-stagger 0.7` |
