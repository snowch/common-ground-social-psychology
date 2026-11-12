"""Prepare a static course for GitHub Pages or other static hosting."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,zipfile,html
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
 s=s.replace('href="visual-guide.html"','href="'+prefix+'visual-guide.html"').replace('href="visual-guide.pdf"','href="'+prefix+'visual-guide.pdf"')
 s=s.replace('The recordings are included in this deck and work offline.','The recordings load when you press Play narration. Download a chapter to use it offline.')
 s=s.replace('The deck embeds prerecorded Kokoro','The course plays prerecorded Kokoro')
 s=s.replace('Quizzes and embedded narration work offline. External reading requires a connection.','This hosted course needs a connection for audio. The chapter downloads include audio for offline use.')
 dst.write_text(s)
hosted(P/'index.html',D/'index.html','./')
shutil.copy(P/'study-guide.html',D/'study-guide.html')
shutil.copy(P/'visual-guide.html',D/'visual-guide.html')
shutil.copy(P/'visual-guide.pdf',D/'visual-guide.pdf')
shutil.copy(P/'visual-guide.pdf',D/'downloads/visual-guide.pdf')
for name in ['LICENSE','FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt']:shutil.copy(P/name,D/name)
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
  z.write(R/'LICENSE','LICENSE')
  z.write(R/'FONT-LICENSE.txt','FONT-LICENSE.txt')
  z.write(R/'THIRD-PARTY-NOTICES.txt','THIRD-PARTY-NOTICES.txt')
  z.write(R/'assets/fonts/manifest.json','assets/fonts/manifest.json')
  for license_file in (R/'licenses').glob('*.txt'):z.write(license_file,'licenses/'+license_file.name)
  z.write(P/'study-guide.pdf','study-guide.pdf')
  z.write(P/'visual-guide.pdf','visual-guide.pdf')
  z.writestr('visual-guide.html',(P/'visual-guide.html').read_text().replace('href="index.html"',f'href="{slug}.html"'))
  z.writestr('START-HERE.txt',f"COMMON GROUND — CHAPTER {n}: {c['title']}\n\nOpen {slug}.html in a browser and press Play narration. Recorded Kokoro af_heart audio is embedded for offline use. {slug}.m4a is the continuous audio track. {slug}.pdf is the static deck. visual-guide.html and visual-guide.pdf collect all 48 teaching illustrations. study-guide.pdf contains the evidence notes and optional written final case; this companion has no recorded narration.\n\nExplore social psychology through fictional café stories, decisions, recall, and field practice. Asset credits and licenses are in FONT-LICENSE.txt, THIRD-PARTY-NOTICES.txt, and licenses/.\n")
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()[:12]
 size=archive.stat().st_size/2**20
 assert size<24,(slug,size)
 rows.append(f'<li><span class="download-num">{n:02d}</span><div><h2>{html.escape(c["title"])}</h2><p>{html.escape(c["topic"])}</p></div><a class="button" href="downloads/{slug}.zip?v={digest}" download aria-label="Download chapter {n}: {html.escape(c["title"],quote=True)}">Download chapter <span>{size:.1f} MB</span></a></li>')
shutil.copy(R/'common-ground-slides.pdf',D/'downloads/all-slides.pdf')
font_css='\n'.join(re.findall(r'@font-face\{[^}]+\}',(P/'index.html').read_text()))
notices=(R/'FONT-LICENSE.txt').read_text()+'\n'+(R/'THIRD-PARTY-NOTICES.txt').read_text()
(D/'downloads.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Download chapters — Common Ground</title><!--\n'''+notices+'\n--><style>'+font_css+'''
*{box-sizing:border-box}body{margin:0;background:#EDF3F8;color:#19394D;font:17px/1.7 CourseSans,Arial,sans-serif;-webkit-font-smoothing:antialiased}a{color:#216B88;text-underline-offset:4px}a:focus-visible{outline:3px solid #A1486D;outline-offset:4px}h1,h2,h3{font-family:CourseSerif,Georgia,serif;font-weight:400;line-height:1.3;margin-top:0}h1{font-size:clamp(36px,4.5vw,58px);letter-spacing:-1.7px;margin-bottom:23px}h2{font-size:23px;letter-spacing:-.4px;margin-bottom:7px}p{margin-top:0;color:#4B6172}.top{max-width:1440px;margin:auto;min-height:88px;padding:19px 4vw;display:flex;justify-content:space-between;align-items:center;gap:20px}.brand{font:22px/1.4 CourseSerif,Georgia,serif;letter-spacing:-.6px;color:#19394D;text-decoration:none;display:flex;align-items:center;gap:12px}.brand svg{width:36px;height:36px}.button{display:inline-flex;align-items:center;justify-content:center;gap:14px;border:1px solid #B9CDD9;border-radius:7px;min-height:44px;padding:10px 16px;text-decoration:none;font-size:14px;white-space:nowrap}.button:hover{background:#E0EBF3}.download-wrap{max-width:1260px;margin:auto;padding:32px 4vw 55px}.download-intro{display:grid;grid-template-columns:1.35fr 1fr;gap:70px;align-items:center;margin:15px 0 40px}.download-intro>div>p{max-width:520px;line-height:1.85;font-size:17px}.intro{font-size:14px!important;margin-bottom:18px!important;color:#315C74}.download-guide{padding:24px 27px;border-left:3px solid #D8AC5C;background:#E3EDF4}.download-guide h2{font:16px/1.5 CourseSans,Arial,sans-serif;font-weight:bold;margin-bottom:13px}.download-guide ol{padding-left:21px;margin:0}.download-guide li{padding-left:6px;font-size:14px;color:#4B6172;line-height:1.8;margin-bottom:9px}.download-guide li:last-child{margin-bottom:0}.download-list{padding:0;margin:0;list-style:none;border-top:1px solid #BCCFDB}.download-list>li{display:grid;grid-template-columns:40px minmax(0,1fr) auto;gap:23px;align-items:center;padding:26px 4px;border-bottom:1px solid #BCCFDB}.download-num{display:flex;align-items:center;justify-content:center;width:36px;height:36px;border:1px solid #BCCFDB;border-radius:50%;font-size:14px;color:#456378}.download-list p{font-size:14px;margin:0}.download-list .button{color:#fff;background:#19394D;border-color:#19394D;padding:11px 17px}.download-list .button:hover{background:#295269}.download-list .button span{font-size:12px;color:#D4E4EC;border-left:1px solid #7392A4;padding-left:13px}.pdf-downloads{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:40px;padding:35px 0}.pdf-downloads h2{font-size:22px}.pdf-downloads p{font-size:14px;max-width:430px}.pdf-downloads a{font-size:15px}.footer{font-size:12px;line-height:1.8;border-top:1px solid #CDD9E2;padding:22px 0 0;color:#4B6172}
@media(max-width:760px){.download-intro{gap:25px}.download-list>li{column-gap:15px}.download-list h2{font-size:21px}.download-list .button{gap:9px;padding:10px 12px;font-size:13px}.download-list .button span{padding-left:9px}.top{padding:18px 22px}.brand{font-size:20px}}
@media(max-width:600px){.top{flex-wrap:wrap;gap:15px;padding:19px 21px}.brand{font-size:19px;gap:9px}.brand svg{width:31px;height:31px}.top .button{font-size:12px;padding:8px 11px;min-height:38px}.download-wrap{padding:20px 22px 35px}.download-intro{grid-template-columns:1fr;gap:18px;margin-top:5px;margin-bottom:28px}h1{font-size:36px;line-height:1.25;letter-spacing:-1.2px;margin-bottom:20px}.download-intro>div>p{font-size:16px;line-height:1.85}.download-guide{padding:20px 21px}.download-list>li{grid-template-columns:33px minmax(0,1fr);gap:10px 13px;padding:24px 0}.download-num{width:31px;height:31px;align-self:start;margin-top:2px;font-size:13px}.download-list h2{font-size:21px;line-height:1.35}.download-list p{font-size:13px;line-height:1.6}.download-list .button{grid-column:2;justify-self:start;font-size:13px;margin-top:4px}.pdf-downloads{grid-template-columns:1fr;gap:25px;padding:31px 0}.pdf-downloads h2{font-size:22px}.footer{font-size:12px}}
@media print{.top{display:none}.download-wrap{padding:0}.download-intro{gap:25px}.download-list .button{color:#19394D;background:transparent}.download-list .button span{color:#4B6172}}
</style></head><body><header class="top"><a class="brand" href="./" aria-label="Common Ground home"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="12" cy="12" r="6" fill="#216B88"/><circle cx="28" cy="12" r="6" fill="#A1486D"/><path d="M5 32Q5 20 12 20Q19 20 19 32M21 32Q21 20 28 20Q35 20 35 32" fill="#19394D"/><path d="M4 34H36" stroke="#D8AC5C" stroke-width="3"/></svg>Common Ground</a><a class="button" href="./">Back to the course</a></header><main class="download-wrap"><section class="download-intro"><div><p class="intro">Listen and learn offline</p><h1>Take a chapter<br>with you.</h1><p>Each package includes the narrated deck, a continuous audio track, a chapter PDF, the study companion, and the complete visual companion. Download one chapter at a time for a smaller file.</p></div><aside class="download-guide" aria-label="How to use a chapter download"><h2>From download to learning</h2><ol><li>Download a chapter and extract the ZIP in your Files app.</li><li>Open the HTML deck in a browser, or play the M4A audio directly.</li><li>Use the PDF for the slides and the study companion for evidence notes and written practice.</li></ol></aside></section><ul class="download-list" aria-label="Chapter downloads">'''+''.join(rows)+'''</ul><section class="pdf-downloads" aria-label="PDF companions"><div><h2>The complete slide deck</h2><p>All '''+str(sum(len(c['slides']) for c in C))+''' slides in one PDF, for reading away from the screen or printing.</p><a href="downloads/all-slides.pdf" download>Download all slides</a></div><div><h2>The visual companion</h2><p>All 48 teaching illustrations collected in a printable guide, with one figure per page.</p><a href="visual-guide.html">Explore all visuals</a> · <a href="downloads/visual-guide.pdf" download>Download the visual PDF</a></div><div><h2>The study companion</h2><p>Evidence notes, the final written case, suggested reasoning, and a self-assessment rubric.</p><a href="downloads/study-guide.pdf" download>Download the companion PDF</a> · <a href="study-guide.html">Read online</a></div></section><footer class="footer"><a href="https://github.com/snowch/common-ground-social-psychology/blob/main/LICENSE">Copyright © 2026 Christopher Snow. All rights reserved.</a><br>The narrated decks and audio work offline. External reading links need a connection. The optional written case and study companion have no recorded narration.<br><a href="THIRD-PARTY-NOTICES.txt">Asset credits and licences</a></footer></main></body></html>''')
(D/'.nojekyll').write_text('')
for f in D.rglob('*'):
 if f.is_file():assert f.stat().st_size<25*2**20,(f,f.stat().st_size)
print('Hosted course prepared; every asset under 25 MiB.')
print('ZIP sizes:',[(p.name,round(p.stat().st_size/2**20,1))for p in sorted((D/'downloads').glob('*.zip'))])
