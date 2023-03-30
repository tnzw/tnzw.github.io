const cacheKey = 'page-2.5.0';

const contentToCache = [
  './page.html',
  './favicon.ico',
  './favicon-32.png',
  './favicon-64.png',
  './favicon-96.png',
  './favicon-128.png',
  './favicon-168.png',
  './favicon-192.png',
  './favicon-256.png',
  './favicon-512.png',
];

console = {log:()=>{}};  // disable logging

self.addEventListener('install', (e) => {
  // Installing Service Worker
  console.log('[Service Worker] Install');
  e.waitUntil((async () => {
    const cache = await caches.open(cacheKey);
    console.log('[Service Worker] Caching all: app shell and content');
    await cache.addAll(contentToCache);
  })());
});

self.addEventListener('fetch', (e) => {
  // Fetching content using Service Worker

  e.respondWith((async () => {
    const r = await caches.match(e.request);
    if (r) return r;
    return await fetch(e.request);
  })());

  // // Cache http and https only, skip unsupported chrome-extension:// and file://...
  // if (!/^https?:/i.test(e.request.url)) return;

  // e.respondWith((async () => {
  //   const r = await caches.match(e.request);
  //   console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
  //   if (r) return r;
  //   const response = await fetch(e.request);
  //   const cache = await caches.open(cacheKey);
  //   console.log(`[Service Worker] Caching new resource: ${e.request.url}`);
  //   cache.put(e.request, response.clone());
  //   return response;
  // })());

});

self.addEventListener('activate', (e) => {
  // Activating this version of the Service Worker

  // Using it to clear old Service Worker version cache.
  e.waitUntil(
    caches.keys().then((cacheKeyList) => {
      return Promise.all(
        cacheKeyList.map((key) => {
          if (key === cacheKey) return;
          console.log(`[Service Worker] Deleting old cache: ${key}`);
          return caches.delete(key);
        })
      );
    })
  );
});
