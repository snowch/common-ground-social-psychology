"""Check hosted course paths, recordings, licenses, and offline chapter packages."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,hashlib,json,re,zipfile
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='out/pages');a=p.parse_args();D=(R/a.output).resolve()
manifest=json.loads((R/'audio/manifest.json').read_text());clips={x['id']:x for x in manifest['clips']}
chapter_clip_counts={f"chapter-{c['number']:02d}":sum(x['id'].startswith(f"c{c['number']:02d}") for x in manifest['clips']) for c in json.loads((R/'course.json').read_text())}
font_notice=(R/'FONT-LICENSE.txt').read_text();asset_notice=(R/'THIRD-PARTY-NOTICES.txt').read_text()
files=[D/'index.html',*sorted((D/'chapters').glob('*.html')),D/'study-guide.html',D/'visual-guide.html',D/'downloads.html'];assert len(files)==14
mappings=0;links=0
for file in files:
 s=file.read_text();assert not re.search(r'__[A-Z_]+__',s),file
 assert font_notice in s and asset_notice in s,file
 if 'const RECORDED_AUDIO='in s:
  start=s.index('const RECORDED_AUDIO=')+len('const RECORDED_AUDIO=');audio,_=json.JSONDecoder().raw_decode(s[start:]);assert len(audio)==(len(clips) if file.name=='index.html'else chapter_clip_counts[file.stem]),file
  for id,url in audio.items():
   parts=urlsplit(url);assert not parts.scheme and not parts.path.startswith('/'),(file,url)
   recording=(file.parent/unquote(parts.path)).resolve();assert recording.is_relative_to(D)and recording.is_file(),recording
   assert hashlib.sha256(recording.read_bytes()).hexdigest()==clips[id]['sha256'],id
   assert '?v='+clips[id]['sha256'][:12]in url,id
  mappings+=len(audio)
 for url in re.findall(r'href="([^"]+)"',s):
  if '${'in url or url.startswith('#'):continue
  parts=urlsplit(url)
  if parts.scheme or parts.netloc:continue
  assert not parts.path.startswith('/'),(file,url)
  target=(file.parent/unquote(parts.path)).resolve();assert target.is_relative_to(D)and target.exists(),(file,url)
  links+=1
archives=sorted((D/'downloads').glob('*.zip'));assert len(archives)==10
for archive in archives:
 with zipfile.ZipFile(archive)as z:
  assert z.testzip()is None,archive
  assert z.read('FONT-LICENSE.txt').decode()==font_notice
  assert z.read('THIRD-PARTY-NOTICES.txt').decode()==asset_notice
  assert z.read('visual-guide.pdf')==(R/'visual-guide.pdf').read_bytes()
  visual_html=z.read('visual-guide.html').decode();assert font_notice in visual_html and asset_notice in visual_html
  assert 'href="'+archive.stem+'.html"' in visual_html
  s=z.read(archive.stem+'.html').decode();start=s.index('const RECORDED_AUDIO=')+len('const RECORDED_AUDIO=');audio,_=json.JSONDecoder().raw_decode(s[start:]);assert len(audio)==chapter_clip_counts[archive.stem] and all(url.startswith('data:audio/mp4;base64,')for url in audio.values()),archive
assert (D/'.nojekyll').exists()
assert not list(D.rglob('*.py'))and not(D/'production').exists()
size=sum(f.stat().st_size for f in D.rglob('*')if f.is_file());assert size<1024**3,size
print(json.dumps({'html_files':len(files),'relative_audio_paths_checked':mappings,'local_links_checked':links,'offline_chapter_archives':len(archives),'font_and_asset_notices':'passed','total_mib':round(size/2**20,1)},indent=2))
