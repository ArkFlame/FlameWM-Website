#!/usr/bin/env python3
"""Offline Chromium behavior/layout checks. HTTP path checks are in http_smoke.py."""
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
import base64
import mimetypes
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '.pages-output' if (ROOT / '.pages-output/index.html').exists() else ROOT
CSS = (SITE / 'assets/css/site.css').read_text()
JS = (SITE / 'assets/js/site.js').read_text()


def datauri(file):
    kind = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
    return 'data:' + kind + ';base64,' + base64.b64encode(file.read_bytes()).decode('ascii')


def fixture(page_name, prefix):
    page = SITE / page_name
    text = page.read_text()
    base_url = 'https://wm.arkflame.com' + prefix + (page.parent.name + '/' if page.parent != SITE else '')
    # Keep original relative hrefs; all images are inlined to exercise UI without web access.
    text = text.replace('<head>', '<head><base href="' + base_url + '">', 1)
    text = re.sub(r'<script\b[^>]*src=["\'][^"\']*assets/js/site\.js[^>]*></script>', '', text)
    text = re.sub(r'<link\b[^>]*href=["\'][^"\']*assets/css/site\.css[^>]*>', '', text)
    stylesheet = CSS.replace("url('../images/flamewm-wallpaper.webp')", "url('" + datauri(SITE / 'assets/images/flamewm-wallpaper.webp') + "')")
    text = text.replace('</head>', '<style>' + stylesheet + '</style></head>', 1)
    folder = page.parent

    def embed(m):
        attr, href = m.group(1), m.group(2)
        parsed = urlsplit(href)
        if parsed.scheme or not re.search(r'\.(webp|png|svg|jpe?g)$', parsed.path):
            return m.group(0)
        path = (folder / parsed.path).resolve()
        assert path.is_relative_to(SITE.resolve()) and path.is_file(), (page_name, href)
        return attr + '="' + datauri(path) + '"'

    text = re.sub(r'\b(src|data-image)="([^"]+)"', embed, text)
    return text.replace('loading="lazy"', 'loading="eager"')


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        for prefix in ('/', '/FlameWM-Website/'):
            for route in ('index.html','features/index.html','about/index.html','404.html'):
                for width, height in ((1440,900),(390,844),(320,700)):
                    page = browser.new_page(viewport={'width':width,'height':height})
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.set_content(fixture(route, prefix),wait_until='domcontentloaded')
                    page.add_script_tag(content=JS)
                    page.wait_for_timeout(60)
                    assert page.locator('main#content').count() == 1, (prefix, route)
                    assert page.evaluate('document.documentElement.scrollWidth-innerWidth') <= 2, (prefix, route, width, 'overflow')
                    assert page.locator('.site-header img').evaluate('(i)=>i.complete && i.naturalWidth>0'),(prefix,route,'logo')
                    expected_home = '/FlameWM-Website/' if prefix != '/' else '/'
                    assert page.locator('.site-header a.brand').evaluate('(e)=>new URL(e.getAttribute("href"),document.baseURI).pathname') == expected_home
                    if route == 'index.html':
                        assert page.locator('.bench-col').count()==9
                        assert page.locator('.bench-col').first.locator('.bench-name strong').inner_text()=='FlameWM'
                        assert page.locator('.bench-name img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
                        assert page.locator('.screen-shot img').evaluate('(i)=>i.complete && i.naturalWidth>0')
                        page.locator('#ram').scroll_into_view_if_needed()
                        page.wait_for_timeout(80)
                        assert 'RAM' in page.locator('#stage-title').inner_text()
                        if width == 390:
                            page.locator('#menu-trigger').click()
                            assert page.locator('#mobile-nav').is_visible()
                            page.keyboard.press('Escape')
                            assert not page.locator('#mobile-nav').is_visible()
                        if width == 1440:
                            page.locator('.screen-shot').scroll_into_view_if_needed()
                            page.locator('.screen-shot').click()
                            assert page.locator('#lightbox').is_visible()
                            assert page.locator('#lightbox-image').evaluate('(i)=>i.complete && i.naturalWidth>0')
                            page.keyboard.press('Escape')
                            assert not page.locator('#lightbox').is_visible()
                    assert not errors, (prefix, route, width, errors)
                    print('PASS', prefix, route, width, flush=True)
                    page.close()
        page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
        page.set_content(fixture('index.html','/'))
        page.add_script_tag(content=JS)
        assert page.evaluate('getComputedStyle(document.querySelector(".floating-next")).display') == 'none'
        assert page.locator('.feature-card').first.evaluate('(e)=>getComputedStyle(e).opacity') == '1'
        print('PASS reduced motion', flush=True)
        browser.close()

if __name__=='__main__':
    run()
