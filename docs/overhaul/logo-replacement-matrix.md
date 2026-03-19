# Logo and Icon Replacement Matrix

Date: 2026-02-13
Checklist ID: `T008`

## Current Desktop Assets

| Area | Current Path | Current State | Replacement Requirement |
|---|---|---|---|
| App icon | `App/assets/icons/app_icon.png` | Neutral placeholder icon | Replace with finalized EON app icon set (`16/32/64/256`) |
| Toolbar open | `App/assets/icons/open.png` | Neutral placeholder icon | Replace with EON-styled open-file glyph |
| Toolbar slice | `App/assets/icons/slice.png` | Neutral placeholder icon | Replace with EON-styled slice glyph |
| Toolbar print | `App/assets/icons/print.png` | Neutral placeholder icon | Replace with EON-styled print glyph |

## Web Asset Targets (Planned)

| Area | Planned Path | Replacement Requirement |
|---|---|---|
| Favicon | `platform/frontend/public/favicon.*` | Use EON brand favicon set |
| PWA icon | `platform/frontend/public/icon-*` | Use EON app icon set |
| Login/hero mark | `platform/frontend/src/assets/` | Use EON logo mark only |

## Rules

- Do not import any upstream logos, wordmarks, or splash screens.
- Keep source files for brand assets in first-party asset directories only.
