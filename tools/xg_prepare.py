#!/usr/bin/env python3
"""
xgassman.com page fixer.

Makes sure every game listed in site.json has:
  - the Google Analytics tag
  - its favicon
  - a "Name · xgassman" tab title
  - a description and link-preview (Open Graph) tags
  - the "← xgassman." back link

It also catches a new version of a game saved under one of the OLD file
names (for example hotdog_drop.html): the new version is moved to the real
file and the old name is turned back into a redirect.

Usage (from the site folder):
  python3 tools/xg_prepare.py           fix everything, list what changed
  python3 tools/xg_prepare.py --check   only report, change nothing

The git pre-commit hook runs this automatically.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = '--check' in sys.argv
HOOK = '--hook' in sys.argv          # used by the git hook: print changed paths only

def esc(t):
    return t.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

def ga_block(tag):
    return ('<!-- Google tag (gtag.js) -->\n'
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script>\n'
            '<script>\n'
            '  window.dataLayer = window.dataLayer || [];\n'
            '  function gtag(){dataLayer.push(arguments);}\n'
            "  gtag('js', new Date());\n\n"
            f"  gtag('config', '{tag}');\n"
            '</script>\n')

BACK = '''<!-- xgassman back link -->
<a id="xg-back" href="/" title="More projects at xgassman.com">← xgassman<span style="color:#6f8259">.</span></a>
<style>
#xg-back{all:initial;position:fixed!important;left:12px;bottom:12px;z-index:2147483000!important;
  font:500 12px/1 Arial,Helvetica,sans-serif;letter-spacing:-.2px;color:#eeeeea;cursor:pointer;
  background:rgba(25,26,24,.78);padding:7px 11px;border-radius:999px;
  box-shadow:0 1px 4px rgba(0,0,0,.35);opacity:.8;transition:opacity .15s}
#xg-back:hover,#xg-back:focus-visible{opacity:1}
#xg-back:focus-visible{outline:2px solid #6f8259;outline-offset:2px}
@media print{#xg-back{display:none}}
</style>
'''

def redirect_page(url, icon):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/png" href="/favicons/{icon}.png">
<title>Moved · xgassman</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://xgassman.com/{url}">
<meta http-equiv="refresh" content="0; url=/{url}">
<script>location.replace('/{url}' + location.search + location.hash);</script>
</head>
<body style="background:#191a18;color:#eeeeea;font-family:Arial,Helvetica,sans-serif;padding:40px">
<p>This page has moved to <a style="color:#eeeeea" href="/{url}">xgassman.com/{url}</a>.</p>
</body>
</html>
'''

def fix_page(s, page, cfg):
    tag, site = cfg['google_tag'], cfg['site']
    # 1. strip everything this script manages, so it can be re-added cleanly
    s = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[A-Z0-9-]+"></script>\s*<script>.*?</script>\s*', '', s, flags=re.S)
    # any stray pieces of an old or partial Google tag
    s = re.sub(r'[ \t]*<!-- Google tag \(gtag\.js\) -->[ \t]*\n?', '', s)
    s = re.sub(r'[ \t]*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"></script>[ \t]*\n?', '', s)
    s = re.sub(r'[ \t]*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];[^<]*?gtag\(\'config\',[^<]*?</script>[ \t]*\n?', '', s, flags=re.S)
    s = re.sub(r'[ \t]*<link\s+rel="(?:shortcut )?(?:icon|apple-touch-icon)"[^>]*>\n?', '', s)
    s = re.sub(r'[ \t]*<meta\s+(?:name="description"|property="og:[^"]*"|name="twitter:[^"]*")[^>]*>\n?', '', s)
    s = re.sub(r'<!-- xgassman back link -->\s*<a id="xg-back".*?</style>\s*', '', s, flags=re.S)

    # 2. Google tag + favicon right after <head>
    m = re.search(r'<head[^>]*>', s, flags=re.I)
    if not m:
        raise ValueError('no <head> tag')
    i = m.end()
    if s[i:i + 1] == '\n':
        i += 1
    else:
        s = s[:i] + '\n' + s[i:]
        i += 1
    icon = page['icon']
    s = s[:i] + ga_block(tag) + (f'<link rel="icon" type="image/png" href="/favicons/{icon}.png">\n'
                                 f'<link rel="apple-touch-icon" href="/favicons/{icon}-touch.png">\n') + s[i:]

    # 3. title + description + preview tags
    name, desc = page['name'], page['description']
    meta = (f'<title>{esc(name)} · xgassman</title>\n'
            f'<meta name="description" content="{esc(desc)}">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="xgassman">\n'
            f'<meta property="og:title" content="{esc(name)}">\n'
            f'<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{site}/{page["url"]}">\n'
            f'<meta property="og:image" content="{site}/og/{page["card"]}.png">\n'
            '<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">')
    if re.search(r'<title>.*?</title>', s, flags=re.S | re.I):
        s = re.sub(r'<title>.*?</title>', lambda _: meta, s, count=1, flags=re.S | re.I)
    else:
        k = s.lower().index('</head>')
        s = s[:k] + meta + '\n' + s[k:]

    # 4. back link just before </body>
    j = s.lower().rfind('</body>')
    if j < 0:
        s = s + BACK
    else:
        s = s[:j] + BACK + s[j:]
    return s

def main():
    os.chdir(ROOT)
    cfg = json.load(open('site.json', encoding='utf-8'))
    pages = {p['file']: p for p in cfg['pages']}
    by_url = {p['url']: p for p in cfg['pages']}
    changed, notes, problems = [], [], []

    def write(path, text):
        if CHECK:
            changed.append(path)
            return
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        changed.append(path)

    # A. new versions saved under an old (redirect) file name
    for old, url in cfg.get('redirects', {}).items():
        if not os.path.exists(old):
            continue
        s = open(old, encoding='utf-8').read()
        if 'location.replace(' in s and len(s) < 4000:
            continue  # still a proper redirect
        page = by_url.get(url)
        if not page:
            problems.append(f'{old}: redirects to "{url}", which is not in site.json')
            continue
        notes.append(f'{old} had a new version of {page["name"]}: moved it to {page["file"]} '
                     f'and turned {old} back into a redirect')
        write(page['file'], s)
        write(old, redirect_page(url, page['icon']))

    # B. every game page gets its tags
    for f, page in pages.items():
        if not os.path.exists(f):
            problems.append(f'{f} is listed in site.json but the file is missing')
            continue
        src = open(f, encoding='utf-8').read() if not (CHECK and f in changed) else None
        if src is None:
            continue
        try:
            out = fix_page(src, page, cfg)
        except ValueError as e:
            problems.append(f'{f}: {e}')
            continue
        if out != src:
            if f not in changed:
                notes.append(f'{f}: added missing Google tag / favicon / title / preview / back link')
            write(f, out)

    # C. pages nobody has told us about yet
    known = set(pages) | set(cfg.get('redirects', {})) | set(cfg.get('ignore', []))
    for f in sorted(os.listdir('.')):
        if f.endswith('.html') and f not in known:
            problems.append(f'{f} is not in site.json yet (new game? add it to site.json, '
                            'or to "ignore" if it should stay off the site)')

    changed = sorted(set(changed))
    if HOOK:
        for c in changed:
            print(c)
        for n in notes:
            print('xgassman: ' + n, file=sys.stderr)
        for p in problems:
            print('xgassman: note: ' + p, file=sys.stderr)
        return 0
    for n in notes:
        print(('would fix: ' if CHECK else 'fixed: ') + n)
    for p in problems:
        print('note: ' + p)
    if not notes and not problems:
        print('All pages have their Google tag, favicon, title, preview card and back link.')
    return 1 if (CHECK and changed) else 0

if __name__ == '__main__':
    sys.exit(main())
