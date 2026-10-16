# FlameWM Website

A responsive marketing site for **FlameWM**, built with **Astro** and deployed as static HTML to **GitHub Pages**. Includes the original interactive desktop prototype at `/try/`.

- Canonical site: https://wm.arkflame.com
- Website source: https://github.com/ArkFlame/FlameWM-Website
- FlameWM source: https://github.com/ArkFlame/flamewm

## Local development

Requires Node.js 22.22+ (Node.js 24 recommended) and npm. Astro 7.3.8 is pinned. Build-time dependency: Astro; no frontend framework is shipped to the browser.

```sh
npm install
npm run dev
npm run build
npm run check:static
npm run preview
```

The build writes to `dist/`. Only `dist/` is deployed. Do not publish `src/` as the Pages branch source.

**Verification note:** This package includes a browser-tested offline static preview in `dist/`. The local sandbox cannot reach the npm registry (`EAI_AGAIN`), so the Astro compiler build could not run here. The GitHub Actions workflow runs `npm install`, `astro build` and the post-build static check in an environment with npm access. Do not report the GitHub deployment as verified until that workflow succeeds.

## Deploy to GitHub Pages

1. Replace the contents of the `FlameWM-Website` repository with this package, keeping `.github/workflows/pages.yml`.
2. Push to `main`.
3. Under **Settings → Pages → Build and deployment**, select **GitHub Actions**.
4. The workflow installs Astro, builds prerendered pages, checks output and publishes `dist/`.
5. Under **Settings → Pages → Custom domain**, set `wm.arkflame.com` and enable **Enforce HTTPS** after certificate issuance. `public/CNAME` already contains the domain.
6. DNS should contain a `wm` **CNAME** record pointing to the correct organization Pages host, typically `arkflame.github.io` (verify the actual organization Pages host before changing existing DNS). Do not overwrite working DNS unnecessarily.

### Testing at the default GitHub project URL instead

`astro.config.mjs` supports the `SITE_URL` and `BASE_PATH` environment variables:

```sh
SITE_URL=https://arkflame.github.io BASE_PATH=/FlameWM-Website/ npm run build
```

All Astro-generated links and CSS image paths use `import.meta.env.BASE_URL`. **A GitHub project URL cannot simultaneously use the existing `wm.arkflame.com` CNAME.** To deploy to the project URL rather than the custom domain, remove `public/CNAME`, set the two environment variables in the workflow build step, adjust `robots.txt`, `sitemap.xml`, and domain-specific metadata for the new host, then push.

### Jekyll / Astro decision

GitHub Pages can build Jekyll directly from a publishing branch; it does not automatically build Astro source from a branch. Astro generates plain HTML/CSS and static assets; GitHub Actions publishes its `dist/` artifact. Jekyll and a GitHub Pages Ruby theme are not needed. Do not enable a Jekyll theme for this Astro project.

## Content and assets

| Path | Role |
| --- | --- |
| `src/pages/index.astro` | Overview/landing |
| `src/pages/features.astro` | Product features and workflow |
| `src/pages/about.astro` | Background and product principles |
| `src/layouts/SiteLayout.astro` | Shared meta, navigation and footer |
| `src/components/DesktopPreview.astro` | **Illustrative concept**; replace with actual product screenshot when available |
| `src/styles/global.css` | Global design tokens, layout and responsiveness |
| `public/try/` | Existing interactive prototype, preserved verbatim |
| `public/assets/images/` | Legacy development screenshots and wallpaper used as placeholders |
| `public/CNAME` | Existing production domain |

**Reality / release policy:** The preview is illustrative and `/try/` is a browser prototype, not a downloadable operating system. Do not label native features as released without release evidence. Current copy avoids numeric performance/availability claims.

**Screenshot replacement:** Replace `DesktopPreview.astro` contents with a responsive `<picture>`/`<img>` once approved real screenshots exist. Replace development reference images under `public/assets/images/`. Retain dimensions or CSS aspect ratios to avoid layout shift. New images should be optimized WebP/AVIF and include meaningful alternative text.

**Asset provenance:** FlameWM mark and development image files were carried forward from the provided website archive. The existing `/try/` subdirectory includes its own `LICENSE.txt` and bundled asset licensing notices. Do not remove those notices.

## Test scope

The static output validator (`tests/check_static.py`) verifies required routes, links, local file dependencies, CNAME, prototype assets and HTML-level invariants. Local browser checks should also cover mobile navigation, keyboard accessibility, viewport overflow and demo behavior. A successful CI build is required before claiming the GitHub Pages deployment is fully verified.


## 2026-10-16 homepage refresh

- Uses the provided **real desktop screenshot** in the home-page hero.
- Uses the provided **cropped FlameWM wordmark** in the navbar and footer.
- Adds a horizontal-scrollable vertical comparison chart with approximate ~17 MB WM RSS, six Ubuntu desktop results and IceWM from a separate published test; clearly labels incompatible measurement scopes.
- Includes icon provenance and benchmark limitations in `docs/RAM_BENCHMARK_SOURCES.md`.
- Original `/try/` contents preserved.
- Browser screenshots are visual-fixture outputs, not an Astro compiler build; `npm run build` remains the publishing authority in GitHub Actions.
