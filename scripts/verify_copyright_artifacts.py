"""Verify the audited artifact set and notices; this does not establish legal clearance."""
from pathlib import Path
import base64,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1];P=R/'out/portable'
forbidden=re.compile(r'\bThe\s+Social\s+Animal\b|\bAronsons?\b|\b480[- ]page',re.I)
manifest=json.loads((R/'assets/fonts/manifest.json').read_text())
for item in manifest['files']:assert hashlib.sha256((R/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
assert not list((R/'assets/fonts').glob('*.otf'))
expected_fonts={x['sha256']for x in manifest['files']if x['file'].endswith('.ttf')}
font_notice=(R/'FONT-LICENSE.txt').read_text();asset_notice=(R/'THIRD-PARTY-NOTICES.txt').read_text()
htmls=[P/'index.html',*sorted((P/'chapters').glob('*.html')),P/'study-guide.html']
for file in htmls:
 text=file.read_text();assert not forbidden.search(text),file;assert font_notice in text and asset_notice in text,file
 data=re.findall(r'data:font/ttf;base64,([A-Za-z0-9+/=]+)',text)
 assert {hashlib.sha256(base64.b64decode(x)).hexdigest()for x in data}==expected_fonts,file
 assert not re.search(r'__[A-Z_]+__',text),file
for file in (P/'licenses').glob('*.txt'):assert file.read_bytes()==(R/'licenses'/file.name).read_bytes()
for file in ['FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt']:assert (P/file).read_bytes()==(R/file).read_bytes()
pdfs=[R/'common-ground-slides.pdf',*sorted((R/'chapters').glob('*.pdf')),R/'study-guide.pdf'];pdf_rows=[]
for file in pdfs:
 names=subprocess.check_output(['pdffonts',str(file)],text=True);assert 'Nimbus'not in names and 'URWBookman'not in names,file
 for row in names.splitlines()[2:]:assert any(name in row for name in ['Arimo-','LibreBaskerville-']),row
 text=subprocess.check_output(['pdftotext',str(file),'-'],text=True);assert not forbidden.search(text),file
 info=subprocess.check_output(['pdfinfo',str(file)],text=True);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1]);assert pages==(11 if file.name=='study-guide.pdf'else 80 if file.name=='common-ground-slides.pdf'else 8)
 pdf_rows.append({'file':str(file.relative_to(R)),'pages':pages,'font_families':'Libre Baskerville / Arimo','book_comparison_scan':'clear'})
audio=json.loads((R/'audio/manifest.json').read_text());clips=audio['clips'];tracks=audio['chapters']
for item in clips+tracks:assert hashlib.sha256((R/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
assert not subprocess.check_output(['git','diff','HEAD','--name-only','--','audio/'],cwd=R).strip()
wrapper=(R/'production/asr_batch.py').read_text();assert "str(upstream)"in wrapper and 'def speech('not in wrapper and 'norm=lambda'not in wrapper
assets=[*sorted((R/'assets/fonts').glob('*.ttf')),*sorted((R/'audio').rglob('*.m4a')),*pdfs,*sorted((R/'licenses').glob('*.txt')),R/'FONT-LICENSE.txt',R/'THIRD-PARTY-NOTICES.txt'];rows=[]
for file in assets:rows.append({'file':str(file.relative_to(R)),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(R/'qa/copyright-inventory.json').write_text(json.dumps({'date_utc':'2026-11-11','scope':'Current font, audio, PDF and license artifacts; earlier Git/release artifacts excluded','assets':rows},indent=2)+'\n')
out={'revision':'v0.3.0','purpose':'Artifact consistency and license-notice verification, not a determination of non-infringement','html_files':len(htmls),'standalone_html_font_and_asset_notices':'passed','embedded_font_hashes':'passed','font_license_hashes':'passed','removed_URW_binaries':'passed','learner_book_comparison_scan':'clear','pdfs':pdf_rows,'encoded_clip_hashes':len(clips),'continuous_track_hashes':len(tracks),'audio_unchanged_from_parent_commit':True,'external_ASR_runner_source_check':'passed','interactive_Site_browser_QA':'not rerun; managed preview route unavailable'}
(R/'qa/copyright-artifact-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='pdfs'},indent=2))
