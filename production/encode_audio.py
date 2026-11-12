"""Encode finished Kokoro speech and assemble chapter listening tracks."""
import concurrent.futures,hashlib,json,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
W=R/'production/af-heart'
OUT=R/'audio/clips';CH=R/'audio/chapters';OUT.mkdir(parents=True,exist_ok=True);CH.mkdir(parents=True,exist_ok=True)
scenes=json.loads((W/'scenes.json').read_text())
assert len(scenes)==len({s['id'] for s in scenes})

def encode(s):
 src=W/'audio'/f"{s['id']}.wav"; dst=OUT/f"{s['id']}.m4a"
 while not src.exists() or time.time()-src.stat().st_mtime<1.0:time.sleep(0.5)
 if not dst.exists() or dst.stat().st_mtime<src.stat().st_mtime:
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(src),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1','-c:a','aac','-b:a','160k','-threads','1','-movflags','+faststart',str(dst)],check=True)
 result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(dst)]))['format']
 return dict(id=s['id'],file=str(dst.relative_to(R)),duration=float(result['duration']),bytes=int(result['size']),sha256=hashlib.sha256(dst.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(2) as pool:clips=list(pool.map(encode,scenes))
print('Encoded',len(clips),'clips',flush=True)
# Assemble from raw, equally sampled speech, then normalize the whole chapter.
silence=W/'audio/pause.wav'
if not silence.exists():subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','anullsrc=r=24000:cl=mono','-t','6','-c:a','pcm_s16le',str(silence)],check=True)
chapters=json.loads((R/'course.json').read_text());tracks=[]
for c in chapters:
 files=[]
 for s in c['slides']:
  files.append(W/'audio'/f"{s['id']}.wav")
  if 'quiz'in s:
   files.extend([silence,W/'audio'/f"{s['id']}-feedback-{s['quiz']['correct']}.wav"])
  if 'answers'in s:files.extend([silence,W/'audio'/f"{s['id']}-answers.wav"])
 lst=W/f"chapter-{c['number']:02d}-concat.txt"
 lst.write_text(''.join(f"file '{x}'\n" for x in files))
 dst=CH/f"chapter-{c['number']:02d}.m4a"
 if not dst.exists() or any(x.stat().st_mtime>dst.stat().st_mtime for x in files):
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1','-c:a','aac','-b:a','160k','-threads','1','-metadata','title='+c['title'],'-metadata','artist=Common Ground — Kokoro af_heart','-movflags','+faststart',str(dst)],check=True)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dst)]))
 tracks.append(dict(chapter=c['number'],title=c['title'],file=str(dst.relative_to(R)),duration=duration,sha256=hashlib.sha256(dst.read_bytes()).hexdigest()))
 print('Chapter',c['number'],round(duration,1),'seconds',flush=True)
durations=json.loads((W/'audio/durations.json').read_text())
assert set(durations['durations'])=={s['id'] for s in scenes}
manifest=dict(voice=durations['voice'],speed=durations['speed'],engine=durations['engine'],encoding=dict(codec='AAC',sample_rate=48000,channels=1,bitrate=160000,loudness_target_lufs=-16,true_peak_target_dbtp=-1.5),clips=clips,chapters=tracks,review='Independent ASR and phoneme screening; not a human listening review')
(R/'audio/manifest.json').write_text(json.dumps(manifest,indent=2))
print('Narration manifest written.',flush=True)
