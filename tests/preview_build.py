"""Offline visual-test fixture from Astro templates. Not the production Astro build.

Used only when npm registry access is unavailable. CI deploys actual `astro build` output.
"""
from pathlib import Path
import re, shutil, html
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

def read(rel):
    text = (ROOT/rel).read_text()
    return re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)

def replace_urls(text):
    text = re.sub(r"\b(href|src)=\{(?:url|to)\('([^']*)'\)\}", lambda m: f'{m[1]}="/{m[2]}"', text)
    text = re.sub(r"\b(href|src)=\{`\$\{base\}([^`]*)`\}", lambda m: f'{m[1]}="/{m[2]}"', text)
    text = re.sub(r"\bhref=\{base\}", 'href="/"', text)
    text = text.replace(' is:inline','')
    return text

layout = read('src/layouts/SiteLayout.astro')
preview = read('src/components/DesktopPreview.astro')
preview = re.sub(r'<div class:list=\{.*?\} aria-label=', '<div class="desktop-preview" aria-label=', preview, count=1)
preview = preview.replace('style={`--preview-bg: url(\'${base}assets/images/flamewm-wallpaper.webp\')`}', 'style="--preview-bg:url(\'/assets/images/flamewm-wallpaper.webp\')"')
preview = preview.replace('src={`${base}assets/brand/flamewm-mark.svg`}', 'src="/assets/brand/flamewm-mark.svg"')

if DIST.exists(): shutil.rmtree(DIST)
shutil.copytree(ROOT/'public', DIST)
shutil.copytree(ROOT/'public/try', DIST/'try', dirs_exist_ok=True)
(DIST/'assets/css').mkdir(parents=True,exist_ok=True)
shutil.copy(ROOT/'src/styles/global.css', DIST/'assets/css/site.css')
for name,path in [('home','index.astro'),('features','features.astro'),('about','about.astro'),('404','404.astro')]:
    page = read('src/pages/'+path)
    page = re.sub(r'^<SiteLayout\s+.*?>', '', page, count=1, flags=re.S).strip()
    page = re.sub(r'</SiteLayout>\s*$', '', page)
    page = page.replace('<DesktopPreview />', preview).replace('<DesktopPreview compact={true} />',preview.replace('class="desktop-preview"','class="desktop-preview desktop-preview-compact"',1))
    page = replace_urls(page)
    site = layout.replace('<slot />',page)
    site = replace_urls(site)
    site = re.sub(r'aria-current=\{page === \'([^\']+)\' \? \'page\' : undefined\}',lambda m: 'aria-current="page"' if m[1]==name else '',site)
    site = site.replace('content={description}','content="An independent Rust desktop and window manager for Linux. Familiar by design and lightweight at heart."')
    site = site.replace('content={title}',f'content="FlameWM — {name}"')
    canonical = 'https://wm.arkflame.com/' + ({'home': '', 'features': 'features/', 'about': 'about/', '404': '404.html'}[name])
    site = site.replace('href={canonical}', f'href="{canonical}"').replace('content={canonical}', f'content="{canonical}"')
    site = site.replace('content={new URL(url(\'assets/images/flamewm-desktop.webp\'), Astro.site || Astro.url).toString()}', 'content="https://wm.arkflame.com/assets/images/flamewm-desktop.webp"')
    site = site.replace('<title>{title}</title>',f'<title>FlameWM — {name}</title>')
    site = site.replace('</head>', '<link rel="stylesheet" href="/assets/css/site.css" />\n</head>')
    site = site.replace('src={`${base}assets/brand/flamewm-mark.svg`}', 'src="/assets/brand/flamewm-mark.svg"')
    site = site.replace('src={`${base}assets/images/flamewm-settings.webp`}', 'src="/assets/images/flamewm-settings.webp"')
    site = site.replace('src={`${base}assets/images/flamewm-desktop.webp`}', 'src="/assets/images/flamewm-desktop.webp"')
    site = site.replace('&#123;<span>/</span>&#125;','{<span>/</span>}')
    site = re.sub(r'\b(href|src)=\{url\(\'([^\']+)\'\)\}',lambda m:f'{m[1]}="/{m[2]}"',site)
    out = {'home':DIST/'index.html','features':DIST/'features/index.html','about':DIST/'about/index.html','404':DIST/'404.html'}[name]
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(site)
    print('PREVIEW',out.relative_to(DIST),len(site))
print('Offline visual-test fixture generated. NOT an Astro compiler build.')
