# FlameWM Website — verification ledger

Date: 2026-10-16

## Completed

- Source migration: modular Astro layout, shared navigation/footer, landing, features, about, 404.
- Original `/try/` prototype copied intact from the uploaded website package.
- GitHub Pages custom domain `wm.arkflame.com` retained via `public/CNAME`.
- GitHub Actions builds a static `dist/` artifact and deploys it with `actions/deploy-pages`.
- `src/components/DesktopPreview.astro` is explicit **concept imagery**, not a production screenshot.
- Static fixture generator ran successfully (`python3 tests/preview_build.py`).
- Static links/routes/assets/sitemap gate passed (`python3 tests/check_static.py dist`).
- Chromium set-content rendering and mobile-menu smoke test passed (`python3 tests/browser_smoke.py`) at 1440x900 and 390x844; both had zero document horizontal overflow.
- The `dist/` folder in this archive is an **offline visual-test fixture**, not output from an installed Astro compiler.

## Remaining external gates

- `npm install && npm run build && npm run check:static` on a machine with access to the npm registry. Local npm registry DNS is blocked in the supplied sandbox; Astro build could not be executed here.
- GitHub Actions deployment verification after pushing to `ArkFlame/FlameWM-Website` and selecting GitHub Actions under Pages.
- Real screenshots/assets after the native FlameWM interface is approved; current concepts intentionally temporary.

Do not claim an Astro build or remote deployment has passed before these gates run. CI is designed to reject a failed build/test before publishing.
