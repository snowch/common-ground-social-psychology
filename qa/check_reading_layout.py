"""Check paragraph rendering, glossary controls, and expanded teaching figures."""
import asyncio, os, json
from pathlib import Path
COURSE=json.loads((Path(__file__).resolve().parents[1]/'course.json').read_text())
from playwright.async_api import async_playwright
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(reduced_motion='reduce'); errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/#chapter-1-slide-5')
  assert await page.locator('.evidence-body p').count()==3
  assert (await page.locator('.evidence-body p').first.inner_text()).strip()==COURSE[0]['evidence'].split('\n\n')[0]
  term=page.locator('.evidence-body .glossary-term').filter(has_text='Attribution research')
  await term.focus();await page.keyboard.press('Enter')
  assert 'patterns across' in await page.locator(':popover-open').inner_text()
  await page.keyboard.press('Escape');assert await term.evaluate('(e)=>e===document.activeElement')
  for width in [320,390,768,1024,1440]:
   await page.set_viewport_size({'width':width,'height':1000})
   for c in COURSE:
    chapter=c['number']
    for pos,s in enumerate(c['slides'],1):
     slide=s['id'].split('s')[1].lstrip('0')
     await page.evaluate('(h)=>location.hash=h',f'chapter-{chapter}-slide-{slide}')
     await page.locator(f'.slide[aria-label^="Chapter {chapter},"]').wait_for()
     await page.wait_for_function('(n)=>document.querySelector(".slide-number").textContent===n',arg=f"{pos} / {len(c['slides'])}")
     if await page.locator('.more-visuals').count():await page.locator('.more-visuals').evaluate('(e)=>e.open=true')
     assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,chapter,slide)
     if s['kind'] in ['concept','evidence']:
      assert await page.locator('.slide-art').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1'),(width,chapter,slide)
      for figure in await page.locator('.more-visuals figure').all():
       assert await figure.evaluate('(e)=>{const r=e.getBoundingClientRect(),p=e.closest(".slide-art").getBoundingClientRect();return r.left>=p.left&&r.right<=p.right+1}'),(width,chapter,slide)
   print(f'Passed all {sum(len(c["slides"]) for c in COURSE)} slides at {width}px',flush=True)
  assert not errors,errors
  await browser.close()
asyncio.run(main())
