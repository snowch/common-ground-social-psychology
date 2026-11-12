"""Check complete visual coverage, expanded figures, accessibility, and PDF export."""
import asyncio, json, os, re, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))

def normal(text):
 return re.sub(r'\s+',' ',re.sub(r'(?<=[-–—])\s*\n\s*','',text)).strip().casefold()

async def bounds(svg):
 return await svg.evaluate('''svg=>[...svg.querySelectorAll('text')].filter(t=>{const r=t.getBBox(),m=svg.getScreenCTM().inverse().multiply(t.getScreenCTM()),v=svg.viewBox.baseVal;return [[r.x,r.y],[r.x+r.width,r.y],[r.x,r.y+r.height],[r.x+r.width,r.y+r.height]].some(([x,y])=>{const p=new DOMPoint(x,y).matrixTransform(m);return p.x<0||p.y<0||p.x>v.width||p.y>v.height})}).map(t=>t.textContent)''')

async def audit(page):
 issues=await page.evaluate('''async()=>{const r=await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))}''')
 assert not issues,issues
 return issues

async def main():
 assert AXE.is_file(),'Set AXE_SCRIPT to a local axe-core script.'
 (ROOT/'out').mkdir(exist_ok=True)
 course=json.loads((ROOT/'course.json').read_text())
 expected={s['id'] for c in course for s in c['slides'] if s['kind'] in ['concept','evidence']}
 required=json.loads((ROOT/'qa/essential-terms.json').read_text())
 errors=[];checks=[];audits=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await browser.new_page(reduced_motion='reduce')
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/visual-guide.html');await page.evaluate('document.fonts.ready');await page.add_script_tag(path=str(AXE))
  manifest=await page.evaluate('Object.fromEntries(Object.entries(visualLessons).map(([k,vs])=>[k,vs.map(v=>({key:v.key,title:v.title,terms:v.terms}))]))')
  assert set(manifest)==expected,(set(manifest)^expected)
  views=[v for vs in manifest.values() for v in vs];assert len({v['key'] for v in views})==len(views)
  for key,terms in required.items():
   declared=[normal(t) for v in manifest[key] for t in v['terms']]
   assert all(normal(term) in declared for term in terms),(key,terms,declared)
  assert await page.locator('.visual-card').count()==len(views)
  for width in [320,390,768,1440]:
   await page.set_viewport_size({'width':width,'height':1000});await page.evaluate('document.fonts.ready')
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
   for v in views:
    card=page.locator('#'+v['key']);svg=card.locator('svg');assert await svg.count()==1,v['key']
    clipped=await bounds(svg);assert not clipped,(width,v['key'],clipped)
    if width==1440:
     text=normal(' '.join([await card.locator('h3').inner_text(),await card.locator('figcaption').inner_text(),*await svg.locator('text').all_text_contents()]))
     assert all(normal(term) in text for term in v['terms']),(v['key'],v['terms'],text)
     await svg.screenshot(path=str(ROOT/f"out/visual-{v['key']}.png"))
    checks.append({'visual':v['key'],'width':width,'clipped_text':clipped})
   if width in [390,1440]:audits.append({'screen':'visual-guide','width':width,'violations':await audit(page)})
  # Same illustrative cases, with different emphasis.
  groups=page.locator('#confirmation-bias [data-evidence-record]');records=await groups.evaluate_all('els=>els.map(e=>e.dataset.evidenceRecord)');assert records[0]==records[1]
  for g,focus in zip(await groups.all(),['failure','success']):
   selected=g.locator('[data-highlighted="true"]');assert 0<await selected.count()<8
   assert all(s==focus for s in await selected.evaluate_all('els=>els.map(e=>e.dataset.outcome)'))
  await page.goto(BASE+'/index.html');await page.add_script_tag(path=str(AXE));await page.set_viewport_size({'width':390,'height':1000})
  for key,vs in manifest.items():
   await page.evaluate('(h)=>location.hash=h',f'chapter-{int(key[1:3])}-slide-{key.split('s')[1].lstrip('0')}')
   await page.locator(f'#app .slide-art > svg[data-diagram="{vs[0]["key"]}"]').wait_for()
   assert not await bounds(page.locator('#app .slide-art > svg')),key
   audits.append({'screen':key,'width':390,'violations':await audit(page)})
   if len(vs)>1:
    details=page.locator('#app .more-visuals');assert await details.get_attribute('open') is None
    await details.locator('summary').click()
    for v in vs[1:]:
     svg=details.locator('[data-diagram="'+v['key']+'"]');assert await svg.is_visible();assert not await bounds(svg)
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),key
    audits.append({'screen':key+'-expanded','width':390,'violations':await audit(page)})
  await page.evaluate('buildPrint()')
  for key,vs in manifest.items():assert await page.locator('#print [data-diagram="'+vs[0]['key']+'"]').count()==1,key
  assert await page.locator('#print .more-visuals').count()==0
  assert not errors,errors
  await browser.close()
 # Every view has its own searchable PDF page, after the cover.
 info=subprocess.check_output(['pdfinfo',str(ROOT/'visual-guide.pdf')],text=True)
 pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);assert pages==len(views)+1,(pages,len(views))
 for i,v in enumerate(views,2):
  text=normal(subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),str(ROOT/'visual-guide.pdf'),'-'],text=True))
  assert normal(v['title']) in text,(i,v['title'],text)
  assert all(normal(term) in text for term in v['terms']),(i,v['terms'])
 report=dict(revision='all-concepts-visual',teaching_slides=len(manifest),concept_slides=sum(s['kind']=='concept' for c in course for s in c['slides']),evidence_slides=10,visual_views=len(views),visual_companion_pages=pages,required_term_appearances=sum(map(len,required.values())),primary_and_expanded_placement='passed',confirmation_evidence='same records, different emphasis',checks=checks,axe_audits=audits,js_errors=errors,limits='Automated visual, PDF, and accessibility checks; no learner pilot or full accessibility certification.')
 (ROOT/'qa/visual-coverage.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'qa/concept-visuals-results.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['checks','axe_audits']},indent=2))

if __name__=='__main__':asyncio.run(main())
