"""Fault-inject real service-worker saves and updates in an isolated nested scope."""
import asyncio, hashlib, json, tempfile, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.async_api import async_playwright
from check_browser_offline import rpc
R=Path(__file__).resolve().parents[1]

async def main():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);scope=root/'nested/course';scope.mkdir(parents=True)
  broken=set()
  class Handler(SimpleHTTPRequestHandler):
   def __init__(self,*args,**kwargs):super().__init__(*args,directory=tmp,**kwargs)
   def log_message(self,*args):pass
   def do_GET(self):
    # SimpleHTTPServer's one-second Last-Modified precision would mask
    # this fixture's same-size worker rewrite; production uses content ETags.
    if self.path.split('?')[0].endswith('/sw.js'):
     if 'If-Modified-Since' in self.headers:del self.headers['If-Modified-Since']
    if self.path.split('?')[0] in broken:
     self.send_response(200);self.end_headers();self.wfile.write(b'corrupt release');return
    super().do_GET()
  server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
  threading.Thread(target=server.serve_forever,daemon=True).start()
  base=f'http://127.0.0.1:{server.server_port}/nested/course/'
  def release(n):
   items={'index.html':f'<!doctype html><html lang="en"><title>Fixture</title><h1>Release {n}</h1></html>'.encode(),
          'audio/clips/sample.m4a':f'audio release {n}'.encode(), 'notes.txt':f'notes {n}'.encode()}
   assets=[]
   for name,body in items.items():
    path=scope/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
    digest=hashlib.sha256(body).hexdigest()
    assets.append({'url':name+('?v='+digest[:12] if name.endswith('m4a') else ''),'bytes':len(body),'sha256':digest})
   worker=(R/'web/offline-worker.js').read_text().replace('__OFFLINE_RELEASE__',json.dumps(str(n))).replace('__OFFLINE_ASSETS__',json.dumps(assets))
   (scope/'sw.js').write_text(worker)
   return assets
  release(1)
  async with async_playwright() as p:
   browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   ctx=await browser.new_context();page=await ctx.new_page();await page.goto(base)
   await page.evaluate('navigator.serviceWorker.register("./sw.js").then(()=>navigator.serviceWorker.ready)')
   await page.wait_for_function('navigator.serviceWorker.controller!==null')
   broken.add('/nested/course/notes.txt')
   await rpc(page,'SAVE')
   async def finished():
    for _ in range(200):
     status=await rpc(page,'STATUS')
     if not status['busy']:return status
     await asyncio.sleep(.05)
    raise AssertionError('Save never settled')
   failed=await finished();assert not failed['ready'],failed
   broken.clear();await rpc(page,'SAVE');saved=await finished();assert saved['ready'],saved
   old_audio=(await page.evaluate('fetch("audio/clips/sample.m4a?v="+"'+hashlib.sha256(b'audio release 1').hexdigest()[:12]+'").then(r=>r.text())'))
   assert old_audio=='audio release 1'
   print('Verified corrupt-file recovery; checking release update.',flush=True)
   assets2=release(2)
   await page.evaluate('''async()=>{
     const r=await navigator.serviceWorker.getRegistration();await r.update();
     const next=r.installing||r.waiting;
     if(next && !['activated','redundant'].includes(next.state)){
      await new Promise(resolve=>next.addEventListener('statechange',()=>{
       if(['activated','redundant'].includes(next.state))resolve();
      }));
     }
   }''')
   for _ in range(200):
    if (await rpc(page,'STATUS'))['version']=='2':break
    await asyncio.sleep(.05)
   assert (await rpc(page,'STATUS'))['version']=='2'
   # A partial update must never replace the complete, working old snapshot.
   broken.add('/nested/course/notes.txt');await rpc(page,'SAVE');failed=await finished()
   assert failed['ready'] and failed['savedVersion']=='1' and failed['version']=='2',failed
   await ctx.set_offline(True);await page.reload();assert await page.locator('h1').inner_text()=='Release 1'
   await ctx.set_offline(False);broken.clear();await rpc(page,'SAVE');updated=await finished()
   assert updated['ready'] and updated['savedVersion']=='2',updated
   await ctx.set_offline(True);await page.reload();assert await page.locator('h1').inner_text()=='Release 2'
   for version in [1,2]:
    digest=hashlib.sha256(f'audio release {version}'.encode()).hexdigest()[:12]
    assert await page.evaluate('(u)=>fetch(u).then(r=>r.text())',f'audio/clips/sample.m4a?v={digest}')==f'audio release {version}'
   assert await page.evaluate('fetch("notes.txt").then(r=>r.text())')=='notes 2'
   await browser.close()
  server.shutdown()
  result={'nested_scope':'passed','corrupt_file_rejected':'passed','partial_save_resume':'passed',
    'failed_update_preserves_complete_old_release_offline':'passed','explicit_update_promotes_complete_release':'passed',
    'previous_recording_version_for_existing_tabs':'passed'}
  (R/'qa/offline-update-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__ == "__main__":
    asyncio.run(main())
