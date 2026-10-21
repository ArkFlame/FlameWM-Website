# Website rebuild — October 21, 2026

Changed: all public marketing pages, responsive layout, hero, source/preview CTAs, RAM section, animations, web metadata, image gallery, benchmark artwork. Preserved: official custom domain, original interactive prototype, URLs, GitHub Pages root deployment. Removed: stale duplicate Astro/public source and package requirements.

Verification: `python3 tests/check_static.py .`, Playwright offline Chromium views at 1440, 768, 390 and 320px, no page JS errors/overflow, menu, lightbox, section-stage updates, logo decode, bars, reduced motion. GitHub deployment/live DNS were not performed from this sandbox.

## Premium visual pass — October 21, 2026

- Reworked atmospheric hero using the supplied FlameWM wallpaper and restrained environmental texture/grids, with no remote runtime asset dependencies.
- Added scroll-responsive hero depth and load-in typography, preserving prefers-reduced-motion behavior.
- Enhanced native capture presentation and details typography.
- Replaced generic Unicode feature marks with consistent inline vector iconography.
- Clarified RAM copy to distinguish a process-RSS observation from full-system idle desktop benchmarks, and corrected the comparison label.
- Removed stale Astro-era preview fixture test; checked-in HTML is the sole source of deployment.
- Asset limitation: upstream artwork exists for IceWM, Plasma, MATE and Xfce; remaining desktop badges are intentionally labelled illustrative rather than pretending to be project trademarks. External downloads were unavailable in this environment.

## Chart visibility, country mark and visual refinement — October 21, 2026

- Fixed the missing FlameWM entry by placing its real brand icon and ~17 MB **process RSS** estimate in a dedicated, always-visible left column next to the scrollable seven-desktop comparison.
- Made the measurement boundaries unambiguous: FlameWM is shown on a **separate visual scale**, while the seven other bars use whole-system Ubuntu idle figures. This is not a controlled like-for-like comparison.
- Added scroll-progress feedback, chart series headers, aligned names, more deliberate red/neutral tones, and responsive mobile treatment.
- Added a small **Made in Argentina 🇦🇷** hero signature and understated footer attribution.
- Polished screenshot hover lighting, section atmosphere, and benchmark focus without new JS dependencies or continuous animation. Respects `prefers-reduced-motion`.
- Added regression checks for the FlameWM column, alignment, asset decoding, and origin subtitle.

- The Argentina signature now uses a local, lightweight SVG flag to render reliably without platform emoji fonts.

## Unified RAM chart update (2026-10-21)

- Combined FlameWM, IceWM, and seven Linux desktop environments into one nine-column bar chart.
- Removed the separate FlameWM panel, IceWM callout, long methodology note, and the “DRAG OR SCROLL TO EXPLORE” text.
- Shortened landing-page and supporting-page copy.
- Kept measurement type on every bar. Detailed source context remains in RAM_BENCHMARK_SOURCES.md.
