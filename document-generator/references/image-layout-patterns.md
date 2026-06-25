# Image-Text Layout Patterns

A vocabulary registry of ways images can be placed on a slide.

## Core Principle

> **The image carries atmosphere, world-building, emotional weight. Native SVG shapes carry information, data, editable text.**

Let the image **be the canvas** (often full-bleed) and draw native vector elements (annotation cards, flow nodes, KPI tiles, leader lines) directly on top.

## Part 1 + Primary Structures

### Container Layouts

1. **Full-bleed background with floating title** + `<image x=0 y=0 width=1280 height=720 preserveAspectRatio="xMidYMid slice"/>` + scrim `<rect>` for legibility + overlay `<text>`

2. **Left-third image + right text body** + `<image x=0 y=0 width=~427 height=720>` on the left; text area in the remaining width

3. **Right-third image + left text body** + mirror of #2

4. **Right image bleeding off the canvas edge** + `<image>` width extended past viewBox; text on left with a rightward gradient fade

5. **Top-band image + bottom multi-column text** + `<image x=0 y=0 width=1280 height=~340>` at the top + bottom-fade gradient + 2-3 evenly spaced text columns below

6. **Bottom-band image + top title + middle text** + mirror of #5

7. **Top-and-bottom symmetric split** + image occupies 50% with a divider line or thin gradient band

8. **Z-pattern serpentine** + three rows, image on the left in rows 1 and 3, on the right in row 2

9. **3+3 grid with central image** + nine cells; center cell holds the image

10. **Centered image with radial callouts** + image (often circular via `clipPath`) at canvas center; multiple `<line>` leader lines + small `<circle>` endpoints + offset text labels

11. **Diagonal split with directional gradient** + full-bleed `<image>` + overlay `<rect fill="url(#grad)">` whose `<linearGradient>` axis runs along the desired diagonal

12. **Faded image as backdrop with oversized overlay text** + `<image>` + heavy semi-transparent `<rect fill="bg-color" fill-opacity="0.5-0.7">` over it + huge `<text>` (80-120px) on top

13. **Narrow vertical image strip + giant horizontal title** + `<image x=0 y=0 width=200-280 height=720>` + thick divider `<rect>` + large `<text>` (60-90px)

14. **Horizontal banner strip cutting through mid-section** + `<image y=middle width=1280 height=200-280>` with edge fades

15. **Multi-image montage with bold text spanning across** + multiple `<image>` tiled with 2-4px gaps + large `<text>` in a darkened band

16. **Negative-space dominant + small image, mostly whitespace** + minimal image placement with generous margins

17. **Asymmetric split with overlapping elements** + two columns with intentional overlap between image and text blocks

18. **Layered depth with parallax effect** + multiple image layers at different scales with subtle offset

19. **Frame-within-frame composition** + image inside a styled frame/container with decorative elements

## Part 2 + Modifier Layers

20. **Image with gradient overlay** + `<linearGradient>` from solid to transparent for text legibility

21. **Rounded-rectangle clipPath** + `rx=6` or circle for softer image edges

22. **Top-edge color overlay** + `<linearGradient>` in the deck's accent color, opacity 0.55 -> 0

23. **Bottom-edge fade to background** + `<linearGradient>` fading to background color, opacity 0 -> 0.95

24. **Vignette effect** + radial gradient darkening edges

25. **Duotone overlay** + two-color gradient overlay on image

26. **Soft blur background** + `<feGaussianBlur>` on image behind sharp foreground content

27. **Color block badge** + small `<rect>` with accent color + label text

28. **Leader lines with endpoints** + `<line>` + `<circle>` connecting image to annotations

29. **Callout boxes** + `<rect>` with arrow pointing to image feature

30. **Overlay data widgets** + KPI tiles, mini-charts drawn as native SVG on top of image

31. **Text mask effect** + letterforms revealing image (baked into source image, not runtime SVG mask)

32. **Rotated image for editorial feel** + `transform="rotate(angle cx cy)"` on the `<image>`, 2-6 degrees

33. **Thin colored matte frame** + `<rect fill="none" stroke="#color" stroke-width="2-6"/>` over image edge

34. **Multiple stacked frames** + nested `<rect>` outlines giving a "framed photograph" look

35. **Image-to-image transition** + two `<image>` elements with overlapping regions and gradient masks

36. **Half-tone or dot pattern overlay** + `<pattern>` with dots for texture

37. **Geometric shape accents** + `<polygon>`, `<circle>`, `<path>` decorative elements around image

## Composition Guidance

- Pick one or more **Primary Structures** as the page's bones
- Add any number of **Modifier Layers** for finish
- Both stack + the question is "is the next layer still earning its place"
- **Cross-primary combinations are encouraged** + combine when the page asks for it

## Hard Constraints

- Long body copy, data points, numeric labels, and Chinese text always go in the SVG layer + never baked into the image
- `<clipPath>` on `<image>` and transparency encoding (`fill-opacity` / `stop-opacity`, never `rgba()`)
- No `<mask>`, no `<feComposite>` for alpha compositing
- `<feDropShadow>` / `<feGaussianBlur>` are accepted but PPT export is inconsistent + bake into source image when fidelity is critical
