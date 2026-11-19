'use strict';
(() => {
 const $ = id => document.getElementById(id);
 let worker, current, lastError = '';
 const mb = bytes => Math.ceil(bytes/1000000)+' MB';
 function render(s) {
  current=s;
  $('offlineSize').textContent=mb(s.bytes);
  const upToDate = s.ready && s.savedVersion===s.version;
  $('offlineState').textContent=s.busy?'Saving your course…':s.ready?(upToDate?'Ready to use offline':'Your saved course is ready. An update is available.'):'Save the course before you go';
  $('offlineDetail').textContent=s.busy?'Keep this tab open until saving finishes. You can continue learning in another tab.':s.ready?'Your browser has a saved copy of all ten chapters, recordings and companions.':'Select Make available offline to save all ten chapters and their recordings in this browser.';
  $('offlineSave').hidden=upToDate&&!s.busy;
  $('offlineSave').disabled=s.busy;
  $('offlineSave').textContent=s.ready?'Update saved course':s.progress?'Resume saving':'Make available offline';
  $('offlinePause').hidden=!s.busy;
  $('offlineRemove').hidden=!s.ready&&!s.progress;
  $('offlineRemove').disabled=s.busy;
  $('offlineContinue').hidden=!s.ready;
  $('offlineContinue').classList.toggle('primary',upToDate&&!s.busy);
  $('offlineProgressWrap').hidden=!s.progress;
  $('offlineProgress').max=s.bytes;
  $('offlineProgress').value=s.progress?.bytes||0;
  $('offlineProgressText').textContent=s.progress?`${mb(s.progress.bytes)} of ${mb(s.bytes)} · ${s.progress.done} of ${s.count} files`:'';
  if(s.error) lastError=s.error;
  $('offlineError').textContent=lastError;
  $('offlineConnection').textContent=navigator.onLine?'':'You are offline. '+(s.ready?'Your saved course is available.':'Reconnect to finish saving the course.');
 }
 function request(type) {
  return new Promise((resolve,reject)=>{
   const channel=new MessageChannel();
   const timer=setTimeout(()=>{channel.port1.close();reject(Error('The offline option did not respond. Reload this page and try again.'));},30000);
   channel.port1.onmessage=e=>{clearTimeout(timer);channel.port1.close();e.data.error?reject(Error(e.data.error)):resolve(e.data);};
   worker.postMessage({type},[channel.port2]);
  });
 }
 async function action(type) {
  lastError='';
  try {
   if(type==='SAVE') {
    // Ask the browser to protect the saved course from automatic cleanup.
    // A refusal does not prevent saving; the copy can always be saved again.
    if(navigator.storage?.persist) navigator.storage.persist().catch(()=>{});
    $('offlineSave').disabled=true;
   }
   if(type==='REMOVE') {
    $('offlineRemove').disabled=true;
    $('offlineRemove').textContent='Removing…';
   }
   render(await request(type));
  } catch(e) {lastError=e.message;if(current)render(current);else $('offlineError').textContent=lastError;}
  finally {$('offlineRemove').textContent='Remove saved course';}
 }
 async function init() {
  if(!('serviceWorker' in navigator) || !('caches' in window) || !window.isSecureContext) {
   $('offlineState').textContent='Offline saving is unavailable in this browser';
   $('offlineDetail').textContent='Try a modern browser, or use the chapter downloads below.';
   $('offlineSave').hidden=true;return;
  }
  try {
   const registration=await navigator.serviceWorker.register('./sw.js',{scope:'./',updateViaCache:'none'});
   await navigator.serviceWorker.ready;
   await registration.update().catch(()=>{});
   const incoming=registration.installing||registration.waiting;
   if(incoming && incoming.state!=='activated' && incoming.state!=='redundant') {
    await new Promise(resolve=>incoming.addEventListener('statechange',()=>{
     if(['activated','redundant'].includes(incoming.state))resolve();
    }));
   }
   worker=registration.active;
   navigator.serviceWorker.addEventListener('message',e=>{
    if(e.data?.type==='OFFLINE_STATUS' && e.source?.scriptURL===new URL('./sw.js',location.href).href)render(e.data);
   });
   navigator.serviceWorker.addEventListener('controllerchange',async()=>{
    worker=navigator.serviceWorker.controller||registration.active;
    try{render(await request('STATUS'));}catch(e){$('offlineError').textContent=e.message;}
   });
   $('offlineSave').onclick=()=>action('SAVE');
   $('offlinePause').onclick=()=>action('PAUSE');
   $('offlineRemove').onclick=()=>action('REMOVE');
   window.addEventListener('online',()=>current&&render(current));
   window.addEventListener('offline',()=>current&&render(current));
   render(await request('STATUS'));
  } catch(e) {
   $('offlineState').textContent='Offline saving could not start';
   $('offlineDetail').textContent='Reload this page while connected, or use the chapter downloads below.';
   $('offlineError').textContent=e.message;$('offlineSave').hidden=true;
  }
 }
 init();
})();
