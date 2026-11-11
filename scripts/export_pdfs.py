from pathlib import Path
import asyncio,json,os
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
async def main():
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(viewport={'width':1280,'height':720},reduced_motion='reduce')
  await page.goto(BASE+'/index.html');await page.evaluate('buildPrint()');await page.emulate_media(media='print');await page.evaluate('document.fonts.ready')
  bad=await page.locator('#print .slide').evaluate_all('''els=>els.flatMap((el,i)=>{const r=el.getBoundingClientRect();return [...el.querySelectorAll('.slide-copy h2,.slide-points,.evidence-body,.choices,.feedback,.answers,.practice-tip,.scene-tag')].filter(x=>{const a=x.getBoundingClientRect();return a.bottom>r.bottom-5||a.right>r.right+1}).map(x=>({slide:i+1,element:x.className||x.tagName,bottom:x.getBoundingClientRect().bottom-r.bottom}));})''')
  print('Overflow:',bad,flush=True)
  assert not bad,bad
  await page.pdf(path=str(R/'common-ground-slides.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  for n in range(1,11):await page.pdf(path=str(R/f'chapters/chapter-{n:02d}.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True,page_ranges=f'{(n-1)*8+1}-{n*8}')
  (R/'qa/course-review-pdf.json').write_text(json.dumps(dict(pages=80,chapter_pdfs=10,overflow=bad,content_revision='v0.2.0'),indent=2))
  await page.goto(BASE+'/study-guide.html');await page.evaluate('document.fonts.ready')
  await page.pdf(path=str(R/'study-guide.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  print('Updated 80-slide PDF, ten chapter PDFs and study companion.',flush=True);await b.close()
asyncio.run(main())
