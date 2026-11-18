/* The hosted builder supplies a content-addressed list for this release. */
const RELEASE = __OFFLINE_RELEASE__;
const ASSETS = __OFFLINE_ASSETS__;
const ROOT = self.registration.scope;
const PREFIX = 'common-ground-offline:' + new URL(ROOT).pathname + ':';
const META = PREFIX + 'state';
const SNAPSHOT = PREFIX + RELEASE;
const STATE_URL = new URL('__offline_state__', ROOT).href;
let job = null, controller = null, progress = null, pendingWriters = [];
const urlFor = path => new URL(path, ROOT).href;
async function readState() {
 const r = await (await caches.open(META)).match(STATE_URL);
 return r ? r.json() : {};
}
async function writeState(value) {
 await (await caches.open(META)).put(STATE_URL, new Response(JSON.stringify(value)));
}
async function status() {
 const saved = await readState();
 // A readiness claim requires every saved entry to still exist.
 let ready = false;
 if (saved.active && await caches.has(saved.active)) {
  const keys = await (await caches.open(saved.active)).keys();
  ready = keys.length === saved.count;
 }
 if (!progress && await caches.has(SNAPSHOT)) {
  const keys = new Set((await (await caches.open(SNAPSHOT)).keys()).map(r=>r.url));
  const present = ASSETS.filter(a=>keys.has(urlFor(a.url)));
  if (present.length) progress={done:present.length,bytes:present.reduce((n,a)=>n+a.bytes,0)};
 }
 return {ready, savedVersion: ready ? saved.version : null, version: RELEASE,
  bytes: ASSETS.reduce((n,a) => n+a.bytes,0), count: ASSETS.length,
  busy: !!job, progress};
}
async function broadcast(extra = {}) {
 const message = {type:'OFFLINE_STATUS', ...await status(), ...extra};
 for (const client of await self.clients.matchAll({includeUncontrolled:true})) client.postMessage(message);
}
async function download() {
 controller = new AbortController();
 const cache = await caches.open(SNAPSHOT);
 let done = 0, bytes = 0;
 const update = async a => {
  done++; bytes += a.bytes; progress = {done, bytes}; await broadcast();
 };
 const remaining = [];
 for (const a of ASSETS) {
  if (await cache.match(urlFor(a.url))) await update(a);
  else remaining.push(a);
 }
 // Keep memory and network use bounded on phones.
 pendingWriters = Array.from({length:3}, async () => {
  while (remaining.length) {
   if (controller.signal.aborted) throw new DOMException('Cancelled','AbortError');
   const a = remaining.shift();
   const response = await fetch(urlFor(a.url), {cache:'no-store', signal:controller.signal});
   if (!response.ok || response.type === 'opaque') throw Error('A course file could not be saved.');
   const body = await response.arrayBuffer();
   const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',body)), b=>b.toString(16).padStart(2,'0')).join('');
   if (digest !== a.sha256) throw Error('The course changed during saving. Reconnect and try again.');
   if (controller.signal.aborted) throw new DOMException('Cancelled','AbortError');
   const headers = new Headers(response.headers);
   headers.delete('Content-Encoding');headers.set('Content-Length',String(body.byteLength));
   await cache.put(urlFor(a.url),new Response(body,{status:200,headers}));
   await update(a);
  }
 });
 await Promise.all(pendingWriters);
 const saved = await readState();
 // Only switch to the new snapshot after ALL content has been verified.
 // Keep the previous release for audio in tabs that were already open.
 await writeState({active:SNAPSHOT,previous:saved.active===SNAPSHOT?saved.previous:saved.active,
  version:RELEASE,count:ASSETS.length});
 const keep = await readState();
 for (const name of await caches.keys()) {
  if (name.startsWith(PREFIX) && ![META,keep.active,keep.previous].includes(name)) await caches.delete(name);
 }
}
self.addEventListener('install',event=>event.waitUntil(self.skipWaiting()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('message',event=>{
 const port = event.ports[0];
 const reply = value => port?.postMessage(value);
 event.waitUntil((async()=>{
  try {
   if (event.data?.type==='STATUS') {reply(await status());return;}
   if (event.data?.type==='SAVE') {
    if (!job) {
     progress = {done:0,bytes:0};
     job = download().catch(async e=>{
      controller.abort();
      // Await all in-flight writers before another SAVE or REMOVE can start.
      await Promise.allSettled(pendingWriters);
      await broadcast({error:e.name==='AbortError'?'Saving paused. Reconnect and resume when you are ready.':
       e.name==='QuotaExceededError'?'There is not enough browser storage. Free some space, then resume saving.':e.message});
     }).finally(async()=>{job=null;controller=null;await broadcast();});
    }
    reply(await status());await job;return;
   }
   if (event.data?.type==='PAUSE') {controller?.abort();await job;reply(await status());return;}
   if (event.data?.type==='REMOVE') {
    controller?.abort();await job;
    for (const name of await caches.keys()) if (name.startsWith(PREFIX)) await caches.delete(name);
    progress=null;reply(await status());await broadcast();return;
   }
   reply({error:'Unknown offline action.'});
  } catch(e) {reply({error:e.message});}
 })());
});
// A small range responder makes cached AAC recordings seekable offline.
async function ranged(response, range) {
 const match = /^bytes=(\d*)-(\d*)$/.exec(range);
 const body = await response.arrayBuffer(), size = body.byteLength;
 let start, end;
 if (match && (match[1] || match[2])) {
  start = match[1] ? Number(match[1]) : Math.max(0,size-Number(match[2]));
  end = match[1] && match[2] ? Math.min(size-1,Number(match[2])) : size-1;
 }
 if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start>end || start>=size) {
  return new Response(null,{status:416,headers:{'Content-Range':`bytes */${size}`}});
 }
 const headers = new Headers(response.headers);
 headers.set('Content-Range',`bytes ${start}-${end}/${size}`);
 headers.set('Content-Length',String(end-start+1));headers.set('Accept-Ranges','bytes');
 return new Response(body.slice(start,end+1),{status:206,headers});
}
self.addEventListener('fetch',event=>{
 if (event.request.method!=='GET') return;
 const url = new URL(event.request.url);
 if (url.origin!==new URL(ROOT).origin || !url.href.startsWith(ROOT)) return;
 if (url.pathname.endsWith('/sw.js')) return;
 event.respondWith((async()=>{
  const saved = await readState();
  if (url.pathname===new URL(ROOT).pathname) url.pathname+='index.html';
  const audio = url.pathname.includes('/audio/clips/');
  for (const name of [saved.active,saved.previous].filter(Boolean)) {
   if (!await caches.has(name)) continue;
   const hit = await (await caches.open(name)).match(url.href,{ignoreSearch:!audio});
   if (hit) {
    if (event.request.headers.has('Range')) return ranged(hit,event.request.headers.get('Range'));
    if (audio) {
     const headers=new Headers(hit.headers);headers.set('Accept-Ranges','bytes');
     return new Response(hit.body,{status:hit.status,headers});
    }
    return hit;
   }
  }
  return fetch(event.request);
 })());
});
