"""Prepare a static course for GitHub Pages or other static hosting."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile,html
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description='Build hosted decks and chapter downloads from the portable course.')
p.add_argument('--portable',default='out/portable');p.add_argument('--output',default='out/pages');a=p.parse_args()
P=(R/a.portable).resolve();D=(R/a.output).resolve()
if not (P/'index.html').is_file():raise SystemExit('First run: python3 build.py --portable --output out/portable')
for folder in ['chapters','downloads','assets/fonts']:(D/folder).mkdir(parents=True,exist_ok=True)
C=json.loads((R/'course.json').read_text())
media_sha={x['id']:x['sha256'][:12]for x in json.loads((R/'audio/manifest.json').read_text())['clips']}
(D/'audio/clips').mkdir(parents=True,exist_ok=True)
for p in (R/'audio/clips').glob('*.m4a'):shutil.copy(p,D/'audio/clips'/p.name)

def hosted(src,dst,prefix):
 s=src.read_text();start=s.index('const RECORDED_AUDIO=')+len('const RECORDED_AUDIO=');audio,end=json.JSONDecoder().raw_decode(s[start:]);mapping={k:prefix+'audio/clips/'+k+'.m4a?v='+media_sha[k]for k in audio}
 s=s[:start]+json.dumps(mapping)+s[start+end:]
 s=s.replace('<button class="small print-btn" id="printButton">','<a class="button small" href="'+prefix+'downloads.html">Downloads</a><button class="small print-btn" id="printButton">')
 s=s.replace('href="study-guide.html"','href="'+prefix+'study-guide.html"').replace('href="study-guide.pdf"','href="'+prefix+'study-guide.pdf"')
 s=s.replace('The recordings are included in this deck and work offline.','The recordings load when you press Play narration. Download a chapter to use it offline.')
 s=s.replace('The deck embeds prerecorded Kokoro','The course plays prerecorded Kokoro')
 s=s.replace('Quizzes and embedded narration work offline. External reading requires a connection.','This hosted course needs a connection for audio. The chapter downloads include audio for offline use.')
 dst.write_text(s)
hosted(P/'index.html',D/'index.html','./')
shutil.copy(P/'study-guide.html',D/'study-guide.html')
for name in ['FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt']:shutil.copy(P/name,D/name)
shutil.copytree(P/'licenses',D/'licenses',dirs_exist_ok=True)
shutil.copy(P/'assets/fonts/manifest.json',D/'assets/fonts/manifest.json')
shutil.copy(P/'study-guide.pdf',D/'study-guide.pdf')
shutil.copy(P/'study-guide.pdf',D/'downloads/study-guide.pdf')
rows=[]
for c in C:
 n=c['number'];slug=f'chapter-{n:02d}';hosted(P/'chapters'/f'{slug}.html',D/'chapters'/f'{slug}.html','../')
 archive=D/'downloads'/f'{slug}.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.write(P/'chapters'/f'{slug}.html',f'{slug}.html')
  z.write(R/'chapters'/f'{slug}.pdf',f'{slug}.pdf')
  z.write(R/'audio/chapters'/f'{slug}.m4a',f'{slug}.m4a')
  z.write(R/'FONT-LICENSE.txt','FONT-LICENSE.txt')
  z.write(R/'THIRD-PARTY-NOTICES.txt','THIRD-PARTY-NOTICES.txt')
  z.write(R/'assets/fonts/manifest.json','assets/fonts/manifest.json')
  for license_file in (R/'licenses').glob('*.txt'):z.write(license_file,'licenses/'+license_file.name)
  z.write(P/'study-guide.pdf','study-guide.pdf')
  z.writestr('START-HERE.txt',f"COMMON GROUND — CHAPTER {n}: {c['title']}\n\nOpen {slug}.html in a browser and press Play narration. Recorded Kokoro af_heart audio is embedded for offline use. {slug}.m4a is the continuous audio track. {slug}.pdf is the static deck. study-guide.pdf contains the evidence notes and optional written final case; this companion has no recorded narration.\n\nExplore social psychology through fictional café stories, decisions, recall, and field practice. Asset credits and licenses are in FONT-LICENSE.txt, THIRD-PARTY-NOTICES.txt, and licenses/.\n")
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()[:12]
 size=archive.stat().st_size/2**20
 assert size<24,(slug,size)
 rows.append(f'<li><div><span class="num">{n:02d}</span><div><h2>{html.escape(c["title"])}</h2><p>{html.escape(c["topic"])}</p></div></div><a href="downloads/{slug}.zip?v={digest}" download>Download chapter <span>({size:.1f} MB)</span></a></li>')
shutil.copy(R/'common-ground-slides.pdf',D/'downloads/all-slides.pdf')
(D/'downloads.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Download chapters — Common Ground</title><style>body{margin:0;background:#f2f6fc;color:#152f52;font:18px/1.5 system-ui,sans-serif}main{max-width:940px;padding:35px 22px 60px;margin:auto}h1{font:46px/1.15 Georgia,serif;margin-top:35px}h2{font:24px/1.25 Georgia,serif;margin:0}a{color:#216b88;text-underline-offset:4px}p{color:#4c617b}ul{list-style:none;padding:0}li{padding:24px 0;border-top:1px solid #c5d3e5;display:flex;justify-content:space-between;align-items:center;gap:20px}li>div{display:flex;gap:20px;align-items:center}li p{font-size:15px;margin:6px 0 0}.num{color:#4c617b}li a{font-size:16px;white-space:nowrap}li a span{display:block;font-size:14px}a:focus-visible{outline:3px solid #a1486d;outline-offset:4px}@media(max-width:600px){h1{font-size:36px}li{align-items:flex-start;flex-direction:column}li a{margin-left:45px}li a span{display:inline}}</style><main><a href="./">Back to the course</a><h1>Take a chapter with you.</h1><p>Each ZIP includes a self-contained narrated deck, a continuous audio track, and an eight-slide PDF. Each package also includes the study companion: evidence notes and an optional written case with suggested reasoning and a rubric. The companion has no recorded narration. Download one chapter at a time for smaller files on your phone.</p><p>After downloading, open the ZIP in your Files app to extract it. Open the HTML deck in a browser, or play the M4A audio directly.</p><ul>'''+''.join(rows)+'''</ul><p><a href="downloads/all-slides.pdf" download>Download all 80 slides as a PDF</a></p><p><a href="downloads/study-guide.pdf" download>Download the study companion PDF</a> · <a href="study-guide.html">Read it online</a></p><p>The narrated course uses Kokoro af_heart at speed 1.0. Voice generation and automated checks are documented in the original course package.</p></main></html>''')
(D/'.nojekyll').write_text('')
for f in D.rglob('*'):
 if f.is_file():assert f.stat().st_size<25*2**20,(f,f.stat().st_size)
print('Hosted course prepared; every asset under 25 MiB.')
print('ZIP sizes:',[(p.name,round(p.stat().st_size/2**20,1))for p in sorted((D/'downloads').glob('*.zip'))])
