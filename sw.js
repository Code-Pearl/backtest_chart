const C='replay-v4',FC='replay-fonts',F=['./','./index.html','./manifest.json'];
const FONT=/(^|\.)(fonts\.googleapis\.com|fonts\.gstatic\.com)$/;
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C&&x!==FC).map(x=>caches.delete(x))))));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  // Google Fonts (Alata): cache on first online load, serve from cache after, refresh in background
  if(FONT.test(new URL(e.request.url).hostname)){
    e.respondWith(caches.open(FC).then(async c=>{
      const hit=await c.match(e.request);
      const net=fetch(e.request).then(r=>{c.put(e.request,r.clone());return r}).catch(()=>hit);
      return hit||net;
    }));
    return;
  }
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
});
