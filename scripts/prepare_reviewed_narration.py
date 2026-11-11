"""Compile the reviewed teaching text into recording scenes and a pacing audit."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];C=json.loads((R/'course.json').read_text());before=json.loads((R/'editorial/narration-before-v0.1.2.json').read_text());old={x['id']:x for x in before}
def speech_form(text):
 text=re.sub(r'\bMaya[’\']s\b','[Maya’s](/mˈaɪəz/)',text)
 text=re.sub(r'\bMaya\b(?![’\']s)',lambda m:'[Maya](/mˈaɪə/)',text) if '[Maya’s]'not in text else re.sub(r'(?<!\[)\bMaya\b(?![’\'])','[Maya](/mˈaɪə/)',text)
 return text.replace('£100','one hundred pounds').replace('£300','three hundred pounds').replace('2024','twenty twenty-four').replace('The linked Vaidis and colleagues study provides the details.','The linked study provides the details.')
scenes=[];audit=[]
for c in C:
 for slide in c['slides']:
  key=slide['id'];kind=slide['kind'];part=f"chapter-{c['number']:02d}"
  if key=='c01s01':scenes.append(old[key]);continue
  text=slide['text'];pause_note=''
  if kind in ('choice','transfer'):
   q=slide['quiz'];text+='\n\n'+'\n'.join(f"Option {chr(65+i)}. {o}"for i,o in enumerate(q['options']))+'\n\nPause here and make your choice.'
   core=slide['text'].split('\n\n');say=' [pause 0.6] '.join(core)+' [pause 0.6] '+' [pause 0.6] '.join(f"Option {chr(65+i)}. {o}"for i,o in enumerate(q['options']))+' [pause 0.7] Pause here and make your choice. [pause 2.0]'
   pause_note='Separate the question, instructions, and options; leave choice time.'
  elif kind=='recall':
   parts=text.split('\n\n');say=parts[0]+' [pause 0.7] '+parts[1]+' [pause 2.0] '+parts[2]+' [pause 2.0] '+parts[3]+' [pause 3.0]';pause_note='Two distinct prompts with thinking time.'
  elif kind=='practice':
   say=text.replace('\n\n',' [pause 0.9] ');pause_note='Separate the field task from the revisit plan.'
  else:
   say=text.replace('\n\n',' [pause 0.9] ')
   if text.endswith('?'):say+=' [pause 1.5]'
   pause_note='Pause at authored shifts in meaning.'
  s=dict(id=key,slide=(c['number']-1)*8+c['slides'].index(slide)+1,step=slide['title'],text=text,part=part,say=speech_form(say));scenes.append(s)
  if 'quiz'in slide:
   for i,f in enumerate(slide['quiz']['feedback']):
    fid=f'{key}-feedback-{i}';prefix='Good application.'if i==slide['quiz']['correct']else'Consider the consequence.';ftext=prefix+' '+f
    if ftext==old[fid]['text']:scenes.append(old[fid])
    else:scenes.append(dict(id=fid,step='Decision feedback',text=ftext,part=part,say=speech_form(prefix+' [pause 0.35] '+f)))
  if 'answers'in slide:
   aid=key+'-answers';atext='Suggested answers.\n\nFirst. '+slide['answers'][0]+'\n\nSecond. '+slide['answers'][1]
   scenes.append(dict(id=aid,step='Suggested recall answers',text=atext,part=part,say=speech_form(atext.replace('\n\n',' [pause 0.8] '))))
assert len(scenes)==150 and len({x['id']for x in scenes})==150
for s in scenes:
 if s['id']=='c01s01':continue
 previous=old[s['id']];changed=s['text']!=previous['text']or s.get('say',s['text'])!=previous.get('say',previous['text'])
 pauses=[float(x)for x in re.findall(r'\[pause ([0-9.]+)\]',s.get('say',''))]
 audit.append(dict(id=s['id'],reviewed=True,status='revised'if changed else'retained',before=previous['text'],after=s['text'],pause_seconds=pauses,explicit_pause_total=sum(pauses),script_sha256=hashlib.sha256(json.dumps(s,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
(R/'production/af-heart/scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2));(R/'editorial/narration-review-v0.1.2.json').write_text(json.dumps(dict(scope='All 149 clips after the approved opening story',reviewed=len(audit),revised=sum(x['status']=='revised'for x in audit),clips=audit),ensure_ascii=False,indent=2))
print('Reviewed',len(audit),'clips; revised',sum(x['status']=='revised'for x in audit),'retained',sum(x['status']=='retained'for x in audit))
print('Speech markers:',sum(len(x['pause_seconds'])for x in audit),'extra silence seconds:',round(sum(x['explicit_pause_total']for x in audit),1))
