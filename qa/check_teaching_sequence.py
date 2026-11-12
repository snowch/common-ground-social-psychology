"""Check the complete narrated teaching sequence, promotions and legacy bookmarks."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
COURSE=json.loads((ROOT/'course.json').read_text())
CLIPS={s['id']:s for s in json.loads((ROOT/'audio/manifest.json').read_text())['clips']}
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
def token(s):return s['id'].split('s')[1].lstrip('0')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  teaching_count=played=0
  for c in COURSE:
   teaching=[s for s in c['slides'] if s['kind'] in ['concept','evidence']]
   await page.goto(BASE+f"/#chapter-{c['number']}-slide-{token(teaching[0])}")
   for s in teaching:
    await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=s['title'])
    assert await page.locator('.slide-number').inner_text()==f"{c['slides'].index(s)+1} / {len(c['slides'])}"
    assert await page.locator('.more-visuals').count()==0,s['id']
    assert await page.locator('.slide-art>svg').get_attribute('data-diagram')==s['visual'],s['id']
    if s['id'][-1].isalpha():
     await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.05')
     assert abs(await page.evaluate('audioPlayer.duration')-CLIPS[s['id']]['duration'])<.04,s['id']
     assert await page.evaluate('(id)=>audioPlayer.src.includes(id)',s['id'])
     await page.locator('#stop').click();played+=1
    teaching_count+=1;await page.locator('#next').click()
   await page.wait_for_selector('.choices');assert page.url.endswith(f"#chapter-{c['number']}-slide-6")
   await page.locator('#prev').click();await page.wait_for_url('**/#chapter-'+str(c['number'])+'-slide-'+token(teaching[-1]))
   await page.goto(BASE+f"/#chapter-{c['number']}-slide-8");await page.locator('#next').click()
   if c['number']<10:
    await page.wait_for_url('**/#chapter-'+str(c['number']+1)+'-slide-1');await page.locator('#prev').click();await page.wait_for_url('**/#chapter-'+str(c['number'])+'-slide-8')
   else:await page.locator('.case-wrap').wait_for()
  # A newly inserted c-suffix page must be resumable, with its visit retained.
  await page.goto(BASE+'/#chapter-2-slide-3c');await page.goto(BASE+'/#home');await page.reload();await page.locator('#resume').click();await page.wait_for_url('**/#chapter-2-slide-3c')
  assert await page.evaluate('JSON.parse(localStorage.getItem("common-ground-v1")).visited.c02s03c===true')
  # Old eight-page positions still resolve to their stable original identities.
  for chapter in [2,6,10]:
   await page.evaluate('(chapter)=>localStorage.setItem("common-ground-v1",JSON.stringify({position:{chapter,slide:3},answers:{c02s06:1},checked:{c02s06:true},visited:{c01s03b:true}}))',chapter)
   await page.goto(BASE+'/#home');await page.reload();await page.locator('#resume').click();await page.wait_for_url('**/#chapter-'+str(chapter)+'-slide-4')
  await page.goto(BASE+'/#chapter-2-slide-6');assert await page.locator('[data-answer="1"]').get_attribute('aria-pressed')=='true'
  await page.set_viewport_size({'width':768,'height':1000})
  for chapter,step in [(2,'3c'),(2,'4b'),(6,'4b'),(7,'4b'),(9,'4b'),(10,'3b')]:
   await page.goto(BASE+f'/#chapter-{chapter}-slide-{step}');await page.evaluate('document.fonts.ready');await page.screenshot(path=str(ROOT/f'out/course-page-{chapter}-{step}.png'),full_page=True)
  await page.goto(BASE+'/chapters/chapter-02.html#chapter-2-slide-3c');assert await page.locator('#slideTitle').inner_text()=='Select people. Assign conditions.'
  assert not errors,errors;await b.close()
 result={'chapters_reviewed':len(COURSE),'teaching_pages':teaching_count,'independent_added_pages_played':played,'sequence_and_chapter_boundaries':'passed','legacy_bookmarks_and_resume':'passed','c_suffix_resume':'passed','saved_choices':'passed','standalone_chapter':'passed','js_errors':errors}
 (ROOT/'qa/teaching-sequence-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
asyncio.run(main())
