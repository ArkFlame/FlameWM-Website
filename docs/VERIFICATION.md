# FlameWM Website — GitHub Pages publishing fix

Date: 2026-10-16

## Root cause

The uploaded repository had `dist/index.html` but **no root `index.html`**. When GitHub Pages published branch `main` / `(root)`, the README was available as a fallback entry page. Astro was not being compiled by branch-based Pages hosting.

## Fix

The existing tested static website has been promoted into the repository root (HTML, CSS, JS, images, fonts, routes, favicon, `.nojekyll`, `CNAME`). GitHub Pages branch publishing now has a real root entry file. The custom Actions workflow deploys an independently checked static snapshot using the official Pages upload/deploy actions; it does not require npm or Astro.

## Verified locally

- `python3 tests/check_static.py .` — PASS.
- `python3 scripts/site_release.py stage` — output generated.
- `python3 tests/check_static.py .pages-output` — PASS.
- `python3 tests/browser_smoke.py` — nine desktop/mobile page sizes, homepage assets, RAM chart, demo Start toggle — PASS.
- `python3 tests/http_smoke.py` — 10 real HTTP routes/assets — PASS.
- Original `public/try/` and publishable `try/`: 112 identical files (SHA-256 byte comparison).
- YAML workflow parses; official `actions/upload-pages-artifact@v4` + `actions/deploy-pages@v4` syntax verified against GitHub docs.

## External verification needed

- Actual GitHub Pages publishing source (Settings → Pages) is an account setting that an archive cannot change. Choose `main` / `(root)` or `GitHub Actions`; both are supported.
- Confirm new public deployment of `https://wm.arkflame.com/` serves FlameWM, not README.
- Astro compiler build is **optional** for this release and was not run in this environment. Root static HTML is the checked-in publishing authority.
