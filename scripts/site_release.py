#!/usr/bin/env python3
"""Deterministic dependency-free Pages deployment, and explicit Astro-to-root sync.

The checked-in root website is the publishing authority. Astro is optional for editing.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'index.html', '404.html', 'CNAME', '.nojekyll', 'robots.txt',
    'sitemap.xml', 'site.webmanifest', 'favicon.ico',
    'favicon-16x16.png', 'favicon-32x32.png',
    'android-chrome-192x192.png', 'android-chrome-512x512.png',
    'apple-touch-icon.png',
)
DIRS = ('about', 'features', 'assets', 'try', 'docs')


def copy_site(source: Path, dest: Path) -> None:
    if source.resolve() == dest.resolve():
        raise ValueError('Source and destination cannot match')
    missing = [p for p in (*FILES, *DIRS) if not (source / p).exists()]
    if missing:
        raise FileNotFoundError(f'Missing site entries in {source}: {missing}')
    dest.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copy2(source / name, dest / name)
    for name in DIRS:
        if (dest/name).exists():
            shutil.rmtree(dest/name)
        shutil.copytree(source/name, dest/name, symlinks=False)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ('stage', 'sync'):
        sys.exit('Usage: python3 scripts/site_release.py stage|sync')
    if sys.argv[1] == 'stage':
        dest=ROOT/'.pages-output'
        if dest.exists():
            shutil.rmtree(dest)
        copy_site(ROOT, dest)
        print(f'Prepared published website: {dest}')
    else:
        # Only run this manually after a real `npm run build`. Do not build a
        # local visual fixture and mistake it for a compiler-verified build.
        source=ROOT/'dist'
        if not (source/'index.html').exists():
            sys.exit('dist/index.html does not exist; run npm run build first')
        copy_site(source, ROOT)
        print('Promoted Astro dist/ into the publishable repository root')


if __name__ == '__main__':
    main()
