"""Serve the exact published root and verify HTTP routes/assets without browser deps."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
try:
    base=f'http://127.0.0.1:{server.server_address[1]}'
    expected={
        '/':b'<main id="content">',
        '/features/':b'<main id="content">',
        '/about/':b'<main id="content">',
        '/try/':b'app.js',
        '/assets/css/site.css':b'.hero',
        '/assets/js/site.js':b'menu-trigger',
        '/assets/brand/flamewm-navbar.webp':b'RIFF',
        '/assets/brand/flamewm-real-screenshot-preview.webp':b'RIFF',
        '/CNAME':b'wm.arkflame.com',
        '/sitemap.xml':b'wm.arkflame.com',
    }
    for uri,needle in expected.items():
        with urlopen(base+uri,timeout=10) as response:
            assert response.status==200,(uri,response.status)
            data=response.read()
            assert needle in data,(uri,needle)
        print('PASS HTTP',uri)
finally:
    server.shutdown()
    thread.join(timeout=5)
print('PASS HTTP smoke suite')
