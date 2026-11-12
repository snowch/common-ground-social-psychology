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
if len(clips)!=150:raise SystemExit('Expected 150 audio/clips/*.m4a recordings. See README.md for setup.')
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
for name in ['FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt']:shutil.copy(R/name,D/name)
shutil.copytree(R/'licenses',D/'licenses',dirs_exist_ok=True)
(D/'assets/fonts').mkdir(parents=True,exist_ok=True)
shutil.copy(R/'assets/fonts/manifest.json',D/'assets/fonts/manifest.json')
if not a.portable:shutil.copytree(R/'audio',D/'audio',dirs_exist_ok=True)
print(f"Built {'portable'if a.portable else 'streamed-audio'} course in {D}")
