# FlameWM Website — release verification

The **published site is at repository root**. GitHub Pages can publish `main / (root)` directly. `.nojekyll` prevents Ruby/Jekyll from transforming content. `CNAME` retains `wm.arkflame.com`.

The included `.github/workflows/pages.yml` provides an alternative GitHub Actions source that copies root published files to `.pages-output`, validates them and uploads with `actions/upload-pages-artifact@v4`, then deploys with `actions/deploy-pages@v4`. **No Node/npm dependency in the deployment workflow.**

## Commands

```sh
python3 tests/check_static.py .
python3 scripts/site_release.py stage
python3 tests/check_static.py .pages-output
python3 tests/http_smoke.py
python3 tests/browser_smoke.py  # requires Playwright + Chromium
```

Last local verification: static checks, HTTP routes, nine responsive browser cases, `/try/` launcher and assets passed. Actual GitHub publishing/DNS/CDN behavior was not tested or modified.

Astro source remains under `src/` for editing. If intentionally rebuilding it later, run `npm install && npm run build:publish` and commit the resulting root HTML/assets. Do not deploy `tests/preview_build.py` fixtures.
