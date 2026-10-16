# FlameWM Website — Verification ledger

Date: 2026-10-16

## Included

- Astro 7.3.8 static site source: overview, features, about, 404, shared responsive layout and CSS.
- GitHub Actions Pages deployment workflow, custom domain `wm.arkflame.com`.
- Preserved full interactive browser prototype under `public/try/` (112/112 original files, byte-for-byte unchanged).
- Browser-tested static preview in `dist/`; this is a rendering fixture generated offline, **not** Astro compiler output.
- Development placeholder images and self-contained preview illustrations; no claims that they are shipped native screenshots.

## Verified in this environment

- `python3 tests/preview_build.py` — completed.
- `python3 tests/check_static.py dist` — PASS (12 mandatory outputs, local links, sitemap).
- `python3 tests/browser_smoke.py` — PASS (nine viewports/routes, menu accessibility, desktop preview image, prototype launcher toggle).
- `node --check public/assets/js/site.js` — PASS.
- `node --check public/try/app.js` — PASS.
- Pixel horizontal overflow in nine tested desktop and mobile layouts: 0px.

## Not independently verified

- `npm install && npm run build` could not run in this restricted sandbox: npm registry lookup returns `EAI_AGAIN`. No Astro-built output or live GitHub Pages deployment is claimed.
- GitHub Pages setup, DNS and HTTPS require repository/site controls. Verify workflow success after pushing.

## Repository publishing

Push the **root source** to the website repository, including `.github/workflows/pages.yml`. In Settings -> Pages select **GitHub Actions** and configure the custom domain **wm.arkflame.com**. This workflow builds `dist/` from the Astro source then deploys. Do not select branch-based Jekyll publishing for Astro source.
