"""Regenerate revised scenes with the requested Kokoro skill, preserving valid speech."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,time,wave
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--record-scripts',default=os.environ.get('RECORD_DEMO_SCRIPTS','/workspace/claude-skills/plugins/demo-video/skills/record-demo/scripts'));args=parser.parse_args();
R=Path(__file__).resolve().parents[1];W=R/'production/af-heart';T=R/'out/narration-v0.1.2';T.mkdir(parents=True,exist_ok=True)
scenes=json.loads((W/'scenes.json').read_text());audit=json.loads((R/'editorial/narration-review-v0.1.2.json').read_text());changed={x['id']for x in audit['clips']if x['status']=='revised'}
old=json.loads((W/'audio/durations.json').read_text());durations=dict(old['durations']);A=T/'audit';(A/'audio').mkdir(parents=True,exist_ok=True);(A/'scenes.json').write_text(json.dumps(sorted(scenes,key=lambda s:len(s.get('say',s['text'])),reverse=True),ensure_ascii=False,indent=2))
previous=json.loads((W/'audio/asr-report.json').read_text());(A/'audio/asr-progress.json').write_text(json.dumps(dict(scenes=[x for x in previous['scenes']if x['id']not in changed]),indent=2))
# Reuse the completed one-thread pilot because its script and settings match exactly.
pilot=R/'out/tts-benchmark';p=json.loads((pilot/'scenes.json').read_text())[0]
assert p==next(s for s in scenes if s['id']==p['id'])
completed={p['id']};shutil.copy2(pilot/'audio'/f"{p['id']}.wav",A/'audio'/f"{p['id']}.wav");shutil.copy2(pilot/'audio'/f"{p['id']}.wav",W/'audio'/f"{p['id']}.wav");durations.update(json.loads((pilot/'audio/durations.json').read_text())['durations'])
remaining=sorted([s for s in scenes if s['id']in changed-completed],key=lambda x:len(x.get('say',x['text'])),reverse=True)
bins=[[]for _ in range(4)];loads=[0]*4
for s in remaining:
 i=min(range(4),key=loads.__getitem__);bins[i].append(s);loads[i]+=len(s.get('say',s['text']))
env=os.environ.copy();env.update(DEMO_TTS_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
processes=[];logs=[]
for i,items in enumerate(bins):
 d=T/f'worker-{i+1}';(d/'audio').mkdir(parents=True,exist_ok=True);(d/'scenes.json').write_text(json.dumps(items,ensure_ascii=False,indent=2));log=(d/'synthesis.log').open('w');logs.append(log)
 processes.append((d,subprocess.Popen(['uv','run',str(Path(args.record_scripts)/'tts.py'),str(d),'af_heart','1.0'],env=env,stdout=log,stderr=subprocess.STDOUT)))
print('Started four bounded one-thread Kokoro workers for',len(remaining),'clips.',flush=True)
asrlog=(T/'asr.log').open('w');asr=subprocess.Popen(['uv','run',str(R/'production/asr_batch.py'),str(A),'--record-scripts',args.record_scripts],stdout=asrlog,stderr=subprocess.STDOUT)
last=-1
while True:
 for d,proc in processes:
  if proc.poll()not in (None,0):raise RuntimeError(f'Synthesis failed: {d}/synthesis.log')
  for f in (d/'audio').glob('*.wav'):
   if f.stem in completed or time.time()-f.stat().st_mtime<.8:continue
   with wave.open(str(f))as wav:assert wav.getframerate()==24000 and wav.getnframes()>0
   shutil.copy2(f,A/'audio'/f.name);shutil.copy2(f,W/'audio'/f.name);completed.add(f.stem)
 if len(completed)!=last:print('Completed',len(completed),'of',len(changed),'revised clips.',flush=True);last=len(completed)
 if all(proc.poll()==0 for _,proc in processes)and len(completed)==len(changed):break
 time.sleep(.5)
for d,proc in processes:
 data=json.loads((d/'audio/durations.json').read_text());assert data['voice']=='af_heart'and data['speed']==1.0 and data['engine']==old['engine'];durations.update(data['durations'])
old['durations']=durations;(W/'audio/durations.json').write_text(json.dumps(old,indent=1));print('Merged generation provenance and durations.',flush=True)
subprocess.run([sys.executable,str(R/'production/encode_audio.py')],check=True)
if asr.wait()!=0:raise RuntimeError('Independent transcription failed; inspect out/narration-v0.1.2/asr.log')
shutil.copy(A/'audio/asr-report.json',W/'audio/asr-report.json');shutil.copy(A/'audio/asr-report.json',R/'qa/af-heart-asr-report.json')
print('Synthesis, encoding, chapter tracks, and independent ASR finished.',flush=True)
