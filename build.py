"""Build the Carlisle Capital portal.

Reads portal.html (source with __LOGO__ / __MARK__ placeholders) and brand-mark.svg,
then writes:
  dist/carlisle-portal.html  the artifact page (no doc skeleton; the artifact host adds one)
  docs/index.html            the GitHub Pages page (full document)
  docs/data/brokerage.json   copy of data/brokerage.json
"""
import os, re, shutil, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'portal.html'), encoding='utf-8').read()
svg = open(os.path.join(ROOT, 'brand-mark.svg'), encoding='utf-8').read().strip()
uri = 'data:image/svg+xml,' + urllib.parse.quote(svg, safe='')
page = src.replace('__LOGO__', uri).replace('__MARK__', uri)

os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
open(os.path.join(ROOT, 'dist', 'carlisle-portal.html'), 'w', encoding='utf-8').write(page)

head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<link rel="icon" href="' + uri + '">'
        '<style>:root{color-scheme:dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif;background:#06070A}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')
os.makedirs(os.path.join(ROOT, 'docs', 'data'), exist_ok=True)
open(os.path.join(ROOT, 'docs', 'index.html'), 'w', encoding='utf-8').write(head + page + '</body></html>')
shutil.copy(os.path.join(ROOT, 'data', 'brokerage.json'), os.path.join(ROOT, 'docs', 'data', 'brokerage.json'))

m = re.search(r'<script>(.*)</script>', page, re.S)
os.makedirs('/tmp/claude-0/carlisle', exist_ok=True)
open('/tmp/claude-0/carlisle/page.js', 'w', encoding='utf-8').write(m.group(1))
print('built', len(page), 'bytes')
