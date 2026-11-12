"""Check the independent explanation lesson and preserved bookmarks/progress."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
FIRST=json.loads((ROOT/'course.json').read_text())[0]['slides']
def position(id):return f"{next(i+1 for i,s in enumerate(FIRST) if s['id']==id)} / {len(FIRST)}"
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  # All teaching steps are now visible in the normal sequence.
  await page.goto(BASE+'/#chapter-1-slide-1')
  for i,slide in enumerate(FIRST):
   await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=slide['title'])
   assert await page.locator('.slide-number').inner_text()==position(slide['id'])
   if slide['kind'] in ['concept','evidence']:assert await page.locator('.more-visuals').count()==0
   if slide['id'] in ['c01s03b','c01s04b']:
    await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1')
    expected=next(s['duration'] for s in json.loads((ROOT/'audio/manifest.json').read_text())['clips'] if s['id']==slide['id'])
    assert abs(await page.evaluate('audioPlayer.duration')-expected)<.04
    await page.locator('#stop').click()
   if i+1<len(FIRST):await page.locator('#next').click()
  await page.goto(BASE+'/#chapter-1-slide-5');assert await page.locator('.more-visuals').count()==0
  await page.locator('#next').click();await page.wait_for_url('**/#chapter-1-slide-5b');assert await page.locator('#slideTitle').inner_text()=='Test the explanation.'
  assert await page.locator('.slide-number').inner_text()==position('c01s05b')
  await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1');assert await page.evaluate('audioPlayer.src.includes("c01s05b")')
  expected=next(s['duration'] for s in json.loads((ROOT/'audio/manifest.json').read_text())['clips'] if s['id']=='c01s05b')
  assert abs(await page.evaluate('audioPlayer.duration')-expected)<.04
  await page.locator('#next').click();await page.wait_for_url('**/#chapter-1-slide-6');assert await page.locator('.choices').count()==1;assert await page.evaluate('audioPlayer===null')
  await page.locator('#prev').click();await page.wait_for_url('**/#chapter-1-slide-5b')
  await page.reload();assert await page.locator('#slideTitle').inner_text()=='Test the explanation.'
  await page.goto(BASE+'/#chapter-1-slide-8');assert await page.locator('.slide-number').inner_text()==position('c01s08')
  await page.locator('#next').click();await page.wait_for_url('**/#chapter-2-slide-1');await page.locator('#prev').click();await page.wait_for_url('**/#chapter-1-slide-8')
  # Legacy position 5 meant the transfer decision, not the new lesson.
  await page.evaluate('localStorage.setItem("common-ground-v1",JSON.stringify({position:{chapter:1,slide:5},visited:{c01s05:true},answers:{c01s06:1},checked:{c01s06:true}}))')
  await page.goto(BASE+'/#home');await page.reload();await page.locator('#resume').click();await page.wait_for_url('**/#chapter-1-slide-6');assert await page.locator('[data-answer="1"]').get_attribute('aria-pressed')=='true'
  await page.goto(BASE+'/#chapter-1-slide-5b');await page.goto(BASE+'/#home');await page.locator('#resume').click();await page.wait_for_url('**/#chapter-1-slide-5b')
  for width in [320,390,768,1440]:
   await page.set_viewport_size({'width':width,'height':1000});assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.set_viewport_size({'width':768,'height':1000});await page.evaluate('document.fonts.ready');await page.screenshot(path=str(ROOT/'out/new-lesson-tablet.png'),full_page=True)
  await page.set_viewport_size({'width':1440,'height':1000});await page.screenshot(path=str(ROOT/'out/new-lesson-desktop.png'),full_page=True)
  await page.set_viewport_size({'width':768,'height':1000})
  for token in ['3b','4','4b']:
   await page.goto(BASE+f'/#chapter-1-slide-{token}');await page.evaluate('document.fonts.ready');await page.screenshot(path=str(ROOT/f'out/chapter-one-{token}.png'),full_page=True)
  await page.evaluate('(()=>{const s=JSON.parse(localStorage.getItem("common-ground-v1"));s.visited.c02s01=true;localStorage.setItem("common-ground-v1",JSON.stringify(s))})()')
  await page.goto(BASE+'/chapters/chapter-01.html#chapter-1-slide-5b');assert await page.locator('#slideTitle').inner_text()=='Test the explanation.'
  assert await page.evaluate('JSON.parse(localStorage.getItem("common-ground-v1")).visited.c02s01===true')
  assert not errors,errors;await b.close()
 print('Chapter 1 sequence, independent lessons, playback, bookmarks, saved progress, responsive layout and standalone chapter passed.')
asyncio.run(main())
