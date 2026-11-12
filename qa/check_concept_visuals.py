"""Check concept-specific visuals, shared evidence, layout, and accessibility.

Run against a local preview; AXE_SCRIPT selects a local axe-core script.
"""
import asyncio, json, os, re, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')
AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))
SPEC={'c02s03':'confounding','c03s04':'confirmation-bias','c04s04':'sunk-cost','c05s03':'conformity-motives','c07s04':'group-polarization','c10s03':'helping-barriers'}
PDF_LABELS={
 'confounding':['Several changes, one outcome','Dashed paths: possible explanations'],
 'confirmation-bias':['Same illustrative repair records','Notices failures','Notices successes'],
 'sunk-cost':['Choose from today onward','Cannot recover it','Future options'],
 'conformity-motives':['Same words, different reasons','Both motives can operate together.'],
 'group-polarization':['After: consensus','After: polarization','Stronger initial leaning','Agreement and polarization can coexist.'],
 'helping-barriers':['Two possible barriers to helping','Pluralistic ignorance','Diffusion of responsibility'],
}

async def main():
 assert AXE.is_file(),'Set AXE_SCRIPT to a local axe-core script.'
 (ROOT/'out').mkdir(exist_ok=True)
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await browser.new_page(reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/index.html');await page.add_script_tag(path=str(AXE));rows=[]
  for width in [320,390,768,1440]:
   await page.set_viewport_size({'width':width,'height':1000})
   for key,name in SPEC.items():
    chapter=int(key[1:3]);slide=int(key[4:6]);await page.evaluate('(h)=>location.hash=h',f'chapter-{chapter}-slide-{slide}')
    svg=page.locator(f'#app [data-diagram="{name}"]');await svg.wait_for();await page.evaluate('document.fonts.ready')
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,key)
    overflow=await svg.evaluate('''svg=>{const v=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].filter(t=>{const r=t.getBBox(),m=svg.getScreenCTM().inverse().multiply(t.getScreenCTM());return [[r.x,r.y],[r.x+r.width,r.y],[r.x,r.y+r.height],[r.x+r.width,r.y+r.height]].some(([x,y])=>{const p=new DOMPoint(x,y).matrixTransform(m);return p.x<0||p.y<0||p.x>v.width||p.y>v.height})}).map(t=>t.textContent)}''')
    assert not overflow,(width,key,overflow)
    issues=[]
    if width in [390,1440]:
     issues=await page.evaluate('''async()=>{const r=await axe.run(document.querySelector('#app'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>v.id)}''')
     assert not issues,(width,key,issues)
     await svg.screenshot(path=str(ROOT/f'out/{name}-{width}.png'))
    if name=='confirmation-bias':
     records=await svg.locator('[data-evidence-record]').evaluate_all('els=>els.map(e=>e.dataset.evidenceRecord)');assert len(records)==2 and records[0]==records[1]
     for group,focus in zip(await svg.locator('[data-evidence-record]').all(),['failure','success']):
      selected=group.locator('[data-highlighted="true"]');assert 0<await selected.count()<len(records[0].split(','))
      assert all(s==focus for s in await selected.evaluate_all('els=>els.map(e=>e.dataset.outcome)'))
    rows.append(dict(slide=key,diagram=name,width=width,overflow=overflow,axe_violations=issues if width in [390,1440] else 'not rerun at this width'))
  await page.evaluate('buildPrint()')
  for name in SPEC.values():assert await page.locator(f'#print [data-diagram="{name}"]').count()==1,name
  assert not errors,errors
  await browser.close()
  for key,name in SPEC.items():
   chapter=int(key[1:3]);slide=int(key[4:6])
   for file,number in [(ROOT/'common-ground-slides.pdf',(chapter-1)*8+slide),(ROOT/f'chapters/chapter-{chapter:02d}.pdf',slide)]:
    text=re.sub(r'\s+',' ',subprocess.check_output(['pdftotext','-f',str(number),'-l',str(number),str(file),'-'],text=True))
    for phrase in PDF_LABELS[name]:assert phrase in text,(str(file),number,phrase)
  (ROOT/'qa/concept-visuals-results.json').write_text(json.dumps(dict(revision='concept-visuals',concepts=['confounding','confirmation bias','sunk cost effect','informational and normative influence','group polarization','pluralistic ignorance','diffusion of responsibility'],target_slides=SPEC,checks=rows,js_errors=errors,unique_print_placement='passed',confirmation_evidence='same records, different emphasis',complete_and_chapter_pdf_diagrams=12,limits='Automated layout and accessibility checks; no learner pilot.'),indent=2)+'\n')
  print('Six concept diagrams checked at four widths; 12 accessibility audits and 12 PDF-page checks passed.')
if __name__=='__main__':asyncio.run(main())
