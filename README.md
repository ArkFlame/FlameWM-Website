# FlameWM Website

Independent static website for [FlameWM](https://github.com/ArkFlame/flamewm), by ArkFlame Studios.

**Published URL:** https://wm.arkflame.com

## Architecture

- Plain HTML, CSS, JavaScript. No Astro, Jekyll, npm or build step.
- `index.html`, `features/index.html`, `about/index.html`, `404.html`: published pages.
- `assets/css/site.css`: all styling, responsive design, scroll transitions and reduced-motion support.
- `assets/js/site.js`: right ruler/progress, active section headings, rising next-section typography, restrained hero parallax, mobile navigation, screenshot lightbox, reveal and bar animation, and benchmark scroller progress.
- `assets/brand`: FlameWM wordmark and real development screenshot.
- `assets/de-logos`: MATE/Xfce/KDE/IceWM source assets and original illustrative emblems for LXQt, GNOME, Cinnamon and Budgie; see `ASSET_SOURCES.md`.
- `try/`: original interactive browser desktop prototype, preserved.
- `docs/RAM_BENCHMARK_SOURCES.md`: reported external measurements and critical non-comparability disclaimer.
- `.github/workflows/pages.yml`: deploy the checked-in static root using GitHub Pages Actions.

## Publish on GitHub Pages

1. Extract the package **contents** to the repository root (not into a nested folder). Ensure `index.html` is in the root.
2. Commit/push to the default `main` branch.
3. GitHub → Settings → Pages → Source: **GitHub Actions**. The included workflow validates/stages and publishes the static files.
4. Keep the `wm.arkflame.com` custom domain. `CNAME` is included.

Alternatively choose **Deploy from a branch** → `main` → `/(root)` because the site is already static at the repository root. Choose **only one** deployment source.

## Preview and test

Local preview: run `./preview.sh` from the extracted website directory. It serves the website at `http://127.0.0.1:8080/`, opens your default browser on Linux desktops, and stops with Ctrl+C. Use `./preview.sh 8081` to select a different port, or `./preview.sh --no-browser` when testing without a graphical browser. Requires only Python 3; no npm or Astro.

Dependency-free checks: `python3 tests/check_static.py .`.

Optional Chromium browser tests: `python3 tests/browser_smoke.py` (requires Playwright and Chromium). The browser test creates an offline HTML fixture; no public network is required.

GitHub Actions deploys the exact website, including `try/`. No `dist/` or remote package registry is involved.

## Site truth and measurements

FlameWM's ~17 MB is a **preliminary internally reported process RSS**, not independently reproduced. Competitor figures are **whole-system** idle values from a published Ubuntu 26.04 comparison (IceWM comes from another Q4OS test). The figures appear on one visual axis for convenience, but are not directly comparable benchmarks because the measurement scopes differ.

FlameWM is an independent Rust desktop/window manager **under active development**; the `/try/` path is a browser UI prototype, not a native Linux distribution. Current marketing copy does not assert that FlameWM is the objectively lightest desktop in the world.

## Assets and reuse

The landing page includes a compact “Made in Argentina 🇦🇷” signature. The RAM comparison uses one nine-column chart: FlameWM (reported window-manager RSS), IceWM (Q4OS idle system) and seven desktop sessions (Ubuntu idle system). Each column states its measurement type.

The site uses the supplied FlameWM wordmark, real desktop screenshot and original wallpaper (with atmospheric overlays), plus available open-source desktop application artwork. The four remaining desktop emblems are clearly labelled *illustrative artwork*, not official brand logos. See `assets/de-logos/ASSET_SOURCES.md` for provenance.

Historical website files and Astro source were intentionally retired: the checked-in static root is the **only deployment authority**.
