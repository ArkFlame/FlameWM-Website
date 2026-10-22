#!/usr/bin/env python3
"""Validate the checked-in GitHub Pages site and its exact staging artifact."""
import html.parser
import pathlib
import posixpath
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
required = (
    '.nojekyll', 'site-version.txt', 'index.html', 'features/index.html', 'about/index.html',
    '404.html', 'try/index.html', 'try/app.js', 'try/styles.css',
    'assets/js/site.js', 'assets/css/site.css',
    'assets/brand/argentina-flag.svg', 'assets/brand/flamewm-mark.svg',
    'assets/brand/flamewm-navbar.webp',
    'assets/brand/flamewm-real-screenshot-preview.webp',
    'docs/RAM_BENCHMARK_SOURCES.md', 'CNAME', 'sitemap.xml', 'robots.txt',
)
errors = [f'Missing: {p}' for p in required if not (root / p).is_file()]


class Scan(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.title = False
        self.main = False
        self.imgalt = True

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.title = True
        if tag == 'main' and attrs.get('id') == 'content':
            self.main = True
        if tag == 'img' and 'alt' not in attrs:
            self.imgalt = False
        for attr in ('src', 'href', 'data-image'):
            if attr in attrs:
                self.links.append((attr, attrs[attr]))


def check_link(page, attr, url):
    if not url or url.startswith(('#', 'mailto:', 'tel:', 'data:')):
        return
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return
    if url.startswith('/'):
        errors.append(f'{page}: root-absolute {attr} {url} breaks project Pages URLs')
        return
    rel = urllib.parse.unquote(parsed.path)
    if not rel:  # local-page fragment only
        return
    from_folder = posixpath.dirname(page)
    resolved = posixpath.normpath(posixpath.join(from_folder, rel))
    if resolved == '..' or resolved.startswith('../'):
        errors.append(f'{page}: link escapes website root: {url}')
        return
    if rel.endswith('/') or resolved == '.':
        resolved = posixpath.join(resolved, 'index.html')
    if not (root / resolved).is_file():
        errors.append(f'{page}: broken {attr}: {url} → {resolved}')


for page in ('index.html', 'features/index.html', 'about/index.html', '404.html'):
    f = root / page
    if not f.is_file():
        continue
    parser = Scan()
    parser.feed(f.read_text(encoding='utf-8'))
    if not parser.title:
        errors.append(f'{page}: no title')
    if not parser.main:
        errors.append(f'{page}: no #content')
    if not parser.imgalt:
        errors.append(f'{page}: image without alt')
    for attr, url in parser.links:
        check_link(page, attr, url)

css = root / 'assets/css/site.css'
if css.is_file():
    for match in re.finditer(r'url\(\s*[\"\']?(/(?!/)[^\"\')]+)', css.read_text()):
        errors.append(f'CSS root-absolute URL: {match.group(1)}')
for page in ('index.html', 'features/index.html', 'about/index.html', '404.html'):
    if (root / page).is_file() and not re.search(r'assets/css/site\.css', (root / page).read_text()):
        errors.append(f'{page}: missing stylesheet')
if (root / 'site-version.txt').is_file():
    release = (root / 'site-version.txt').read_text().strip()
    for page in ('index.html','features/index.html','about/index.html','404.html'):
        if (root / page).is_file() and f'content="{release}"' not in (root / page).read_text():
            errors.append(f'{page}: unexpected site revision')
if (root / 'index.html').is_file() and '# FlameWM Website' in (root / 'index.html').read_text():
    errors.append('README is the homepage instead of HTML')
try:
    ET.parse(root / 'sitemap.xml')
except Exception as exc:
    errors.append(f'Invalid sitemap: {exc}')
if (root / 'CNAME').is_file() and (root / 'CNAME').read_text().strip() != 'wm.arkflame.com':
    errors.append('Unexpected CNAME')
print(f'Checked {len(required)} required paths, page links, CSS URLs and sitemap')
for message in errors:
    print('FAIL:', message)
if errors:
    sys.exit(1)
print('PASS: static site works with / and /FlameWM-Website/ prefixes')
