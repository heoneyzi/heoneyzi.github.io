/* heoneyzi.github.io — progressive enhancement only; every page reads fine without it.
   1) dark/light theme toggle   2) EN/KR toggle (elements with data-ko)   3) section highlight in the nav
   4) 3D tilt + pointer light on link cards ([data-tilt])   5) top bar shadow once the page scrolls */
(function () {
  'use strict';
  var root = document.documentElement;

  function store(key, value) {
    try { if (value === undefined) { return localStorage.getItem(key); } localStorage.setItem(key, value); } catch (e) { return null; }
    return null;
  }

  /* ---------- theme */
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) { meta.setAttribute('content', t === 'light' ? '#f4f8f8' : '#0b1011'); }
    document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-label', t === 'light' ? b.getAttribute('data-l-dark') : b.getAttribute('data-l-light'));
    });
  }
  setTheme(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      setTheme(t); store('hz-theme', t);
    });
  });

  /* ---------- language */
  var swapAttrs = [['data-ko-aria', 'aria-label'], ['data-ko-title', 'title'], ['data-ko-alt', 'alt']];
  function setLang(lang) {
    var ko = lang === 'ko';
    document.querySelectorAll('[data-ko]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) { el.setAttribute('data-en', el.innerHTML); }
      el.innerHTML = ko ? el.getAttribute('data-ko') : el.getAttribute('data-en');
    });
    swapAttrs.forEach(function (pair) {
      document.querySelectorAll('[' + pair[0] + ']').forEach(function (el) {
        var enKey = 'data-en-' + pair[1];
        if (!el.hasAttribute(enKey)) { el.setAttribute(enKey, el.getAttribute(pair[1]) || ''); }
        el.setAttribute(pair[1], ko ? el.getAttribute(pair[0]) : el.getAttribute(enKey));
      });
    });
    root.setAttribute('lang', ko ? 'ko' : 'en');
    var t = document.querySelector('meta[name="title-ko"]');
    if (t) {
      if (!root.hasAttribute('data-title-en')) { root.setAttribute('data-title-en', document.title); }
      document.title = ko ? t.getAttribute('content') : root.getAttribute('data-title-en');
    }
    document.querySelectorAll('[data-lang-toggle]').forEach(function (b) {
      b.setAttribute('aria-label', ko ? 'View in English' : '한국어로 보기');
      b.setAttribute('aria-pressed', ko ? 'true' : 'false');
    });
  }
  var params = new URLSearchParams(window.location.search);
  var initial = params.get('lang') || store('hz-lang') || 'en';
  if (initial === 'ko') { setLang('ko'); }
  document.querySelectorAll('[data-lang-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var next = root.getAttribute('lang') === 'ko' ? 'en' : 'ko';
      setLang(next); store('hz-lang', next);
    });
  });

  /* ---------- section highlight (index page only) */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"], .nav-strip a[href^="#"]'));
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { var id = a.getAttribute('href').slice(1); (byId[id] = byId[id] || []).push(a); });
    var current = null;
    function activate(id) {
      if (id === current) { return; }
      current = id;
      links.forEach(function (a) { a.classList.remove('is-active'); a.removeAttribute('aria-current'); });
      (byId[id] || []).forEach(function (a) {
        a.classList.add('is-active'); a.setAttribute('aria-current', 'true');
        var strip = a.closest('.nav-strip');
        if (strip) { strip.scrollTo({ left: a.offsetLeft - 16, behavior: 'smooth' }); }
      });
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { activate(e.target.id); } });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) { io.observe(s); } });
    var cover = document.getElementById('top');
    if (cover) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { current = null; links.forEach(function (a) { a.classList.remove('is-active'); a.removeAttribute('aria-current'); }); } });
      }, { rootMargin: '0px 0px -60% 0px' }).observe(cover);
    }
  }

  /* ---------- 3D tilt: only for a mouse/trackpad, never when the visitor asks for less motion */
  var mq = function (q) { return window.matchMedia ? window.matchMedia(q).matches : false; };
  if (mq('(hover: hover) and (pointer: fine)') && !mq('(prefers-reduced-motion: reduce)')) {
    var active = null, box = null, frame = 0;
    var release = function (card) {
      cancelAnimationFrame(frame);
      card.classList.remove('is-tilting');
      card.style.setProperty('--px', '0'); card.style.setProperty('--py', '0');
      if (active === card) { active = null; box = null; }
    };
    document.querySelectorAll('[data-tilt]').forEach(function (card) {
      card.addEventListener('pointerenter', function (ev) {
        if (ev.pointerType && ev.pointerType !== 'mouse' && ev.pointerType !== 'pen') { return; }
        active = card; box = card.getBoundingClientRect();
        card.classList.add('is-tilting');
      });
      card.addEventListener('pointermove', function (ev) {
        if (active !== card || !box) { return; }
        var x = Math.min(Math.max((ev.clientX - box.left) / box.width, 0), 1);
        var y = Math.min(Math.max((ev.clientY - box.top) / box.height, 0), 1);
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(function () {
          card.style.setProperty('--px', (x - 0.5).toFixed(3));
          card.style.setProperty('--py', (y - 0.5).toFixed(3));
          card.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
          card.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
        });
      });
      card.addEventListener('pointerleave', function () { release(card); });
    });
    window.addEventListener('scroll', function () { if (active) { box = active.getBoundingClientRect(); } }, { passive: true });
  }

  /* ---------- top bar: a soft shadow once content slides under it */
  var bar = document.querySelector('.topbar');
  if (bar) {
    var onScroll = function () { bar.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
