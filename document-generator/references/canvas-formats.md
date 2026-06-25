# Canvas Format Specification

## Format Quick Reference

| Format | viewBox | Ratio | Use Case |
|--------|---------|-------|----------|
| PPT 16:9 | `0 0 1280 720` | 16:9 | Business presentations, meetings |
| PPT 4:3 | `0 0 1024 768` | 4:3 | Traditional projectors, academic talks |
| Xiaohongshu (RED) | `0 0 1242 1660` | 3:4 | Image-text sharing, knowledge posts |
| WeChat Moments / IG | `0 0 1080 1080` | 1:1 | Square posters, brand showcases |
| Story / TikTok | `0 0 1080 1920` | 9:16 | Vertical stories, short video covers |
| WeChat Article Header | `0 0 900 383` | 2.35:1 | WeChat article cover images |
| Landscape Banner | `0 0 1920 1080` | 16:9 | Web banners, digital screens |
| Portrait Poster | `0 0 1080 1920` | 9:16 | Phone screens, elevator ads |
| A4 Print | `0 0 1240 1754` | 1:sqrt(2) | Print posters, flyers |

## Layout Principles

### Landscape (16:9, 4:3, 2.35:1)
- Visual flow: Z-pattern, left to right
- Margins: 40-80px
- Layouts: multi-column, left-right split, grid
- Card dimensions (16:9): single-row 530-600px, double-row 265-295px

### Portrait (3:4, 9:16)
- Visual flow: top to bottom
- Margins: 60-120px
- Layouts: single-column, top-bottom split, card stacking
- Card dimensions (3:4): height 400-600px, gap 40-60px

### Square (1:1)
- Visual flow: center-radiating
- Margins: 60-100px
- Core area: ~800x800px

## ViewBox Examples

```xml
<svg width="1280" height="720" viewBox="0 0 1280 720">   <!-- PPT 16:9 -->
<svg width="1242" height="1660" viewBox="0 0 1242 1660"> <!-- Xiaohongshu -->
<svg width="1080" height="1080" viewBox="0 0 1080 1080"> <!-- WeChat Moments -->
<svg width="1080" height="1920" viewBox="0 0 1080 1920"> <!-- Story -->
<svg width="900" height="383" viewBox="0 0 900 383">     <!-- WeChat Article Header -->
```
