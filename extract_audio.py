"""Recover individual clips from a portable HTML deck, if needed."""
from pathlib import Path
import argparse,base64,json
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('deck',nargs='?',default='out/portable/index.html');p.add_argument('--output',default='audio/clips');a=p.parse_args()
text=(R/a.deck).read_text();start=text.index('const RECORDED_AUDIO=')+len('const RECORDED_AUDIO=');clips,_=json.JSONDecoder().raw_decode(text[start:]);out=R/a.output;out.mkdir(parents=True,exist_ok=True)
if not all(v.startswith('data:audio/')for v in clips.values()):raise SystemExit('Use a portable HTML deck with embedded recordings.')
for name,url in clips.items():(out/(name+'.m4a')).write_bytes(base64.b64decode(url.split(',',1)[1]))
print('Extracted',len(clips),'recordings to',out)
