from pathlib import Path
from html.parser import HTMLParser
import urllib.request,concurrent.futures,json,re,hashlib
import argparse
a=argparse.ArgumentParser(description='Screen course expression against linked public reading pages; this is not legal clearance.');a.add_argument('--cache',type=Path,default=Path('/tmp/common-ground-reading-audit'));args=a.parse_args()
R=Path(__file__).resolve().parents[1];D=args.cache;D.mkdir(parents=True,exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.parts.append(s)
def words(s):return re.findall(r"[a-z]+(?:'[a-z]+)?|[0-9]+",s.lower().replace('’',"'"))
course=json.loads((R/'course.json').read_text());urls=sorted({r['url']for c in course for r in c['refs']if r['url'].startswith(('https://openstax.org/','https://nobaproject.com/'))})
def fetch(u):
 key=hashlib.sha256(u.encode()).hexdigest()[:12];p=D/(key+'.html');rec={'url':u}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (course source review)'}),timeout=30)as f:b=f.read();rec['status']=f.status
  p.write_bytes(b);x=Text();x.feed(b.decode('utf-8','replace'));w=words(' '.join(x.parts));rec.update(sha256=hashlib.sha256(b).hexdigest(),tokens=len(w));return rec,w
 except Exception as e:rec['error']=type(e).__name__;return rec,[]
units=[]
def collect(v,path):
 if isinstance(v,str):
  if not v.startswith('https://'):units.append((path,words(re.sub(r'\[([^\]]+)\]\(/[^/]+/\)',r'\1',re.sub(r'\[pause [0-9.]+\]',' ',v)))))
 elif isinstance(v,list):
  for i,x in enumerate(v):collect(x,f'{path}[{i}]')
 elif isinstance(v,dict):
  for k,x in v.items():
   if k not in ['refs','sources','url','id','color','icon','part']:collect(x,f'{path}.{k}')
for c in course:collect(c['slides'],f'chapter-{c["number"]}')
for f in ['course-evidence.json','learning-check.json']:collect(json.loads((R/f).read_text()),f)
# Include speech-specific wording that differs from display text.
for s in json.loads((R/'production/af-heart/scenes.json').read_text()):collect(s.get('say',s['text']),s['id']+'-recording')
unique={tuple(w):(p,w)for p,w in units if len(w)>=8};units=list(unique.values());records=[];hits=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:
 for rec,source in ex.map(fetch,urls):
  records.append(rec);index={}
  for k in range(len(source)-7):index.setdefault(tuple(source[k:k+8]),[]).append(k)
  for path,own in units:
   best=0
   for i in range(len(own)-7):
    for j in index.get(tuple(own[i:i+8]),[]):
     n=8
     while i+n<len(own)and j+n<len(source)and own[i+n]==source[j+n]:n+=1
     best=max(best,n)
   if best>=8:hits.append({'course_unit':path,'source_url':rec['url'],'longest_matching_words':best})
out={'checked_utc':'2026-11-11','method':'Case-normalized contiguous word matching against linked public reading pages. An 8-word candidate threshold is a screening choice, not a legal rule or safe harbor. Source text retained only in ignored/external working storage. No proprietary textbook full text was acquired or compared.','unique_course_units':len(units),'source_pages':records,'candidate_overlaps':hits};(R/'qa/copyright-source-overlap.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'unique_units':len(units),'sources':len(records),'failures':[r for r in records if r.get('status')!=200],'candidates':hits},indent=2))
