"""Verify optional research and evidence-based transfer tasks throughout the course."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];C=json.loads((R/'course.json').read_text());BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/');AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))
TEACHING=[(c,s)for c in C for s in c['slides']if s['kind']in ['concept','evidence']]
async def main():
 errors=[];audits=[];expanded=0
 assert len(TEACHING)==48 and all(s.get('research',{}).get('sources')for _,s in TEACHING)
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(BASE+'/#home');await page.add_script_tag(path=str(AXE))
  async def goto(c,s):
   token=s['id'].split('s')[1].lstrip('0');await page.evaluate('(h)=>location.hash=h',f"chapter-{c['number']}-slide-{token}")
   await page.wait_for_function('([label,title])=>document.querySelector("#app .slide")?.getAttribute("aria-label")===label&&document.querySelector("#slideTitle")?.textContent===title',arg=[f"Chapter {c['number']}, {s['stage']}",s['title']])
  for width in [320,390,768,1440]:
   await page.set_viewport_size({'width':width,'height':1000})
   for c,s in TEACHING:
    await goto(c,s);details=page.locator('.lesson-research');assert await details.get_attribute('open') is None,s['id'];assert not await page.locator('.research-content').is_visible();assert await page.locator('.chapter-reading').get_attribute('open') is None
    summary=details.locator('summary');await summary.focus();await page.keyboard.press('Enter');assert await page.locator('.research-content').is_visible()
    assert await page.locator('.research-content a').evaluate_all('els=>els.map(e=>e.href)')==[r['url']for r in s['research']['sources']],s['id']
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,s['id'])
    if width==390:
     issues=await page.evaluate('''async()=>{const r=await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))}''');assert not issues,(s['id'],issues);audits.append({'slide':s['id'],'violations':issues})
    await page.keyboard.press('Enter');assert await details.get_attribute('open') is None;expanded+=1
   print('All 48 research disclosures passed at',width,'px',flush=True)
  # Old choices for replaced transfers clear; unrevised first decisions and the
  # current Chapter 1 transfer remain valid, including in shared chapter storage.
  old={f'c{n:02d}s{k:02d}':1 for n in range(1,11)for k in [2,6]}
  await page.evaluate('(answers)=>localStorage.setItem("common-ground-v1",JSON.stringify({answers,checked:Object.fromEntries(Object.keys(answers).map(k=>[k,true])),answerRevisions:{c01s06:"attribution-evidence-v2"},reasoning:{c01s06:"Keep the early start comparable."},visited:{c02s03c:true},position:{chapter:2,slide:5}}))',old)
  await page.goto(BASE+'/#home');await page.reload();await page.locator('#resume').click();await page.wait_for_url('**/#chapter-2-slide-6');assert await page.locator('.option[aria-pressed="true"]').count()==0
  saved=await page.evaluate('JSON.parse(localStorage.getItem("common-ground-v1"))')
  assert all(saved['answers'][f'c{n:02d}s02']==1 for n in range(1,11));assert saved['answers']['c01s06']==1 and saved['reasoning']['c01s06'];assert all(f'c{n:02d}s06' not in saved['answers']for n in range(2,11));assert saved['visited']['c02s03c']
  # Every chapter's revised task offers three reasoned feedback variants and
  # retains an escaped written response across choices, reloads and files.
  for c in C:
   s=next(s for s in c['slides']if s['kind']=='transfer');await goto(c,s)
   text=f"Chapter {c['number']}: distinguish the process, compare relevant evidence, and retain uncertainty. <script>throw Error('unsafe')</script>"
   await page.locator('#decisionReasoning').fill(text);await page.locator('#decisionReasoning').press('ArrowRight');assert page.url.endswith(f"chapter-{c['number']}-slide-6")
   for index,feedback in enumerate(s['quiz']['feedback']):
    await page.locator(f'[data-answer="{index}"]').click();assert await page.locator('#decisionReasoning').input_value()==text;assert not await page.locator('#playFeedback').is_visible();await page.locator('#checkChoice').click();assert feedback in await page.locator('.feedback').inner_text()
   await page.reload();assert await page.locator('#decisionReasoning').input_value()==text;assert await page.locator('[data-answer="2"]').get_attribute('aria-pressed')=='true';assert not await page.locator('.reasoning-field script').count()
   await page.goto(BASE+f"/chapters/chapter-{c['number']:02d}.html#chapter-{c['number']}-slide-6");assert await page.locator('#decisionReasoning').input_value()==text
   await page.goto(BASE+'/#home')
  saved=await page.evaluate('JSON.parse(localStorage.getItem("common-ground-v1"))');assert len(saved['reasoning'])==10
  await page.evaluate('buildPrint()');assert await page.locator('#print .print-research-sources').count()==48;assert await page.locator('#print .reasoning-print').count()==10;assert not await page.locator('#print .lesson-research,#print textarea').count()
  await page.goto(BASE+'/study-guide.html');assert await page.locator('.research-notes').count()==10;assert await page.locator('.research-topic').count()==48
  assert await page.locator('.guide-contents a').count()==10
  for n in range(1,11):assert await page.locator(f'#study-chapter-{n}').count()==1
  assert not errors,errors;await b.close()
 report={'chapters':10,'teaching_pages_with_optional_research':48,'expanded_checks':expanded,'widths':[320,390,768,1440],'expanded_research_axe_audits':len(audits),'axe_violations':sum(len(a['violations'])for a in audits),'written_transfer_tasks':10,'transfer_feedback_variants':30,'old_replaced_choices':'cleared; original decisions and current Chapter 1 response retained','written_responses_across_standalone_files':'passed','response_escaping':'passed','research_print_sources':48,'study_companion_research_topics':48,'study_companion_chapter_links':10,'js_errors':errors}
 (R/'qa/course-academic-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
asyncio.run(main())
