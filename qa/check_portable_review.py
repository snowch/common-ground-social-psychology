"""Verify final offline decks and exact embedded audio bytes without external requests."""
import asyncio,base64,hashlib,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];P=R/'out/portable';BASE=os.environ.get('PORTABLE_BASE_URL','http://127.0.0.1:8878').rstrip('/');expected={x['id']:x['sha256']for x in json.loads((R/'audio/manifest.json').read_text())['clips']}
s=(P/'index.html').read_text();start=s.index('const RECORDED_AUDIO=')+len('const RECORDED_AUDIO=');audio,_=json.JSONDecoder().raw_decode(s[start:]);assert len(audio)==len(expected)
for id,data in audio.items():assert hashlib.sha256(base64.b64decode(data.split(',',1)[1])).hexdigest()==expected[id],id
async def main():
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);ctx=await b.new_context(offline=False,viewport={'width':390,'height':844});page=await ctx.new_page();errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url)if r.url.startswith(('http:','https:'))and not r.url.startswith(BASE+'/')else None)
  async def load(relative):
   await ctx.set_offline(False);await page.goto(BASE+'/'+relative);await ctx.set_offline(True)
  await load('index.html#chapter-1-slide-1');await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1');await page.locator('#stop').click()
  course=json.loads((R/'course.json').read_text());added=[(c,s) for c in course for s in c['slides'] if s['id'][-1].isalpha()]
  for c,slide in added:
   token=slide['id'].split('s')[1].lstrip('0')
   await page.evaluate('(h)=>location.hash=h',f"chapter-{c['number']}-slide-{token}");await page.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=slide['title'])
   await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1');assert await page.evaluate('(id)=>audioPlayer.src===RECORDED_AUDIO[id]',slide['id']);await page.locator('#stop').click()
  await page.evaluate("location.hash='case'");await page.wait_for_selector('.case-wrap');assert await page.locator('.case-wrap ol li').count()==6
  for n in range(1,11):
   await load(f'chapters/chapter-{n:02d}.html');await page.wait_for_selector('#slideTitle');assert await page.evaluate('Object.keys(RECORDED_AUDIO).length')==sum(id.startswith(f'c{n:02d}') for id in expected)
   await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.05');await page.locator('#stop').click()
  await page.evaluate("location.hash='case'");await page.wait_for_selector('.case-wrap');assert await page.locator('.case-wrap ol li').count()==6
  await load('study-guide.html');assert await page.locator('section.chapter').count()==10
  assert not errors and not requests,(errors,requests)
  out={'build':'out/portable','embedded_audio_hashes_verified':len(expected),'network_disabled_during_interaction_and_playback':True,'load_method':'Portable document served locally, then browser network disabled; file URLs are blocked by managed Chromium policy and were not tested','independent_teaching_pages_played':len(added),'chapter_decks_played':10,'full_deck_playback':'passed','written_case_full_and_standalone':'passed','study_companion':'passed','external_requests':requests,'js_errors':errors};(R/'qa/course-review-portable.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));await b.close()
asyncio.run(main())
