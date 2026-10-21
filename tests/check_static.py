"""Static build checks for GitHub Pages outputs. Uses stdlib only."""
import sys, pathlib, re, html.parser, urllib.parse, xml.etree.ElementTree as ET
root = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
required = ('.nojekyll','index.html','features/index.html','about/index.html','404.html','try/index.html','try/app.js','try/styles.css','assets/js/site.js','assets/brand/argentina-flag.svg','assets/brand/flamewm-mark.svg','assets/brand/flamewm-navbar.webp','assets/brand/flamewm-real-screenshot-preview.webp','assets/css/site.css','docs/RAM_BENCHMARK_SOURCES.md','CNAME','sitemap.xml','robots.txt')
errors = [f'Missing required file: {p}' for p in required if not (root/p).is_file()]
base = '/'
class Scan(html.parser.HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.links=[];self.title=False;self.main=False;self.imgalt=True
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag == 'title': self.title=True
        if tag == 'main' and a.get('id') == 'content':self.main=True
        if tag=='img' and 'alt' not in a:self.imgalt=False
        for att in ('src','href'):
            if att in a:self.links.append((tag,att,a[att]))
for file in (root/'index.html', root/'features/index.html', root/'about/index.html', root/'404.html'):
    # Legacy demo has its own structure; don't apply marketing-page invariants to it.
    if file.relative_to(root).parts[0]=='try':continue
    scan=Scan(file);scan.feed(file.read_text())
    if not scan.title:errors.append(f'No title in {file}')
    if not scan.main:errors.append(f'No #content in {file}')
    if not scan.imgalt:errors.append(f'Image without alt in {file}')
    for tag,att,link in scan.links:
        if not link or link.startswith(('#','mailto:','tel:','data:')):continue
        dest=urllib.parse.urlparse(link)
        if dest.scheme in ('http','https'):continue
        if dest.scheme or link.startswith('//'):continue
        local=dest.path
        if not local:continue
        if local.startswith('/'):
            local=local.lstrip('/')
        else:local=str(file.parent.relative_to(root)/local)
        if local.endswith('/') or local=='':local+='index.html'
        if not (root/local).is_file():errors.append(f'Broken {att} in {file.relative_to(root)}: {link}')
if (root/'index.html').is_file() and '# FlameWM Website' in (root/'index.html').read_text():errors.append('README is being served as homepage')
try:ET.parse(root/'sitemap.xml')
except Exception as e:errors.append(f'Invalid sitemap: {e}')
if (root/'CNAME').is_file() and (root/'CNAME').read_text().strip()!='wm.arkflame.com':errors.append('Unexpected CNAME')
print(f'Checks: {len(required)} required files, {len(list(root.glob("**/*.html")))} HTML files, local links and sitemap')
for x in errors:print('FAIL:',x)
if errors:sys.exit(1)
print('PASS: static output checks')
