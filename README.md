# FlameWM Website

**Live site:** https://wm.arkflame.com  
**Repository:** https://github.com/ArkFlame/FlameWM-Website

## GitHub Pages fix (2026-10-16)

The previous ZIP contained `dist/index.html` but did **not** contain `index.html` at repository root. GitHub Pages configured to publish **main / (root)** therefore served the repository README instead of the site.

**Fixed:** all generated HTML, CSS, JavaScript, images, favicon assets, and the unchanged `/try/` prototype are now present directly at the repository root, alongside `.nojekyll` and `CNAME`.

### Publish now

1. Replace the repository contents with **the contents of this ZIP** (not a folder wrapping them); commit all files including `.github/workflows/pages.yml`, `index.html`, `assets/`, `features/`, `about/`, `try/`, `CNAME`, and `.nojekyll`, then push to `main`.
2. GitHub → **Settings → Pages → Build and deployment** → select **Deploy from a branch**, branch **main**, folder **/(root)** → Save. This is the simplest deployment path and requires no npm/Astro build.
3. If you prefer **GitHub Actions** as the Pages source, select it instead and run the bundled **Deploy FlameWM website** workflow. It stages *only* the approved static website and deploys it with `actions/upload-pages-artifact@v4` / `actions/deploy-pages@v4`. It never installs dependencies.
4. GitHub → **Settings → Pages → Custom domain**: `wm.arkflame.com`. Keep existing working DNS and enable **Enforce HTTPS** once available. Root `CNAME` contains exactly this domain.
5. After publishing, check `/`, `/features/`, `/about/`, and `/try/`. The homepage should begin with FlameWM's hero, **not** this README.

**Important:** A repository ZIP cannot change the GitHub repository's Settings → Pages publishing source. Step 2 or 3 must match the selected method. Do not publish from `docs/`, `dist/`, or a non-existent `gh-pages` branch.

### Verify without Node.js

```sh
python3 tests/check_static.py .
python3 scripts/site_release.py stage
python3 tests/check_static.py .pages-output
python3 -m http.server 8000
```

Open http://localhost:8000/ (plus `/features/`, `/about/`, `/try/`). Browser UI tests with Playwright can be run using `python3 tests/browser_smoke.py` if `playwright` and Chromium are installed.

### Optional Astro editing workflow

Astro templates remain in `src/`, but **the checked-in root HTML is the deployment source**. Edits to `src/` do not deploy until the new Astro build is explicitly promoted to the root:

```sh
npm install
npm run build:publish
```

This requires Node.js >=22.22.0 and network access to install Astro 7.3.8. Commit the regenerated root HTML and assets. The published website itself needs **no** npm or Node.js.

`npm run build` alone updates `dist/` locally, which Pages no longer consumes. Do not run `tests/preview_build.py` to prepare a release: that script creates a non-Astro fixture for visual tests only.

### Included content

- Responsive landing page with the real FlameWM screenshot and supplied wordmark.
- RAM comparison with **~17 MB FlameWM process RSS** identified separately from competitors' full-session measurements. These numbers are **not directly comparable**; data sources are recorded in `docs/RAM_BENCHMARK_SOURCES.md`.
- Features, About, and 404 pages, sitemap, favicon and SEO metadata.
- Preserved interactive desktop preview at `/try/` and required licensing files.
- No Jekyll theme, React, CDN, or browser framework required.

**Deployment status:** This package is locally validated; GitHub Pages publishing settings, DNS, and the final public deployment must be checked in the target repository after upload.
