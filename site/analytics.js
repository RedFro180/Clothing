// Shop analytics. Sends events to PostHog (free tier) when POSTHOG_KEY is set in config.js; otherwise does nothing.
// Data lands in the owner's PostHog dashboard only. No names, emails or phone numbers are sent here.
// Events:
//   product_viewed, added_to_list, search, search_no_results, suggestion_opened
//   preorder_sent      items, item_count, subtotal, shipping, clicks_to_purchase, seconds_to_purchase
//   bought_together    one event per pair of different hoodies in the same preorder ("A + B")
//   session_end        seconds_on_site, clicks, products_viewed, viewed_names, items_in_list, purchased (true/false)
(() => {
  "use strict";
  const C = window.SITE_CONFIG || {};
  const t0 = Date.now();
  const S = { clicks: 0, viewed: [], added: 0, purchased: false, ended: false };
  let ph = null;

  if (C.POSTHOG_KEY) {
    // Official PostHog loader (array.js), cookieless: nothing is stored on the visitor's device.
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify reset register opt_out_capturing opt_in_capturing".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    try {
      posthog.init(C.POSTHOG_KEY, { api_host: C.POSTHOG_HOST || "https://us.i.posthog.com", persistence: "memory",
        autocapture: false, capture_pageview: true, capture_pageleave: true, disable_session_recording: true });
      ph = window.posthog;
    } catch (e) { ph = null; }
  }

  const secs = () => Math.round((Date.now() - t0) / 1000);
  function track(name, props) {
    const p = Object.assign({}, props, { seconds_on_site: secs(), clicks_so_far: S.clicks });
    if (name === "product_viewed" && !S.viewed.includes(props.id)) S.viewed.push(props.id);
    if (name === "added_to_list") S.added++;
    try { if (ph) ph.capture(name, p); } catch (e) {}
    try { (window.__events = window.__events || []).push([name, p]); } catch (e) {}   // for testing in the browser
  }
  function trackPurchase(items, subtotal, shipping) {
    S.purchased = true;
    track("preorder_sent", { items, item_ids: items.map(i => i.id), item_count: items.reduce((s, i) => s + i.qty, 0),
      subtotal, shipping, clicks_to_purchase: S.clicks, seconds_to_purchase: secs() });
    const ids = [...new Set(items.map(i => i.id))].sort((a, b) => a - b);
    const name = id => (items.find(i => i.id === id) || {}).name || "#" + id;
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++)
      track("bought_together", { pair: `${name(ids[i])} + ${name(ids[j])}`, a: ids[i], b: ids[j] });
  }
  function end() {
    if (S.ended) return; S.ended = true;
    const cat = (window.CATALOG && window.CATALOG.products) || [];
    const names = S.viewed.map(id => (cat.find(p => p.id === id) || {}).name || "#" + id);
    const p = { seconds_on_site: secs(), clicks: S.clicks, products_viewed: S.viewed.length, viewed_names: names,
      items_in_list: S.added, purchased: S.purchased, last_product: names[names.length - 1] || null };
    try { if (ph) ph.capture("session_end", p, { transport: "sendBeacon" }); } catch (e) {}
    try { (window.__events = window.__events || []).push(["session_end", p]); } catch (e) {}
  }
  document.addEventListener("click", () => { S.clicks++; }, true);
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") end(); else S.ended = false; });
  window.addEventListener("pagehide", end);
  window.track = track; window.trackPurchase = trackPurchase; window.__session = S;
})();
