# /// script
# requires-python = ">=3.10,<3.13"
# ///
"""Run independent screening through a separately obtained record-demo checkout.

This wrapper distributes no upstream ASR implementation. Three external workers
screen stable WAV inputs and merge their reports into the existing course format.
"""
from pathlib import Path
import argparse,concurrent.futures,json,os,statistics,subprocess,tempfile,time


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('workdir',type=Path)
 parser.add_argument('--record-scripts',type=Path,default=os.environ.get('RECORD_DEMO_SCRIPTS','/workspace/claude-skills/plugins/demo-video/skills/record-demo/scripts'))
 args=parser.parse_args();work=args.workdir.resolve();upstream=args.record_scripts.resolve()/'asr.py'
 if not upstream.is_file():parser.error('Obtain the authorized record-demo checkout separately and set --record-scripts or RECORD_DEMO_SCRIPTS.')
 scenes=json.loads((work/'scenes.json').read_text());cache=work/'audio/asr-progress.json'
 retained=json.loads(cache.read_text()).get('scenes',[])if cache.exists()else []
 valid_ids={s['id']for s in scenes};by_id={r['id']:r for r in retained if r['id']in valid_ids}
 pending=[s for s in scenes if s['id']not in by_id]
 print(f'Reusing {len(by_id)} screened clips; waiting for {len(pending)} stable WAV inputs.',flush=True)
 def worker(batch):
  with tempfile.TemporaryDirectory(prefix='common-ground-asr-')as temp:
   job=Path(temp);(job/'audio').mkdir();(job/'scenes.json').write_text(json.dumps(batch,ensure_ascii=False))
   for scene in batch:
    source=work/'audio'/(scene['id']+'.wav')
    while not source.exists()or time.time()-source.stat().st_mtime<1:time.sleep(.5)
    (job/'audio'/source.name).symlink_to(source)
   env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
   subprocess.run(['uv','run',str(upstream),str(job),'small.en'],env=env,check=True)
   result=json.loads((job/'audio/asr-report.json').read_text())
   rows=result['scenes'];baseline=statistics.median(row['level']for row in rows)if rows else 0
   for row in rows:
    checks={}
    checks['words']=row['ratio']<0.9
    checks['pace']=not row['short']and (row['wpm']<120 or row['wpm']>190)
    checks['clip']=row['peak']>=0.99
    checks['level']=abs(row['level']-baseline)>3
    checks['gap']=row['gap']>row['gap_ok']
    row['flags']=[label for label,failed in checks.items()if failed]
   assert sum(bool(row['flags'])for row in rows)==result['flagged'],'External ASR criteria changed; review the upstream interface.'
   return rows
 batches=[pending[i::3]for i in range(3)if pending[i::3]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
  for rows in pool.map(worker,batches):
   by_id.update((r['id'],r)for r in rows)
   cache.write_text(json.dumps({'scenes':list(by_id.values())},indent=2))
 rows=[by_id[s['id']]for s in scenes]
 report={'method':'External record-demo ASR screening of audio-only inputs; existing cached screens retained. Not a human listening review.','model':'small.en','flagged':sum(bool(r.get('flags'))for r in rows),'scenes':rows}
 (work/'audio/asr-report.json').write_text(json.dumps(report,indent=2))
 print(f'Screening complete: {len(rows)} clips, {report["flagged"]} flagged.',flush=True)


if __name__=='__main__':main()
