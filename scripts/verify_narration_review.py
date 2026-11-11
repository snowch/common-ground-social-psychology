"""Verify speech assets, deliberate pauses, and unchanged quiz answer keys."""
from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];W=R/'production/af-heart'
review=json.loads((R/'editorial/narration-review-v0.1.2.json').read_text());scenes={x['id']:x for x in json.loads((W/'scenes.json').read_text())}
assert review['reviewed']==149 and len(review['clips'])==149
records=[]
for row in review['clips']:
 if row['status']!='revised':continue
 s=scenes[row['id']];targets=[float(x)for x in re.findall(r'\[pause ([0-9.]+)\]',s.get('say',''))];a,sr=sf.read(W/'audio'/f"{s['id']}.wav",dtype='float32')
 assert sr==24000 and np.isfinite(a).all()and np.max(np.abs(a))<1,s['id']
 mask=np.concatenate(([False],a==0,[False]));starts=np.flatnonzero(np.diff(mask.astype(int))==1);ends=np.flatnonzero(np.diff(mask.astype(int))==-1);gaps=[float(e-b)/sr for b,e in zip(starts,ends)if e-b>=.3*sr]
 # Match each requested pause in order; extra natural silence is permitted.
 matched={0}
 for gap in gaps:
  matched|={i+1 for i in list(matched)if i<len(targets)and targets[i]-.01<=gap<=targets[i]+.4}
 assert len(targets)in matched,(s['id'],targets,gaps)
 records.append(dict(id=s['id'],pause_count=len(targets),explicit_pause_seconds=sum(targets),raw_seconds=round(len(a)/sr,3),peak=round(float(np.max(np.abs(a))),6)))
original=json.loads(subprocess.check_output(['git','show','f9a251c:course.json'],cwd=R));current=json.loads((R/'course.json').read_text())
assert [[q['correct']for q in c['quizzes']]for c in original]==[[q['correct']for q in c['quizzes']]for c in current]
m=json.loads((R/'audio/manifest.json').read_text())
for item in m['clips']+m['chapters']:assert hashlib.sha256((R/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
report=dict(reviewed_clips=149,revised_clips=len(records),retained_clips=review['reviewed']-len(records),measured_pauses=sum(x['pause_count']for x in records),explicit_pause_seconds=sum(x['explicit_pause_seconds']for x in records),quiz_answer_keys='unchanged',encoded_audio_hashes='verified',clips=records)
(R/'qa/narration-review-waveforms.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='clips'},indent=2))
