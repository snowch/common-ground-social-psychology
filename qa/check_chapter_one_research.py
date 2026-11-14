"""Check optional research, visible qualifications, written reasoning and saved-state migration."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
C=json.loads((R/'course.json').read_text())[0]
PAGES=[s for s in C['slides'] if s.get('research')]
AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))
async def main():
 errors=[];audits=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/#chapter-1-slide-3');await page.add_script_tag(path=str(AXE))
  for width in [320,390,768,1024,1440]:
   await page.set_viewport_size({'width':width,'height':1000})
   for s in PAGES:
    token=s['id'].split('s')[1].lstrip('0');await page.evaluate('(h)=>location.hash=h','chapter-1-slide-'+token)
    await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=s['title'])
    details=page.locator('.lesson-research');assert await details.count()==1 and await details.get_attribute('open') is None,s['id']
    assert not await page.locator('.research-content').is_visible()
    assert await page.locator('.chapter-reading').get_attribute('open') is None
    if s['id']=='c01s05':
     assert 'not a general rule' in await page.locator('.evidence-body').inner_text()
     assert 'positive and negative events' in await page.locator('.evidence-body').inner_text()
    summary=details.locator('summary');await summary.focus();await page.keyboard.press('Enter');assert await page.locator('.research-content').is_visible()
    assert await page.locator('.research-content a').count()==len(s['research']['sources'])
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,s['id'])
    if width<=900:
     assert await page.evaluate('''()=>{const copy=document.querySelector('.slide-copy').getBoundingClientRect(),nav=document.querySelector('.player-controls').getBoundingClientRect(),art=document.querySelector('.slide-art').getBoundingClientRect();return copy.bottom<=nav.top+1&&nav.bottom<=art.top+1}'''),(width,s['id'])
    if width==390:
     issues=await page.evaluate('''async()=>{const r=await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))}''');assert not issues,(s['id'],issues);audits.append({'slide':s['id'],'violations':issues})
    await page.keyboard.press('Enter');assert await details.get_attribute('open') is None
  # Existing answers for the replaced exercise must not acquire new meanings.
  await page.evaluate('''localStorage.setItem('common-ground-v1',JSON.stringify({answers:{c01s02:0,c01s06:1,c02s06:1},checked:{c01s02:true,c01s06:true,c02s06:true},position:{chapter:1,slide:5},visited:{c01s05b:true}}))''')
  await page.goto(BASE+'/#home');await page.reload();await page.goto(BASE+'/#chapter-1-slide-6')
  assert await page.locator('.option[aria-pressed="true"]').count()==0
  assert await page.locator('#checkChoice').is_disabled()
  saved=await page.evaluate('JSON.parse(localStorage.getItem("common-ground-v1"))');assert 'c01s06' not in saved['answers'] and saved['answers']['c01s02']==0 and saved['answers']['c02s06']==1 and saved['visited']['c01s05b']
  assert await page.locator('.quiz-record tbody tr').count()==2
  assert 'Invented teaching record' in await page.locator('.quiz-record caption').inner_text()
  text='Keep the early start similar; compare bus availability. Other conditions can still differ. <script>throw Error("unsafe")</script>'
  await page.locator('#decisionReasoning').fill(text);await page.locator('#decisionReasoning').press('ArrowLeft');assert page.url.endswith('chapter-1-slide-6')
  for index,feedback in enumerate(C['quizzes'][1]['feedback']):
   await page.locator(f'[data-answer="{index}"]').click();assert await page.locator('#decisionReasoning').input_value()==text
   assert not await page.locator('#playFeedback').count();await page.locator('#checkChoice').click();assert feedback in await page.locator('.feedback').inner_text()
  await page.reload();assert await page.locator('#decisionReasoning').input_value()==text;assert await page.locator('[data-answer="2"]').get_attribute('aria-pressed')=='true'
  assert not await page.locator('.reasoning-field script').count()
  await page.goto(BASE+'/chapters/chapter-02.html');await page.locator('#next').click();await page.locator('[data-answer="1"]').click()
  await page.goto(BASE+'/chapters/chapter-01.html#chapter-1-slide-6');assert await page.locator('#decisionReasoning').input_value()==text
  assert await page.locator('[data-answer="2"]').get_attribute('aria-pressed')=='true'
  await page.evaluate('buildPrint()');assert await page.locator('#print .lesson-research').count()==0;assert await page.locator('#print #decisionReasoning').count()==0
  assert await page.locator('#print .quiz-record').count()==1
  assert await page.locator('#print .print-research-sources').count()==len(PAGES)
  assert any('Jones & Harris (1967)' in t for t in await page.locator('#print .print-research-sources').all_inner_texts())
  assert 'not a general rule' in await page.locator('#print .evidence-body').first.inner_text()
  assert await page.locator('#print .reasoning-print').count()==1
  await page.goto(BASE+'/study-guide.html');assert await page.locator('.research-notes .research-topic').count()==len(PAGES)
  assert await page.locator('.research-notes a[href="https://doi.org/10.1037/0033-2909.132.6.895"]').count()==1
  await page.goto(BASE+'/chapters/chapter-01.html#chapter-1-slide-5');assert await page.locator('.lesson-research').get_attribute('open') is None
  await page.locator('.lesson-research summary').click();assert '173 published studies' in await page.locator('.research-content').inner_text()
  assert not errors,errors;await b.close()
 result={'chapter':1,'teaching_disclosures':len(PAGES),'research_default':'collapsed','essential_qualification':'visible on screen and in print','widths':[320,390,768,1024,1440],'expanded_research_axe_audits':audits,'stacked_controls':'between text and illustration','three_comparison_feedbacks':'passed','written_reasoning_restore_and_escaping':'passed','cross_chapter_standalone_response_retention':'passed','replaced_exercise_migration':'old answer cleared; other answers and visits retained','research_in_study_companion':'passed','standalone_chapter':'passed','js_errors':errors}
 (R/'qa/chapter-one-research-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
asyncio.run(main())
