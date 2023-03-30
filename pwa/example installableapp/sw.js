//self.importScripts('some_data.js');

const cacheKey = 'installableapp-v2';

const contentToCache = [
  './',
  './index.html',
  './favicon.ico',
  './icons/icon-32.png',
  './icons/icon-64.png',
  './icons/icon-96.png',
  './icons/icon-128.png',
  './icons/icon-168.png',
  './icons/icon-192.png',
  './icons/icon-256.png',
  './icons/icon-512.png',
  './icons/og_image-512.png',
];

//console = {log:()=>{}};  // disable logging

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

  // Cache http and https only, skip unsupported chrome-extension:// and file://...
  if (!/^https?:/i.test(e.request.url)) return;

  e.respondWith((async () => {
    const r = await caches.match(e.request);
    console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
    if (r) return r;
    const response = await fetch(e.request);
    const cache = await caches.open(cacheKey);
    console.log(`[Service Worker] Caching new resource: ${e.request.url}`);
    cache.put(e.request, response.clone());
    return response;
  })());

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
