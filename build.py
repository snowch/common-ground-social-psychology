"""Build the course with the standard library and bundled assets."""
from pathlib import Path
import argparse,base64,json,re,shutil
from scripts.build_study_guide import render as render_study_guide
from scripts.build_visual_guide import render as render_visual_guide
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--portable',action='store_true',help='Embed narration in each HTML deck for offline use.')
p.add_argument('--output',default='dist',help='Build output directory (default: dist).')
a=p.parse_args();D=(R/a.output).resolve();D.mkdir(parents=True,exist_ok=True);(D/'chapters').mkdir(exist_ok=True)
C=json.loads((R/'course.json').read_text());clips={f.stem:f for f in (R/'audio/clips').glob('*.m4a')}
expected={s['id'] for c in C for s in c['slides']}
for c in C:
 for s in c['slides']:
  expected.update(s['id']+'-feedback-'+str(i) for i in range(len(s.get('quiz',{}).get('options',[]))))
  if 'answers' in s:expected.add(s['id']+'-answers')
if set(clips)!=expected:raise SystemExit('Recordings do not match the course: '+str(set(clips)^expected))
fonts=''
for family,name in [('CourseSerif','LibreBaskerville[wght].ttf'),('CourseSans','Arimo[wght].ttf')]:
 b=base64.b64encode((R/'assets/fonts'/name).read_bytes()).decode();fonts+=f'@font-face{{font-family:{family};src:url(data:font/ttf;base64,{b}) format("truetype");font-weight:100 900;font-display:swap}}\n'
def spoken_text(scene):
 text=scene.get('say',scene['text'])
 text=re.sub(r'\[pause [0-9.]+\]', '\n\n', text)
 return re.sub(r'\[([^\]]+)\]\(/[^/]+/\)',r'\1',text).strip()
narration={x['id']:spoken_text(x)for x in json.loads((R/'production/af-heart/scenes.json').read_text())}
rights=(R/'FONT-LICENSE.txt').read_text()+'\n'+(R/'THIRD-PARTY-NOTICES.txt').read_text()
assert '-->' not in rights
visual_js=(R/'visuals.js').read_text()+'\n'+(R/'visual-lessons.js').read_text()
template=(R/'template.html').read_text().replace('__VISUALS__',visual_js).replace('__FONTS__',fonts).replace('__RIGHTS_NOTICES__',rights)
quiz_metadata={s['id']:dict(revision=s['quiz'].get('revision'),reasoningPrompt=bool(s['quiz'].get('reasoningPrompt')))for c in C for s in c['slides']if 'quiz'in s}
template=template.replace('__QUIZ_METADATA__',json.dumps(quiz_metadata))
for placeholder,file in [('__GLOSSARY__','glossary.json'),('__EVIDENCE__','course-evidence.json'),('__LEARNING_CHECK__','learning-check.json')]:
 template=template.replace(placeholder,json.dumps(json.loads((R/file).read_text()),ensure_ascii=False).replace('</','<\\/'))

def render(path,chapters,prefix):
 numbers={f"c{c['number']:02d}"for c in chapters}
 audio={key:('data:audio/mp4;base64,'+base64.b64encode(file.read_bytes()).decode()if a.portable else prefix+'audio/clips/'+file.name)for key,file in clips.items()if key[:3]in numbers}
 s=template.replace('__NARRATION_TEXT__',json.dumps({k:v for k,v in narration.items()if k[:3]in numbers},ensure_ascii=False).replace('</','<\\/')).replace('__DATA__',json.dumps(chapters,ensure_ascii=False).replace('</','<\\/')).replace('__AUDIO__',json.dumps(audio))
 if not a.portable:
  s=s.replace('The recordings are included in this deck and work offline.','Recordings load when you press Play narration. The portable build embeds them for offline use.').replace('The deck embeds prerecorded Kokoro','The course plays prerecorded Kokoro').replace('Quizzes and embedded narration work offline. External reading requires a connection.','This build loads audio files from its audio folder. Use the portable build for self-contained offline decks.')
 path.write_text(s)
(D/'study-guide.html').write_text(render_study_guide(R).replace('__FONTS__',fonts).replace('__RIGHTS_NOTICES__',rights))
(D/'visual-guide.html').write_text(render_visual_guide(R).replace('__FONTS__',fonts).replace('__RIGHTS_NOTICES__',rights))
if (R/'visual-guide.pdf').exists():shutil.copy(R/'visual-guide.pdf',D/'visual-guide.pdf')
if (R/'study-guide.pdf').exists():shutil.copy(R/'study-guide.pdf',D/'study-guide.pdf')
render(D/'index.html',C,'./')
for c in C:
 slug=f"chapter-{c['number']:02d}"
 render(D/'chapters'/f'{slug}.html',[c],'../');shutil.copy(R/'chapters'/f'{slug}.pdf',D/'chapters'/f'{slug}.pdf')
shutil.copy(R/'common-ground-slides.pdf',D/'common-ground-slides.pdf')
for name in ['LICENSE','FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt']:shutil.copy(R/name,D/name)
shutil.copytree(R/'licenses',D/'licenses',dirs_exist_ok=True)
(D/'assets/fonts').mkdir(parents=True,exist_ok=True)
shutil.copy(R/'assets/fonts/manifest.json',D/'assets/fonts/manifest.json')
if not a.portable:shutil.copytree(R/'audio',D/'audio',dirs_exist_ok=True)
print(f"Built {'portable'if a.portable else 'streamed-audio'} course in {D}")

# Include the project notice in every HTML edition, including offline decks.
for page in D.rglob("*.html"):
 text=page.read_text()
 if 'class="copyright-notice"' in text:continue
 # Keep the notice in each printed page's footer rather than creating a final
 # notice-only page that shifts the slide and chapter export page ranges.
 if 'const RECORDED_AUDIO=' in text:
  print_notice='@media print{.copyright-notice{position:fixed;bottom:2px;left:0;right:0;margin:0;padding:2px 12px!important;font:9px/1.4 sans-serif!important;background:#fff;color:#19394D;z-index:10}.copyright-notice a{font:inherit!important;color:inherit!important}}'
 else:
  print_notice='@media print{.copyright-notice{display:none!important}}@page{@bottom-center{content:"Copyright © 2026 Christopher Snow. All rights reserved.";font:9px sans-serif;color:#19394D}}'
 text=text.replace('</style>',print_notice+'</style>',1)
 marker="</body>" if "</body>" in text else "</html>"
 assert marker in text, page
 page.write_text(text.replace(marker, '<footer class="copyright-notice" style="padding:1rem 4vw;font:14px/1.6 sans-serif"><a href="https://github.com/snowch/common-ground-social-psychology/blob/main/LICENSE">Copyright © 2026 Christopher Snow. All rights reserved.</a></footer>'+marker, 1))
