#!/usr/bin/env python3
"""Offline Chromium smoke checks; inspect rendered UI without network or localhost permissions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64
import mimetypes
import re

ROOT = Path(__file__).resolve().parents[1]
STYLE = (ROOT / 'assets/css/site.css').read_text()
JS = (ROOT / 'assets/js/site.js').read_text()
mimetypes.add_type('image/svg+xml', '.svg')


def fixture(route):
    html = (ROOT / route).read_text()
    html = re.sub(r'<script\b[^>]*src="/assets/js/site\.js"[^>]*></script>', '', html)
    html = re.sub(r'<link\b[^>]*href="/assets/css/site\.css"[^>]*>', '<style>' + STYLE + '</style>', html)

    def replace(match):
        path = ROOT / match.group(1).lstrip('/')
        assert path.is_file(), path
        content_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return 'src="data:' + content_type + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii') + '"'

    return re.sub(r'src="(/assets/[^"?]+)"', replace, html)


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        cases = [('index.html', 1440, 900), ('index.html', 768, 900), ('index.html', 390, 844), ('index.html', 320, 700),
                 ('features/index.html', 1440, 900), ('features/index.html', 390, 844),
                 ('about/index.html', 1440, 900), ('about/index.html', 390, 844), ('404.html', 390, 844)]
        for route, width, height in cases:
            page = browser.new_page(viewport={'width': width, 'height': height})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.set_content(fixture(route), wait_until='domcontentloaded')
            page.add_script_tag(content=JS)
            page.wait_for_timeout(90)
            assert page.locator('h1').count() == 1
            assert page.locator('main#content').count() == 1
            assert page.evaluate('document.documentElement.scrollWidth-innerWidth') <= 1, (route, width, 'overflow')
            assert not errors, (route, width, errors)
            if route == 'index.html':
                assert page.locator('.screen-shot img').evaluate('(img)=>img.complete && img.naturalWidth>0')
                assert page.locator('.bench-col').count() == 9
                assert page.locator('.bench-flame').count() == 0
                assert page.locator('.bench-col').first.locator('.bench-name strong').inner_text() == 'FlameWM'
                assert page.locator('.bench-col').nth(1).locator('.bench-name strong').inner_text() == 'IceWM'
                assert '~17' in page.locator('.bench-col').first.locator('.bench-number').inner_text()
                assert '288' in page.locator('.bench-col').nth(1).locator('.bench-number').inner_text()
                assert page.locator('.bench-col').first.get_attribute('data-scope') == 'Window manager'
                assert page.locator('.bench-col').nth(1).get_attribute('data-scope') == 'Q4OS'
                assert page.locator('.bench-col').nth(2).get_attribute('data-scope') == 'System idle'
                assert 'DRAG OR SCROLL TO EXPLORE' not in page.content()
                assert not page.locator('.method-note').count()
                assert page.locator('.origin-flag img').evaluate('(img)=>img.complete && img.naturalWidth>0')
                page.locator('.bench-col').first.locator('img').scroll_into_view_if_needed()
                page.wait_for_function('() => {const img=document.querySelector(".bench-col img");return img.complete && img.naturalWidth>0}',timeout=5000)
                assert page.locator('.bench-unified .bench-grid').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length==9')
                if width == 1440:
                    page.locator('#ram').scroll_into_view_if_needed()
                    page.wait_for_timeout(120)
                    assert 'RAM' in page.locator('#stage-title').inner_text()
                    assert page.locator('.bench-name img').evaluate_all('(images)=>images.every(img=>img.complete && img.naturalWidth>0)')
                    page.locator('.bench-scroll').evaluate('(e)=>{e.scrollLeft=200}')
                    assert page.locator('.bench-col').first.evaluate('(e)=>e.getBoundingClientRect().right<=innerWidth')
                    assert page.locator('#bench-progress-fill').evaluate('(e)=>parseFloat(getComputedStyle(e).width)>0')
                    page.locator('.screen-shot').scroll_into_view_if_needed()
                    page.locator('.screen-shot').click()
                    assert page.locator('#lightbox').is_visible()
                    page.keyboard.press('Escape')
                    assert not page.locator('#lightbox').is_visible()
                if width == 390:
                    page.locator('#menu-trigger').click()
                    assert page.locator('#mobile-nav').is_visible()
                    assert page.locator('#menu-trigger').get_attribute('aria-expanded') == 'true'
                    page.keyboard.press('Escape')
                    assert not page.locator('#mobile-nav').is_visible()
            print(f'PASS {route:24s} {width}x{height}', flush=True)
            page.close()
        page = browser.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        page.set_content(fixture('index.html'))
        page.add_script_tag(content=JS)
        assert page.evaluate('getComputedStyle(document.querySelector(".floating-next")).display') == 'none'
        assert page.locator('.feature-card').first.evaluate('(e)=>getComputedStyle(e).opacity') == '1'
        print('PASS reduced-motion fallback')
        browser.close()


if __name__ == '__main__':
    run()
