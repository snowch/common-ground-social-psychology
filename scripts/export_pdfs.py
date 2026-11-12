from pathlib import Path
import argparse,asyncio,json,os
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
parser=argparse.ArgumentParser(description='Export the current course PDFs from a running preview.');parser.add_argument('--revision',default='working-tree');args=parser.parse_args()
async def main():
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(viewport={'width':1280,'height':720},reduced_motion='reduce')
  await page.goto(BASE+'/index.html');await page.evaluate('buildPrint()');await page.emulate_media(media='print');await page.evaluate('document.fonts.ready')
  bad=await page.locator('#print .slide').evaluate_all('''els=>els.flatMap((el,i)=>{const r=el.getBoundingClientRect();return [...el.querySelectorAll('.slide-copy h2,.slide-points,.evidence-body,.choices,.feedback,.answers,.practice-tip,.scene-tag')].filter(x=>{const a=x.getBoundingClientRect();return a.bottom>r.bottom-5||a.right>r.right+1}).map(x=>({slide:i+1,element:x.className||x.tagName,bottom:x.getBoundingClientRect().bottom-r.bottom}));})''')
  print('Overflow:',bad,flush=True)
  assert not bad,bad
  await page.pdf(path=str(R/'common-ground-slides.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  for n in range(1,11):await page.pdf(path=str(R/f'chapters/chapter-{n:02d}.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True,page_ranges=f'{(n-1)*8+1}-{n*8}')
  (R/'qa/course-review-pdf.json').write_text(json.dumps(dict(pages=80,chapter_pdfs=10,overflow=bad,content_revision=args.revision),indent=2))
  await page.goto(BASE+'/study-guide.html');await page.evaluate('document.fonts.ready')
  await page.pdf(path=str(R/'study-guide.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  await page.goto(BASE+'/visual-guide.html');await page.evaluate('document.fonts.ready')
  count=await page.locator('.visual-card').count();assert count>=30
  bad_visuals=await page.locator('.visual-card').evaluate_all('els=>els.filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>e.id)')
  assert not bad_visuals,bad_visuals
  await page.pdf(path=str(R/'visual-guide.pdf'),prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
  print(f'Updated 80-slide PDF, ten chapter PDFs, study companion, and {count}-figure visual companion.',flush=True);await b.close()
asyncio.run(main())
