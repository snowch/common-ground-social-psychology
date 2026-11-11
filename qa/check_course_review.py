"""Whole-course regression checks. Requires Playwright, Chromium and a local axe-core file."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/');AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))
async def main():
 assert AXE.exists(),'Set AXE_SCRIPT to axe-core 4.10.3 axe.min.js (MIT).'
 C=json.loads((R/'course.json').read_text());scenes=json.loads((R/'production/af-heart/scenes.json').read_text());evidence=json.loads((R/'course-evidence.json').read_text());case=json.loads((R/'learning-check.json').read_text())
 assert len(scenes)==150 and len(evidence)==10 and len(case['tasks'])==6
 assert set(n for t in case['tasks']for n in t['chapters'])==set(range(1,11))
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);page=await b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/index.html');await page.add_script_tag(path=str(AXE));audits=[]
  async def audit(label):
   issues=await page.evaluate('''async()=>{let r=await axe.run(document.querySelector('#app'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}));}''')
   audits.append({'screen':label,'violations':issues});assert not issues,(label,issues)
  await audit('home')
  for c in C:
   for j,s in enumerate(c['slides']):
    await page.evaluate('(h)=>location.hash=h',f"chapter-{c['number']}-slide-{j+1}");await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=s['title'])
    assert await page.evaluate('document.activeElement.id')=='slideTitle',s['id']
    reading=page.locator('.chapter-reading')
    assert (await reading.get_attribute('open') is not None)==(s['kind']=='evidence')
    if await reading.get_attribute('open') is None:await reading.locator('summary').first.click()
    assert await page.locator('.evidence-note').inner_text() and evidence[str(c['number'])]['note'] in await page.locator('.evidence-note').inner_text()
    text=await page.locator('.transcript details > p').first.inner_text();assert '[pause' not in text and '](/' not in text
    if 'quiz'in s:
     await page.locator('[data-answer="0"]').click();assert 'explain why' in await page.locator('.feedback').inner_text();assert not await page.locator('#playFeedback').count()
     # Selecting alone must not leak feedback through the audio queue.
     await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.02');await page.evaluate("audioPlayer.dispatchEvent(new Event('ended'))");assert await page.evaluate('!playing')
     await page.locator('#checkChoice').click();assert s['quiz']['feedback'][0] in await page.locator('.feedback').inner_text();assert 'Option A.' in text and 'Option C.'in text
     assert await page.locator('#playFeedback').count()==1
     await page.locator('#playFeedback').click();assert await page.evaluate('(id)=>audioPlayer.src===new URL(RECORDED_AUDIO[id+"-feedback-0"],location.href).href',s['id']);await page.locator('#stop').click()
    await audit(s['id'])
  await page.evaluate("location.hash='case'");await page.wait_for_selector('.case-wrap');assert await page.locator('.case-wrap ol li').count()==6;assert not await page.locator('.case-wrap details').first.get_attribute('open');await audit('case')
  await page.screenshot(path=str(R/'qa/course-case.png'),full_page=True)
  await page.evaluate("location.hash='about'");await page.wait_for_selector('#main h1');await audit('about')
  await page.locator('.skip').focus();await page.keyboard.press('Enter');assert await page.evaluate('document.activeElement.id')=='main';assert await page.evaluate('location.hash')=='#about'
  # Browser back/forward restores the destination heading, not a removed control.
  await page.evaluate('history.back()');await page.wait_for_selector('.case-wrap');await page.evaluate('history.forward()');await page.wait_for_function('document.querySelector("#main h1")?.textContent==="About Common Ground"')
  await page.evaluate('buildPrint()');assert await page.locator('#print .slide').count()==80
  assert await page.evaluate('''()=>{let ids=[...document.querySelectorAll('[id]')].map(x=>x.id);return ids.length===new Set(ids).size}''')
  # Corrupted saved values must not make Resume crash.
  await page.evaluate('''localStorage.setItem('common-ground-v1',JSON.stringify({position:{chapter:1,slide:'bad'},answers:{c01s02:50},visited:{c01s01:'yes'}}))''');await page.goto(BASE+'/index.html#home');await page.reload();await page.locator('#resume').click();await page.wait_for_selector('#slideTitle');assert await page.locator('.slide-number').inner_text()=='1 / 8'
  for width in [320,390,768,1440]:
   await page.set_viewport_size({'width':width,'height':900})
   for hash in ['home','chapter-1-slide-2','chapter-2-slide-3','chapter-8-slide-5','case','about']:
    await page.evaluate('(h)=>location.hash=h',hash);await page.wait_for_timeout(40);assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,hash)
   await page.evaluate("location.hash='case'");await page.wait_for_selector('.case-wrap');await page.locator('.case-wrap summary').first.click();assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  # Denied storage remains usable and tells the learner progress is temporary.
  denied=await b.new_context();await denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied','SecurityError')}})");dp=await denied.new_page();await dp.goto(BASE+'/index.html#chapter-1-slide-1');assert 'unavailable' in await dp.locator('.progress-caption').inner_text();await denied.close()
  await page.goto(BASE+'/study-guide.html');await page.evaluate('document.fonts.ready');assert await page.locator('section.chapter').count()==10;await page.pdf(path=str(R/'study-guide.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  assert not errors,errors
  out={'revision':'v0.4.0','native_evidence_disclosures':'passed','chapters_reviewed':10,'slides_checked':80,'source_notes':10,'written_transfer_tasks':6,'rubric_dimensions':4,'axe_version':'4.10.3','axe_tags':['wcag2a','wcag2aa','wcag21aa','wcag22aa'],'axe_screens':len(audits),'axe_violations':sum(len(x['violations'])for x in audits),'widths':[320,390,768,1440],'navigation_focus':'passed','feedback_gating_and_direct_play':'passed','corrupt_and_denied_storage':'passed','unique_print_ids':'passed','js_errors':errors,'limits':'Automated Chromium checks do not establish full WCAG conformance or usability with assistive technology.'}
  (R/'qa/course-review-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));await b.close()
asyncio.run(main())
