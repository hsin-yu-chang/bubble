const CACHE_NAME = "bubble-translation-v1";

const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./favicon.ico",
  "./vite.svg",
  "./cloudinary_urls.txt",

  "./assets/index-brVkwgov.js",
  "./assets/index-d5z48If.css",
  "./assets/translation_patch.js"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(FILES_TO_CACHE))
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request);
    })
  );
});