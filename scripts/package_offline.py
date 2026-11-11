"""Package the built portable course and tracked source for local offline use."""
from pathlib import Path
import argparse,hashlib,subprocess,zipfile
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--portable',default='out/portable');p.add_argument('--output',default='out/packages');a=p.parse_args()
D=R/a.portable;O=R/a.output;O.mkdir(parents=True,exist_ok=True)
if not (D/'index.html').exists():raise SystemExit('First run: python3 build.py --portable --output out/portable')
archive=O/'common-ground-af-heart.zip';seen=set()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 def add(file,relative):
  name='common-ground/'+relative.as_posix()
  if name not in seen:z.write(file,name);seen.add(name)
 for file in sorted(D.rglob('*')):
  if file.is_file():add(file,file.relative_to(D))
 files=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
 for name in files:
  if not name or name.startswith('audio/clips/'):continue
  file=R/name
  if file.is_file():add(file,Path(name))
 z.writestr('common-ground/START-HERE.txt','''COMMON GROUND — AF_HEART EDITION

Open index.html in a modern browser and press Play narration. Individual chapter decks are in chapters/. Play audio/chapters/*.m4a directly for continuous listening. PDFs provide the static slides. study-guide.html and study-guide.pdf contain evidence notes and the optional written final case, with suggested reasoning and a self-assessment rubric. This companion has no recorded narration.

The HTML includes the individual recorded clips for offline use. To recover separate clips for rebuilding, run:
python3 extract_audio.py index.html

Editable source and build instructions are also available in the project repository:
https://github.com/snowch/common-ground-social-psychology

Learn through fictional stories, decisions, recall, and field practice. Further readings are linked in each chapter. Asset licenses and credits are in FONT-LICENSE.txt, THIRD-PARTY-NOTICES.txt, and licenses/.
''')
with zipfile.ZipFile(archive)as z:
 if z.testzip()is not None:raise SystemExit('ZIP integrity check failed')
 for name in ['FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt','licenses/LibreBaskerville-OFL.txt','licenses/Arimo-OFL.txt']:
  assert 'common-ground/'+name in z.namelist(),name
 assert not any(n.endswith('.otf')for n in z.namelist()),'Obsolete font binary in offline package'
 notices=(R/'FONT-LICENSE.txt').read_text()
 htmls=[file for file in D.rglob('*.html')]
 for file in htmls:
  assert notices in z.read('common-ground/'+file.relative_to(D).as_posix()).decode(),file
 print(f'Font/notice packaging checks passed for {len(htmls)} HTML files.')
(O/'SHA256SUMS.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(f'Packaged {archive.name}: {archive.stat().st_size/2**20:.1f} MiB; integrity passed.')
