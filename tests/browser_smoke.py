"""Local Chromium smoke tests without external networking.

When npm is unavailable, preview_build.py generates the static fixture. These
checks verify actual browser layout/interactions, not an Astro compile.
"""
from pathlib import Path
import base64
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
OUT = ROOT / 'screenshots'
OUT.mkdir(exist_ok=True)


def uri(path):
    path = DIST / path.lstrip('/')
    types = {'.webp': 'image/webp', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon'}
    return f"data:{types[path.suffix]};base64,{base64.b64encode(path.read_bytes()).decode()}"


def html_fixture(route):
    source = (DIST / route).read_text()
    style = (DIST / 'assets/css/site.css').read_text()
    style = re.sub(r'url\([\'\"]?(/assets/[^\'\")]+)[\'\"]?\)', lambda m: f'url("{uri(m[1])}")', style)
    source = re.sub(r'<link[^>]*rel="stylesheet"[^>]*>', '', source)
    source = re.sub(r'<script src="/assets/js/site.js"[^>]*></script>', '', source)
    source = re.sub(r'src="(/assets/[^\"]+)"', lambda m: f'src="{uri(m[1])}"', source)
    return source.replace('</head>', '<style>' + style + '</style></head>')


with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
    cases = [
        ('index.html', 'home', 1440, 900),
        ('index.html', 'tablet', 768, 900),
        ('index.html', 'mobile', 390, 844),
        ('index.html', 'small-mobile', 320, 700),
        ('features/index.html', 'features-mobile', 390, 844),
        ('features/index.html', 'features-desktop', 1440, 900),
        ('about/index.html', 'about-mobile', 390, 844),
        ('about/index.html', 'about-desktop', 1440, 900),
        ('404.html', 'not-found', 390, 844),
    ]
    for route, name, width, height in cases:
        page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(html_fixture(route), wait_until='domcontentloaded')
        page.add_script_tag(content=(DIST / 'assets/js/site.js').read_text())
        page.wait_for_timeout(180)
        overflow = page.evaluate('document.documentElement.scrollWidth - innerWidth')
        assert overflow <= 1, (name, 'horizontal overflow', overflow)
        assert page.locator('h1').count() == 1, (name, 'missing or duplicate H1')
        assert page.locator('main#content').count() == 1, (name, 'missing main')
        assert not errors, (name, errors)
        if name in ('home', 'mobile'):
            page.screenshot(path=str(OUT / f'{name}.png'), full_page=False)
        if name == 'mobile':
            toggle = page.locator('[data-menu-toggle]')
            menu = page.locator('[data-mobile-menu]')
            assert not menu.is_visible()
            toggle.click()
            assert menu.is_visible()
            assert toggle.get_attribute('aria-expanded') == 'true'
            page.keyboard.press('Escape')
            assert not menu.is_visible()
            assert toggle.get_attribute('aria-expanded') == 'false'
        if name == 'home':
            page.locator('.preview-image').scroll_into_view_if_needed()
            page.wait_for_timeout(150)
            images = page.locator('.preview-image img')
            assert images.count() == 1
            assert images.evaluate('(img) => img.complete && img.naturalWidth > 0'), 'preview image missing'
            page.evaluate("document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('in-view'))")
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(800)
            page.screenshot(path=str(OUT / 'home-full.png'), full_page=True)
        print(f'PASS {name:16s} viewport={width}x{height} overflow={overflow}', flush=True)
        page.close()

    # The new assets and actual benchmark values must be visible in browser.
    home = browser.new_page(viewport={'width': 1440, 'height': 900})
    home.set_content(html_fixture('index.html'))
    assert home.locator('.brand-wordmark').count() == 2
    assert home.locator('.brand-wordmark').first.evaluate('(img) => img.complete && img.naturalWidth > 0')
    assert home.locator('.hero-real-screenshot').evaluate('(img) => img.complete && img.naturalWidth > 0')
    assert home.locator('#benchmarks .ram-column').count() == 8
    assert 'Different measurement scopes.' in home.locator('#benchmarks').inner_text()
    home.locator('#benchmarks').scroll_into_view_if_needed()
    home.screenshot(path=str(OUT/'ram-comparison-desktop.png'), full_page=False)
    home.close()
    mobile = browser.new_page(viewport={'width':390,'height':844})
    mobile.set_content(html_fixture('index.html'))
    chart = mobile.locator('#benchmarks .ram-chart-scroll')
    assert chart.evaluate('(el) => el.scrollWidth > el.clientWidth'), 'mobile chart should scroll'
    chart.scroll_into_view_if_needed()
    mobile.screenshot(path=str(OUT/'ram-comparison-mobile.png'), full_page=False)
    mobile.close()
    print('PASS benchmark data, real screenshot, responsive scroll, wordmark assets', flush=True)

    # Existing interactive prototype must still initialize and show its launcher.
    demo = browser.new_page(viewport={'width': 1200, 'height': 760})
    failures = []
    demo.on('pageerror', lambda e: failures.append(str(e)))
    d = DIST / 'try'
    doc = (d / 'index.html').read_text().replace('<link rel="stylesheet" href="styles.css" />', '<style>' + (d / 'styles.css').read_text() + '</style>').replace('<script src="app.js"></script>', '')
    demo.set_content(doc, wait_until='domcontentloaded')
    demo.add_script_tag(content=(d / 'app.js').read_text())
    assert demo.locator('#task-entries button').count() >= 1
    demo.locator('#start-button').click()
    assert 'hidden' not in (demo.locator('#start-menu').get_attribute('class') or '').split()
    demo.locator('#start-button').click()
    assert 'hidden' in (demo.locator('#start-menu').get_attribute('class') or '').split()
    assert not failures, failures
    print('PASS interactive /try/ app initialises and launcher toggles', flush=True)
    demo.close()
    browser.close()
print('PASS browser smoke suite')
