import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
CLIP_COUNT=len(json.loads((R/'audio/manifest.json').read_text())['clips'])
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  pg=await b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  await pg.goto((os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')+'/index.html#chapter-1-slide-1'));await pg.wait_for_selector('#read')
  assert await pg.evaluate('Object.keys(RECORDED_AUDIO).length')==CLIP_COUNT
  assert not await pg.evaluate("document.documentElement.innerHTML.includes('speechSynthesis')")
  await pg.locator('#read').click();await pg.wait_for_function('audioPlayer&&audioPlayer.currentTime>0.15')
  await pg.locator('#pause').click();t=await pg.evaluate('audioPlayer.currentTime');await pg.wait_for_timeout(300)
  assert abs(await pg.evaluate('audioPlayer.currentTime')-t)<.1
  await pg.locator('#pause').click();await pg.wait_for_function('(t)=>audioPlayer.currentTime>t+.1',arg=t)
  await pg.select_option('#speed','1.15');assert await pg.evaluate('audioPlayer.playbackRate')==1.15
  await pg.locator('#stop').click();assert await pg.evaluate('audioPlayer===null')
  await pg.locator('#next').click();await pg.wait_for_selector('.choices')
  await pg.locator('[data-answer="0"]').click();await pg.locator('#checkChoice').click();await pg.locator('#read').click();await pg.wait_for_function('audioPlayer&&audioPlayer.currentTime>.05')
  await pg.evaluate("audioPlayer.dispatchEvent(new Event('ended'))")
  assert await pg.evaluate("audioPlayer.src===new URL(RECORDED_AUDIO['c01s02-feedback-0'],location.href).href")
  await pg.evaluate('window.oldAudio=audioPlayer');await pg.locator('#next').click()
  await pg.wait_for_function('oldAudio.paused&&audioPlayer===null')
  await pg.evaluate("location.hash='chapter-1-slide-7'");await pg.wait_for_selector('#reveal');await pg.locator('#reveal').click();await pg.locator('#read').click()
  await pg.evaluate("audioPlayer.dispatchEvent(new Event('ended'))")
  assert await pg.evaluate("audioPlayer.src===new URL(RECORDED_AUDIO['c01s07-answers'],location.href).href")
  await pg.locator('#stop').click()
  # Decode metadata from every embedded recording using the real browser AAC decoder.
  decoded=await pg.evaluate('''async()=>{let results=[];for(const [id,url] of Object.entries(RECORDED_AUDIO)){let a=new Audio();a.src=url;await new Promise((resolve,reject)=>{a.onloadedmetadata=resolve;a.onerror=()=>reject(Error(id));a.load()});if(!(a.duration>0))throw Error(id);results.push({id,duration:a.duration});a.removeAttribute('src');a.load();}return results;}''')
  assert len(decoded)==CLIP_COUNT
  expected={x["id"]:x["duration"]for x in json.loads((R/"audio/manifest.json").read_text())["clips"]}
  for item in decoded:assert abs(item["duration"]-expected[item["id"]])<.04,item["id"]
  C=json.loads((R/'course.json').read_text())
  for c in C:
   for j,s in enumerate(c['slides']):
    if 'quiz' not in s:continue
    await pg.evaluate('(h)=>location.hash=h',f"chapter-{c['number']}-slide-{s['id'].split('s')[1].lstrip('0')}")
    await pg.wait_for_function('(t)=>document.querySelector("#slideTitle")?.textContent===t',arg=s['title'])
    for k,f in enumerate(s['quiz']['feedback']):
     await pg.locator(f'[data-answer="{k}"]').click();await pg.locator('#checkChoice').click();assert f in await pg.locator('.feedback').inner_text()
  await pg.set_viewport_size({'width':390,'height':844})
  await pg.evaluate("location.hash='chapter-1-slide-1'");await pg.wait_for_selector('.story')
  assert await pg.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await pg.screenshot(path=str(R/'qa/af-heart-mobile.png'),full_page=True)
  # Separate chapter has all 15 recordings and plays them without external assets.
  await pg.goto((os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/')+'/chapters/chapter-10.html'));await pg.wait_for_selector('#read')
  assert await pg.evaluate('Object.keys(RECORDED_AUDIO).length')==sum(x['id'].startswith('c10') for x in json.loads((R/'audio/manifest.json').read_text())['clips'])
  await pg.locator('#read').click();await pg.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1')
  await pg.locator('#stop').click()
  assert not errors,errors
  out=dict(recordings=CLIP_COUNT,audio_storage='local files or embedded, depending on the selected build',metadata_decoded=len(decoded),real_playback='passed',pause_resume_stop='passed',speed='passed',selected_feedback_queue='passed',recall_answer_queue='passed',navigation_stops_audio='passed',standalone_chapter='passed',feedback_variants=60,mobile_width=390,js_errors=errors,audible_human_review=False)
  (R/'qa/af-heart-browser-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));await b.close()
asyncio.run(main())
