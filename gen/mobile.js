/* The phone page's behaviour (see mobile_view in panels.py): the menu, the sky
   switch, the way into and out of the world, the name, Ping's typing, the
   contact form and Copy email. Plain script, no build step. */
/* ---- the world: opening it is a step in the browser's history, so the back
   button or gesture (or Back to quick view) returns to the same spot */
var outpostScroll = 0;
function outpostWorld(open) {
  var root = document.documentElement;
  if (open) {
    outpostScroll = window.scrollY;
    var menu = document.getElementById('m-menu');
    if (menu && !menu.hidden) { menu.hidden = true; document.querySelector('#mobile .menu-shade').hidden = true; }
    if (!(history.state && history.state.world)) history.pushState({ world: true }, '', '#world');
    root.classList.add('explore');
    window.dispatchEvent(new Event('resize'));
    window.scrollTo(0, 0);
  } else {
    root.classList.remove('explore');
    if (location.hash === '#world') history.replaceState(null, '', location.pathname + location.search);
    window.dispatchEvent(new Event('resize'));
    window.scrollTo({ top: outpostScroll, behavior: 'instant' });
  }
}
window.addEventListener('popstate', function () {
  if (document.documentElement.classList.contains('explore') && !(history.state && history.state.world)) outpostWorld(false);
});
/* ---- the menu: open, close (X, outside, Escape, any link), and mark the section being read ---- */
(function () {
  var btn = document.querySelector('#mobile .menu-btn'), menu = document.getElementById('m-menu'),
      shade = document.querySelector('#mobile .menu-shade');
  function set(open) {
    menu.hidden = shade.hidden = !open;
    btn.setAttribute('aria-expanded', open);
    if (open) menu.focus(); else btn.focus({preventScroll: true});
  }
  btn.addEventListener('click', function () { set(true); });
  if ('IntersectionObserver' in window) {
    var links = {};
    menu.querySelectorAll('a[href^="#m-"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var here = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting || !links[e.target.id]) return;
        Object.keys(links).forEach(function (id) { links[id].removeAttribute('aria-current'); });
        links[e.target.id].setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('#mobile section').forEach(function (sec) { here.observe(sec); });
  }
  shade.addEventListener('click', function () { set(false); });
  menu.querySelector('.menu-close').addEventListener('click', function () { set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) set(false); });
  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (a.hasAttribute('data-open-art')) document.querySelector('#m-studio details').open = true;
      menu.hidden = shade.hidden = true; btn.setAttribute('aria-expanded', false);
    });
  });
})();
/* ---- the sky switch: night or sunrise, remembered on this device ---- */
(function () {
  var root = document.getElementById('mobile'), btn = root.querySelector('.sky-btn');
  function label() { btn.setAttribute('aria-label', root.classList.contains('night') ? 'Switch to sunrise sky' : 'Switch to night sky'); }
  function flip() {
    var night = root.classList.toggle('night');
    try { localStorage.setItem('outpost-sky', night ? 'night' : 'sunrise'); } catch (e) {}
    label();
  }
  label();
  btn.addEventListener('click', flip);
})();
/* ---- Copy email: for people whose mail opens in a browser tab ---- */
(function () {
  document.querySelectorAll('#mobile .copy').forEach(function (b) {
    var label = b.querySelector('span'), timer;
    function show(text, ms) { label.textContent = text; clearTimeout(timer); timer = setTimeout(function () { label.textContent = 'Copy email'; }, ms); }
    b.addEventListener('click', function () {
      var email = b.dataset.email;
      if (navigator.clipboard) navigator.clipboard.writeText(email).then(function () { show('Copied!', 2000); }, function () { show(email, 8000); });
      else show(email, 8000);
    });
  });
})();
/* ---- the name: a tap replays the letter wave ---- */
(function () {
  var name = document.querySelector('#mobile .name');
  name.addEventListener('click', function () {
    name.classList.remove('hop'); void name.offsetWidth; name.classList.add('hop');
  });
  name.addEventListener('animationend', function (e) {
    if (e.animationName === 'm-hop' && e.target === name.lastElementChild) name.classList.remove('hop');
  });
})();
/* ---- the contact form: check each field, then send through Web3Forms ---- */
(function () {
  var f = document.getElementById('m-letter'), el = f.elements;
  /* each field's rule; errors show once a field is left or the form is sent, then update as you type */
  var rules = {
    name: function (v) { return v.length >= 2; },
    from: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); },
    msg: function (v) { return v.length >= 10; }
  };
  function check(name) {
    var ok = rules[name](el[name].value.trim());
    document.getElementById('m-err-' + name).hidden = ok;
    el[name].setAttribute('aria-invalid', !ok);
    return ok;
  }
  Object.keys(rules).forEach(function (name) {
    el[name].addEventListener('blur', function () { if (el[name].value.trim()) { el[name].dataset.touched = 1; check(name); } });
    el[name].addEventListener('input', function () { if (el[name].dataset.touched) check(name); });
  });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = Object.keys(rules).filter(function (name) { el[name].dataset.touched = 1; return !check(name); });
    if (bad.length) { el[bad[0]].focus(); return; }
    send();
  });
  function send() {
    var btn = f.querySelector('.send'), ok = document.getElementById('m-sent'), fail = document.getElementById('m-fail');
    var name = el['name'].value.trim();
    ok.hidden = fail.hidden = true;
    btn.disabled = true; btn.textContent = 'SENDING...';
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ access_key: f.dataset.key, subject: 'Portfolio message from ' + name,
        from_name: name, name: name, email: el['from'].value.trim(), message: el['msg'].value.trim() })
    })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.success) throw new Error(j.message);
        f.reset();
        Object.keys(rules).forEach(function (n) { delete el[n].dataset.touched; el[n].removeAttribute('aria-invalid'); });
        ok.hidden = false;
      })
      .catch(function () { fail.hidden = false; })
      .then(function () { btn.disabled = false; btn.textContent = 'SEND IT DOWN'; });
  }
})();
/* ---- Ping's lines: each bubble types itself out as it scrolls into view, and a
   tap shows the whole line. The full text stays in the page (transparent) for
   its size and for screen readers; the typed copy on top is hidden from them. */
(function () {
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bubbles = [].slice.call(document.querySelectorAll('#mobile .speech'));
  bubbles.forEach(function (b) {
    var who = b.querySelector('.who');
    var text = b.textContent.slice(who.textContent.length);
    b.textContent = '';
    b.appendChild(who);
    var line = document.createElement('span'); line.className = 'line';
    var full = document.createElement('span'); full.className = 'full'; full.textContent = text;
    var type = document.createElement('span'); type.className = 'type'; type.setAttribute('aria-hidden', 'true');
    line.appendChild(full); line.appendChild(type); b.appendChild(line);
    b.typeLine = function () {
      if (b.typed) return; b.typed = true;
      if (still) { type.textContent = text; return; }
      var chars = Array.from(text), i = 0;
      type.classList.add('on');
      (function step() {
        if (b.done) return;
        type.textContent = chars.slice(0, ++i).join('');
        if (i < chars.length) b.timer = setTimeout(step, 25); else type.classList.remove('on');
      })();
    };
    b.addEventListener('click', function () {
      if (!b.typed) b.typeLine();
      b.done = true; clearTimeout(b.timer); type.textContent = text; type.classList.remove('on');
    });
  });
  if (!('IntersectionObserver' in window)) { bubbles.forEach(function (b) { b.typeLine(); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.typeLine(); io.unobserve(e.target); } });
  }, { threshold: 0.6 });
  bubbles.forEach(function (b) { io.observe(b); });
})();
