import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1,reduced_motion='reduce')
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto((os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')+'/index.html'));await page.evaluate('document.fonts.ready')
  await page.screenshot(path=str(R/'qa/cover.png'),full_page=True)
  assert await page.locator('.chapter').count()==10
  await page.locator('#start').click();await page.wait_for_selector('.slide.story')
  await page.screenshot(path=str(R/'qa/story.png'),full_page=True)
  await page.locator('#next').click();await page.wait_for_selector('.choices')
  await page.locator('[data-answer="1"]').click();await page.locator('#checkChoice').click()
  assert 'One episode' in await page.locator('.feedback').inner_text()
  await page.locator('[data-answer="0"]').click();await page.locator('#checkChoice').click()
  assert 'Good application' in await page.locator('.feedback').inner_text()
  await page.screenshot(path=str(R/'qa/decision.png'),full_page=True)
  await page.locator('#next').click();await page.wait_for_selector('.slide.concept')
  await page.screenshot(path=str(R/'qa/concept.png'),full_page=True)
  C=json.loads((R/'course.json').read_text())
  checked=0
  for c in C:
   for j,s in enumerate(c['slides']):
    await page.evaluate('(h)=>{location.hash=h}',f"chapter-{c['number']}-slide-{j+1}")
    await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=s['title'])
    assert await page.locator('.slide').count()==1
    if 'quiz' in s:
     for k in range(3):
      await page.locator(f'[data-answer="{k}"]').click();await page.locator('#checkChoice').click()
      assert s['quiz']['feedback'][k] in await page.locator('.feedback').inner_text()
     checked+=1
    if s['kind']=='recall':
     await page.locator('#reveal').click()
     assert s['answers'][0] in await page.locator('.answers').inner_text()
    bounds=await page.locator('.slide-copy').evaluate('(e)=>({s:e.scrollHeight,c:e.clientHeight})')
    assert bounds['s']<=bounds['c']+1,(c['number'],j,bounds)
  await page.reload();await page.wait_for_selector('.slide.practice')
  # Recorded audio transport has its own real-playback check in check_recorded_audio.py.
  assert await page.evaluate('Object.keys(RECORDED_AUDIO).length')==150
  # Mobile overflow and layout.
  await page.set_viewport_size({'width':390,'height':844})
  for n in [1,2,3,5,7,8]:
   await page.evaluate('(h)=>location.hash=h',f'chapter-1-slide-{n}')
   await page.wait_for_function('(n)=>document.querySelector(".slide-number")?.textContent.trim()===n+" / 8"',arg=n)
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),n
  await page.evaluate('location.hash="chapter-1-slide-5"');await page.wait_for_selector('.slide.evidence')
  await page.screenshot(path=str(R/'qa/mobile-evidence.png'),full_page=True)
  await page.evaluate('location.hash="home"');await page.wait_for_selector('.hero')
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.screenshot(path=str(R/'qa/mobile-cover.png'),full_page=True)
  # Print-ready full deck.
  await page.set_viewport_size({'width':1280,'height':720})
  await page.evaluate('buildPrint()');await page.evaluate('document.fonts.ready')
  assert await page.locator('#print .slide').count()==80
  await page.pdf(path=str(R/'common-ground-slides.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  # A 4K slide export suitable as the first recording input.
  await page.goto((os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')+'/index.html')+'#chapter-1-slide-1');await page.wait_for_selector('.slide.story')
  await page.emulate_media(media='screen',reduced_motion='reduce')
  await page.add_style_tag(content='.slide{width:1280px;height:720px;min-height:720px;border:0;border-radius:0}.player{padding:0}.slide-copy{padding:50px}.slide-art{padding:35px}')
  await page.locator('#app .slide').screenshot(path=str(R/'qa/slide-preview.png'))
  # Verify a chapter deck is self-contained and works without fetching course data.
  await page.goto((os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')+'/chapters/chapter-10.html'));await page.wait_for_selector('.slide.story')
  assert 'Who will do something?' in await page.locator('.player-title').inner_text()
  assert not errors,errors
  result=dict(chapters=10,slides=80,decisions_checked=checked,feedback_variants_checked=checked*3,recall_reveals_checked=10,mobile_width=390,js_errors=errors,narration_controls='See af-heart-browser-results.json for real AAC playback checks',pdf='exported',standalone_chapter='passed')
  (R/'qa/results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
  await browser.close()
asyncio.run(main())
