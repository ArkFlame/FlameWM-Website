#!/usr/bin/env python3
"""Exercise the exact GitHub Pages output at a root and a project subpath."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '.pages-output' if (ROOT / '.pages-output/index.html').exists() else ROOT

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

routes = {
    '/': b'Everything you need.',
    '/features/': b'FlameWM',
    '/about/': b'FlameWM',
    '/try/': b'app.js',
    '/assets/css/site.css': b'.hero',
    '/assets/js/site.js': b'menu-trigger',
    '/assets/brand/flamewm-navbar.webp': b'RIFF',
    '/assets/brand/flamewm-real-screenshot-preview.webp': b'RIFF',
    '/assets/images/flamewm-wallpaper.webp': b'RIFF',
    '/CNAME': b'wm.arkflame.com',
    '/site-version.txt': b'2026-10-21-pages-paths-v1',
    '/sitemap.xml': b'wm.arkflame.com',
}

with TemporaryDirectory(prefix='flamewm-pages-http-') as tmp:
    sandbox = Path(tmp)
    (sandbox / 'FlameWM-Website').symlink_to(SITE, target_is_directory=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(sandbox)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        addr = f'http://127.0.0.1:{server.server_address[1]}'
        for path, prefix in ((SITE, '/'), (sandbox, '/FlameWM-Website/')):
            # First configuration serves site at /, second through /FlameWM-Website/.
            if prefix == '/':
                server.RequestHandlerClass = partial(Quiet, directory=str(SITE))
            else:
                server.RequestHandlerClass = partial(Quiet, directory=str(sandbox))
            for route, required in routes.items():
                with urlopen(addr + prefix.rstrip('/') + route, timeout=8) as response:
                    content = response.read()
                    assert response.status == 200 and required in content, (prefix, route)
                    if route == '/':
                        assert b'href="/assets/css' not in content, 'absolute CSS path'
                        assert b'src="/assets/js' not in content, 'absolute script path'
                print('PASS', prefix.rstrip('/') + route)
    finally:
        server.shutdown()
        thread.join(timeout=5)
print('PASS: project path and custom-domain root routes')
