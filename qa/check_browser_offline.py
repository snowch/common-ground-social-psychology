"""Exercise the hosted browser save on a real service worker, then disconnect."""
import asyncio, json, os, tempfile
from pathlib import Path
from playwright.async_api import async_playwright
R = Path(__file__).resolve().parents[1]
RESULTS=Path(os.environ.get('COURSE_QA_RESULTS_DIR',R/'qa'));RESULTS.mkdir(parents=True,exist_ok=True)
BASE = os.environ.get('COURSE_BASE_URL', 'http://127.0.0.1:8891').rstrip('/')
AXE = Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))

async def rpc(page, action):
    return await page.evaluate('''async type=>{
      const registration=await navigator.serviceWorker.getRegistration();
      return new Promise((resolve,reject)=>{
       const timer=setTimeout(()=>reject(Error('Offline worker did not respond')),10000);
       const c=new MessageChannel();c.port1.onmessage=e=>{clearTimeout(timer);resolve(e.data);};
       registration.active.postMessage({type},[c.port2]);
      });
    }''', action)

async def main():
    errors=[]
    async with async_playwright() as p:
        profile=tempfile.TemporaryDirectory()
        ctx=await p.chromium.launch_persistent_context(profile.name,executable_path='/usr/bin/chromium',args=['--no-sandbox'],viewport={'width':390,'height':844},reduced_motion='reduce')
        page=await ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(BASE+'/offline.html')
        await page.locator('#offlineSave:not([disabled])').wait_for()
        await page.wait_for_function('navigator.serviceWorker.controller!==null')
        initial=await rpc(page,'STATUS');assert not initial['ready']
        for width in [320,390,768,1440]:
            await page.set_viewport_size({'width':width,'height':900})
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        await page.set_viewport_size({'width':390,'height':844})
        if AXE.exists():
            await page.add_script_tag(path=str(AXE))
            audit=await page.evaluate('''async()=>{const r=await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>v.id)}''')
            assert not audit,audit
        await page.screenshot(path=str(RESULTS/'browser-offline-mobile.png'),full_page=True)
        await page.locator('#offlineSave').click()
        await page.wait_for_function('document.querySelector("#offlineProgress").value>0')
        await page.locator('#offlinePause').click()
        await page.wait_for_function('document.querySelector("#offlinePause").hidden')
        paused=await rpc(page,'STATUS');assert not paused['busy'] and not paused['ready']
        assert paused['progress']['done']>0
        await page.reload();await page.locator('#offlineSave:not([disabled])').wait_for()
        assert 'Resume' in await page.locator('#offlineSave').inner_text()
        await page.locator('#offlineSave').click()
        await page.locator('#offlineContinue').wait_for(timeout=180000)
        status=await rpc(page,'STATUS');assert status['ready'] and status['savedVersion']==status['version'],status
        await page.wait_for_function('document.querySelector("#offlinePause").hidden')
        # Every manifest entry must be available; none can depend on HTTP cache.
        manifest=await page.evaluate('fetch("offline-manifest.json",{cache:"no-store"}).then(r=>r.json())')
        await ctx.set_offline(True)
        await page.goto(BASE+'/?offline-test=1#chapter-1-slide-1')
        await page.locator('#slideTitle').wait_for()
        assert await page.locator('.top-actions a').inner_text()=='Offline'
        course=await page.evaluate('COURSE')
        recordings=await page.evaluate('RECORDED_AUDIO')
        assert len(course)==10 and len(recordings)==168
        for c in course:
            await page.goto(BASE+'/#chapter-'+str(c['number'])+'-slide-1')
            await page.locator('#read').click()
            await page.wait_for_function('audioPlayer && audioPlayer.currentTime>0',timeout=15000)
            await page.locator('#stop').click()
            # Written responses and feedback are available and save offline.
            await page.goto(BASE+'/#chapter-'+str(c['number'])+'-slide-6')
            await page.locator('#decisionReasoning').fill('Offline reasoning: compare the evidence and plausible alternatives.')
            await page.locator('.option').first.click();await page.locator('#checkChoice').click()
            await page.locator('.feedback').wait_for()
        # Range support for seeking/resuming recordings, including suffix/invalid ranges.
        sample=next(iter(recordings.values()))
        ranges=await page.evaluate('''async url=>{
          const results=[];
          for(const range of ['bytes=0-31','bytes=32-','bytes=-16','bytes=999999999-']){
            const r=await fetch(url,{headers:{Range:range}});
            results.push({status:r.status,size:(await r.arrayBuffer()).byteLength,range:r.headers.get('Content-Range')});
          }return results;
        }''',sample)
        assert [r['status'] for r in ranges]==[206,206,206,416],ranges
        assert ranges[0]['size']==32 and ranges[2]['size']==16,ranges
        # Complete companion documents, PDFs, definitions and cached files.
        await page.goto(BASE+'/study-guide.html');assert await page.locator('.research-topic').count()==48
        await page.goto(BASE+'/visual-guide.html');assert await page.locator('svg').count()>=48
        await page.goto(BASE+'/chapters/chapter-01.html#chapter-1-slide-3')
        await page.locator('.lesson-research summary').click();assert await page.locator('.research-content').is_visible()
        cached=await page.evaluate('''async assets=>{
          const failures=[];
          for(const a of assets){const r=await fetch(new URL('../'+a.url,location.href));if(!r.ok||(await r.arrayBuffer()).byteLength!==a.bytes)failures.push(a.url);}
          return failures;
        }''',manifest['assets'])
        assert not cached,cached
        # A fresh tab and a document navigation must work with networking disabled.
        await ctx.close()
        ctx=await p.chromium.launch_persistent_context(profile.name,executable_path='/usr/bin/chromium',args=['--no-sandbox'],viewport={'width':390,'height':844})
        await ctx.set_offline(True)
        fresh=ctx.pages[0];await fresh.goto(BASE+'/offline.html')
        await fresh.locator('#offlineContinue').wait_for()
        assert 'Ready to use offline' in await fresh.locator('#offlineState').inner_text()
        # Removal leaves responses, and does not touch other applications' caches.
        await fresh.evaluate('caches.open("unrelated-app-test").then(c=>c.put("/unrelated",new Response("keep")))')
        await fresh.locator('#offlineRemove').click()
        await fresh.wait_for_function('document.querySelector("#offlineRemove").hidden')
        saved=await fresh.evaluate('JSON.parse(localStorage.getItem("common-ground-v1"))')
        assert len(saved['reasoning'])==10
        assert await fresh.evaluate('caches.has("unrelated-app-test")')
        assert not (await rpc(fresh,'STATUS'))['ready']
        assert not errors,errors
        result={'release':status['version'],'files':len(manifest['assets']),'bytes':manifest['bytes'],
         'pause_resume_reload':'passed','offline_chapters_narration_written_exercises':10,
         'all_saved_files_retrievable_offline':'passed','audio_ranges':ranges,
         'browser_restart_offline':'passed','companions_research_pdfs':'passed',
         'remove_retains_progress_and_unrelated_cache':'passed','widths':[320,390,768,1440],
         'axe':'passed' if AXE.exists() else 'not available','js_errors':errors}
        (RESULTS/'browser-offline-results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2));await ctx.close();profile.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
