"""Check elapsed/remaining playback, speed, pause, and multi-recording queues."""
import asyncio,json,math,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
RESULTS=Path(os.environ.get('COURSE_QA_RESULTS_DIR',R/'qa'));RESULTS.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8891').rstrip('/')
async def main():
 errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':390,'height':844});page.on('pageerror',lambda e:errors.append(str(e)))
  # Use the complete saved course: its range responder supports real seeking
  # even when the local static test server has no HTTP Range support.
  await page.goto(BASE+'/offline.html')
  await page.locator('#offlineSave:not([disabled])').wait_for()
  await page.locator('#offlineSave').click()
  await page.locator('#offlineContinue').wait_for(timeout=180000)
  await page.goto(BASE+'/#chapter-1-slide-1')
  assert await page.locator('#playbackProgress').get_attribute('value')=='0'
  initial=await page.evaluate('AUDIO_DURATIONS.c01s01')
  assert abs(float(await page.locator('#playbackProgress').get_attribute('max'))-initial)<.01
  for width in [320,390,768,1024,1440]:
   await page.set_viewport_size({'width':width,'height':900})
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
  await page.set_viewport_size({'width':390,'height':844})
  await page.locator('#read').click();await page.wait_for_function('audioPlayer.currentTime>.3')
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.value')>0
  await page.locator('#pause').click()
  paused=await page.evaluate('audioPlayer.currentTime');await page.wait_for_timeout(400)
  assert abs(await page.evaluate('audioPlayer.currentTime')-paused)<.05
  await page.evaluate('audioPlayer.currentTime=10')
  await page.wait_for_function('document.querySelector("#playbackProgress").value>=10')
  await page.locator('#speed').select_option('1.15')
  expected=await page.evaluate('Math.ceil((audioPlayer.duration-audioPlayer.currentTime)/1.15)')
  clock=f'{expected//60}:{expected%60:02d}'
  assert clock+' left' in await page.locator('#playbackTime').inner_text()
  await page.screenshot(path=str(RESULTS/'playback-progress-mobile.png'),full_page=True)
  await page.locator('#stop').click()
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.value')==0
  await page.locator('#speed').select_option('1')
  await page.goto(BASE+'/#chapter-1-slide-2')
  await page.locator('.option').first.click();await page.locator('#checkChoice').click()
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.max')==await page.evaluate('AUDIO_DURATIONS.c01s02+AUDIO_DURATIONS["c01s02-feedback-0"]')
  await page.locator('#read').click();await page.wait_for_function('audioPlayer.duration>0')
  main_duration=await page.evaluate('audioPlayer.duration')
  await page.evaluate('audioPlayer.currentTime=audioPlayer.duration-.03')
  await page.wait_for_function('audioPlayer.src.includes("feedback-0")&&audioPlayer.currentTime>.1')
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.value')>=main_duration
  await page.locator('#playFeedback').click();await page.wait_for_function('audioPlayer.duration>0')
  assert abs(await page.locator('#playbackProgress').evaluate('(e)=>e.max')-await page.evaluate('audioPlayer.duration'))<.1
  await page.evaluate('audioPlayer.currentTime=audioPlayer.duration-.03')
  await page.wait_for_function('playbackInfo.finished')
  assert '0:00 left' in await page.locator('#playbackTime').inner_text()
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.value===e.max')
  await page.goto(BASE+'/#chapter-1-slide-7')
  await page.locator('#reveal').click()
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.max')==await page.evaluate('AUDIO_DURATIONS.c01s07+AUDIO_DURATIONS["c01s07-answers"]')
  await page.locator('#read').click();await page.wait_for_function('audioPlayer.duration>0')
  await page.evaluate('audioPlayer.currentTime=audioPlayer.duration-.03')
  await page.wait_for_function('audioPlayer.src.includes("answers")&&audioPlayer.currentTime>.1')
  await page.goto(BASE+'/chapters/chapter-10.html#chapter-10-slide-1')
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.value')==0
  assert await page.locator('#playbackProgress').evaluate('(e)=>e.max')==await page.evaluate('AUDIO_DURATIONS.c10s01')
  axe=Path('/tmp/common-ground-axe.min.js')
  if axe.exists():
   await page.add_script_tag(path=str(axe))
   violations=await page.evaluate('''async()=>{const r=await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>v.id)}''')
   assert not violations,violations
  assert not errors,errors
  await browser.close()
 result={'initial_duration_without_loading_audio':'passed','elapsed_and_remaining':'passed','pause_resume_seek_speed_stop':'passed',
  'narration_plus_feedback_queue':'passed','feedback_only_queue':'passed','recall_answers_queue':'passed',
  'completion_and_navigation_reset':'passed','standalone_chapter':'passed','widths':[320,390,768,1024,1440],'js_errors':errors}
 (RESULTS/'playback-progress-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':asyncio.run(main())
