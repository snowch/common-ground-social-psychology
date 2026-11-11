"""Independent Whisper small.en screening using the skill's checks, in audio-only batches.
No script prompt, hotwords, or vocabulary hint is passed to the recognizer.
"""
import bisect,difflib,json,os,re,sys,time,concurrent.futures
from pathlib import Path
import numpy as np,soundfile as sf
from faster_whisper import WhisperModel,BatchedInferencePipeline
W=Path(sys.argv[1]);scenes=json.loads((W/'scenes.json').read_text())
m=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=1,num_workers=3)
PAUSE=re.compile(r'\[pause(?:\s+(\d*\.?\d+))?\]')
norm=lambda s:re.sub(r'\s+',' ',re.sub(r'\[([^\]]+)\]\(/[^)]*/\)',r'\1',PAUSE.sub(' ',s)).lower())
words=lambda s:re.sub(r'[^a-z0-9 ]',' ',norm(s)).split()
spoken=lambda s:words(re.sub(r'(?<=\w)([./-])(?=\w)',lambda m:{'.':' dot ','/':' slash ','-':' dash '}[m[1]],s))
similar=lambda a,b:difflib.SequenceMatcher(None,a,b).ratio()
db=lambda x:20*np.log10(max(float(x),1e-9))
def speech(a,sr):
 n=int(sr*.02);f=a[:len(a)//n*n].reshape(-1,n);rms=np.sqrt((f**2).mean(axis=1));voiced=rms>10**(-40/20)*max(np.abs(a).max(),1e-9)
 if not voiced.any():return -120.,0.
 idx=np.flatnonzero(voiced);gaps=np.diff(idx)-1
 return db(np.sqrt((rms[voiced]**2).mean())),float(gaps.max()*.02 if len(gaps) else 0.)
progress=W/'audio/asr-progress.json'
rows=json.loads(progress.read_text())['scenes'] if progress.exists() else []
seen={r['id'] for r in rows};pending=[s for s in scenes if s['id']not in seen]
print('Retaining',len(rows),'already screened clips; batching',len(pending),'remaining.',flush=True)
def screen_batch(batch):
 pipeline=BatchedInferencePipeline(model=m)
 output=[];arrays=[];raw=[];intervals=[];starts=[];clock=0.
 for s in batch:
  path=W/'audio'/f"{s['id']}.wav"
  while not path.exists() or time.time()-path.stat().st_mtime<1:time.sleep(.5)
  a,sr=sf.read(path,dtype='float32');raw.append((a,sr))
  t=np.arange(0,len(a)/sr,1/16000);resampled=np.interp(t,np.arange(len(a))/sr,a).astype('float32')
  starts.append(clock);intervals.append(dict(start=clock,end=clock+len(resampled)/16000))
  arrays.extend([resampled,np.zeros(16000,dtype='float32')]);clock+=len(resampled)/16000+1
 # Explicit clip boundaries prevent concatenation from mixing the individual recordings.
 if any(x['end']-x['start']>30 for x in intervals):
  heard=[]
  for a,sr in raw:
   t=np.arange(0,len(a)/sr,1/16000);segs,_=m.transcribe(np.interp(t,np.arange(len(a))/sr,a).astype('float32'),language='en',beam_size=5)
   heard.append(' '.join(x.text.strip()for x in segs))
 else:
  segs,_=pipeline.transcribe(np.concatenate(arrays),language='en',beam_size=5,batch_size=8,clip_timestamps=intervals,word_timestamps=False)
  texts=[[]for _ in batch]
  for seg in segs:
   k=max(0,min(len(batch)-1,bisect.bisect_right(starts,seg.start+.001)-1));texts[k].append(seg.text.strip())
  heard=[' '.join(t) for t in texts]
 for s,(a,sr),heard_text in zip(batch,raw,heard):
  say=s.get('say',s['text']);pauses=[float(p or .5)for p in PAUSE.findall(say)];level,gap=speech(a,sr);said=words(say)
  output.append(dict(id=s['id'],text=s['text'],heard=heard_text,level=level,gap=gap,peak=float(np.abs(a).max()),ratio=max(similar(words(s['text']),words(heard_text)),similar(said,spoken(heard_text))),wpm=len(said)/max(len(a)/sr-sum(pauses),.1)*60,short=len(said)<10,gap_ok=max(1.5,max(pauses,default=0)+1.)))
  print('Screened',s['id'],round(output[-1]['ratio'],3),flush=True)
 return output
with concurrent.futures.ThreadPoolExecutor(3) as pool:
 futures=[pool.submit(screen_batch,pending[i:i+4]) for i in range(0,len(pending),4)]
 for future in concurrent.futures.as_completed(futures):
  rows.extend(future.result());progress.write_text(json.dumps(dict(scenes=rows),indent=2))
order={s['id']:i for i,s in enumerate(scenes)};rows.sort(key=lambda r:order[r['id']])
median=float(np.median([r['level']for r in rows]));flagged=0
for r in rows:
 why=[w for w,bad in [('words',r['ratio']<.9),('pace',not r['short']and not 120<=r['wpm']<=190),('clip',r['peak']>=.99),('level',abs(r['level']-median)>3),('gap',r['gap']>r['gap_ok'])]if bad]
 r['flags']=why;flagged+=bool(why)
 if why:print('!!',r['id'],why,r['ratio'],r['heard'],flush=True)
report=dict(method='Independent unprompted Whisper screening. Audio-only batches with explicit clip boundaries; skill word, pacing, peak, level, and gap checks. Not a human listening review.',model='small.en',flagged=flagged,scenes=rows)
(W/'audio/asr-report.json').write_text(json.dumps(report,indent=2))
print('Finished',len(rows),'clips;',flagged,'flagged for inspection.',flush=True)
