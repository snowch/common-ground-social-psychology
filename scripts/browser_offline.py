"""Add explicit, versioned whole-course browser saving to the hosted build."""
import hashlib
import json
import re
import shutil


def build_browser_offline(root, destination, font_css, notices):
    logo = re.search(r'<svg viewBox="0 0 40 40".*?</svg>',
                     (destination / 'downloads.html').read_text()).group()
    page = (root / 'web/offline.html').read_text()
    for key, value in [('__FONTS__', font_css), ('__NOTICES__', notices), ('__LOGO__', logo)]:
        page = page.replace(key, value)
    (destination / 'offline.html').write_text(page)
    shutil.copy(root / 'web/offline-client.js', destination / 'offline-client.js')
    # Registration is lightweight: no course files are saved until the learner
    # chooses Make available offline. Companion pages can be reopened directly.
    for path in destination.rglob('*.html'):
        if path.name == 'offline.html':
            continue
        prefix = '../' if path.parent.name == 'chapters' else './'
        register = ('<script>if("serviceWorker" in navigator){'
                    'navigator.serviceWorker.register("' + prefix + 'sw.js",'
                    '{scope:"' + prefix + '",updateViaCache:"none"}).catch(()=>{});}'
                    '</script>')
        text = path.read_text()
        closing = '</body>' if '</body>' in text else '</html>'
        path.write_text(text.replace(closing, register + closing))
    # ZIP archives and continuous tracks duplicate course recordings. Retain
    # these as optional downloads rather than spending device storage twice.
    paths = [*destination.glob('*.html'), *destination.glob('*.pdf'),
             destination / 'offline-client.js',
             *destination.glob('chapters/*.html'),
             *destination.glob('audio/clips/*.m4a'),
             *destination.glob('downloads/*.pdf'),
             destination / 'LICENSE', destination / 'FONT-LICENSE.txt',
             destination / 'THIRD-PARTY-NOTICES.txt',
             destination / 'assets/fonts/manifest.json',
             *destination.glob('licenses/*.txt')]
    assets = []
    for path in sorted(paths):
        data = path.read_bytes()
        relative = path.relative_to(destination).as_posix()
        digest = hashlib.sha256(data).hexdigest()
        if relative.startswith('audio/clips/'):
            relative += '?v=' + digest[:12]
        assets.append({'url': relative, 'bytes': len(data), 'sha256': digest})
    version = hashlib.sha256(json.dumps(assets, sort_keys=True).encode()).hexdigest()[:16]
    worker = (root / 'web/offline-worker.js').read_text()
    worker = worker.replace('__OFFLINE_RELEASE__', json.dumps(version))
    worker = worker.replace('__OFFLINE_ASSETS__', json.dumps(assets, separators=(',', ':')))
    (destination / 'sw.js').write_text(worker)
    (destination / 'offline-manifest.json').write_text(json.dumps({
        'version': version, 'bytes': sum(a['bytes'] for a in assets), 'assets': assets
    }, indent=2) + '\n')
    print(f'Browser offline course: {len(assets)} files, {sum(a["bytes"] for a in assets)/10**6:.1f} MB; release {version}')
