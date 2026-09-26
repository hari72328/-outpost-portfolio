/* The runtime that renders the artboard in the browser. The artboard is written
   for the claude.ai Design format, where this runtime is built in; this file is
   a small re-implementation of just what Main.dc.html uses: DCLogic with
   setState, {{holes}} in text and attributes, <sc-if>, <sc-for>, on* events
   and controlled inputs. gen/serve.py (and so gen/export.py) puts the markup in
   <template id="dc-tpl"> and the component source in <script id="dc-src">. */

class DCLogic {
  constructor(props) { this.props = props || {}; this.state = {}; }
  setState(patch) {
    const p = typeof patch === 'function' ? patch(this.state, this.props) : patch;
    this.state = Object.assign({}, this.state, p);
    scheduleRender();
  }
}

const HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
const ONLY_HOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;
const BOOL_PROPS = { checked: 1, disabled: 1, selected: 1 };

let component = null;
let tplNodes = [];
let root = null;
let pending = false;
let nextId = 0;

/* {{name}} or {{item.field}}; literals only show up in hint-* attributes. */
function lookup(expr, scope) {
  if (expr === 'true') return true;
  if (expr === 'false') return false;
  if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
  let v = scope;
  for (const part of expr.split('.')) {
    if (v == null) return undefined;
    v = v[part];
  }
  return v;
}

function interpolate(text, scope) {
  return text.replace(HOLE, (_, e) => { const v = lookup(e, scope); return v == null ? '' : String(v); });
}

/* React naming: onChange on a text field fires on every keystroke. */
function eventType(attr, el) {
  const t = attr.slice(2);
  if (t === 'change' && (el.localName === 'input' || el.localName === 'textarea')) return 'input';
  if (t === 'doubleclick') return 'dblclick';
  return t;
}

/* Template nodes -> fresh DOM nodes, each keyed by where it came from. */
function build(nodes, scope, path, out) {
  for (const n of nodes) {
    if (n.__id === undefined) n.__id = nextId++;
    const key = n.__id + path;
    if (n.nodeType === Node.TEXT_NODE) {
      const t = document.createTextNode(interpolate(n.data, scope));
      t.__k = key;
      out.push(t);
      continue;
    }
    if (n.nodeType !== Node.ELEMENT_NODE) continue;
    const tag = n.localName;
    if (tag === 'sc-if') {
      if (lookup(n.getAttribute('value').match(ONLY_HOLE)[1], scope)) build(n.childNodes, scope, path, out);
      continue;
    }
    if (tag === 'sc-for') {
      const list = lookup(n.getAttribute('list').match(ONLY_HOLE)[1], scope) || [];
      const as = n.getAttribute('as') || 'item';
      list.forEach((item, i) => {
        const inner = Object.create(scope);
        inner[as] = item;
        build(n.childNodes, inner, path + '/' + i, out);
      });
      continue;
    }
    const el = document.createElementNS(n.namespaceURI, tag);
    el.__k = key;
    el.__on = {};
    el.__props = {};
    for (const a of n.attributes) {
      if (a.name.startsWith('hint-')) continue;
      const only = a.value.match(ONLY_HOLE);
      if (a.name.startsWith('on') && only) {
        el.__on[eventType(a.name, el)] = lookup(only[1], scope);
      } else if ((a.name === 'value' && (tag === 'input' || tag === 'textarea')) || (BOOL_PROPS[a.name] && only)) {
        el.__props[a.name] = only ? lookup(only[1], scope) : a.value;
      } else if (only) {
        const v = lookup(only[1], scope);
        if (v != null && v !== false) el.setAttribute(a.name, v === true && !a.name.startsWith('aria-') ? '' : String(v));
      } else {
        el.setAttribute(a.name, interpolate(a.value, scope));
      }
    }
    const kids = [];
    build(n.localName === 'template' ? n.content.childNodes : n.childNodes, scope, path, kids);
    for (const k of kids) el.appendChild(k);
    out.push(el);
  }
  return out;
}

function bindEvents(el) {
  el.__bound = el.__bound || {};
  for (const type of Object.keys(el.__on)) {
    if (el.__bound[type]) continue;
    el.__bound[type] = true;
    el.addEventListener(type, (e) => { const f = el.__on[type]; if (typeof f === 'function') f(e); });
  }
}

function applyProps(el) {
  for (const [name, v] of Object.entries(el.__props)) {
    if (name === 'value') { const s = v == null ? '' : String(v); if (el.value !== s) el.value = s; }
    else el[name] = !!v;
  }
}

/* Newly inserted subtree: wire up events and controlled values throughout. */
function activate(node) {
  if (node.nodeType !== Node.ELEMENT_NODE) return;
  bindEvents(node);
  applyProps(node);
  for (const c of node.childNodes) activate(c);
}

/* Update live nodes in place so transitions, focus and caret positions survive. */
function patch(live, fresh) {
  if (live.nodeType === Node.TEXT_NODE) { if (live.data !== fresh.data) live.data = fresh.data; return; }
  for (const a of Array.from(live.attributes)) {
    if (a.name === 'open' && live.localName === 'details') continue;   /* opened by the visitor, not by state */
    if (!fresh.hasAttribute(a.name)) live.removeAttribute(a.name);
  }
  for (const a of fresh.attributes) if (live.getAttribute(a.name) !== a.value) live.setAttribute(a.name, a.value);
  live.__on = fresh.__on;
  live.__props = fresh.__props;
  bindEvents(live);
  applyProps(live);
  patchChildren(live, Array.from(fresh.childNodes));
}

function patchChildren(parent, fresh) {
  const byKey = new Map();
  for (const c of parent.childNodes) if (c.__k !== undefined) byKey.set(c.__k, c);
  let cursor = parent.firstChild;
  for (const f of fresh) {
    const live = byKey.get(f.__k);
    if (live && live.nodeType === f.nodeType && live.localName === f.localName) {
      byKey.delete(f.__k);
      if (live !== cursor) parent.insertBefore(live, cursor);
      patch(live, f);
      cursor = live.nextSibling;
    } else {
      parent.insertBefore(f, cursor);
      activate(f);
    }
  }
  while (cursor) { const next = cursor.nextSibling; parent.removeChild(cursor); cursor = next; }
}

function render() {
  pending = false;
  patchChildren(root, build(tplNodes, component.renderVals(), '', []));
}

function scheduleRender() {
  if (pending || !root) return;
  pending = true;
  queueMicrotask(render);
}

/* The artboard is a fixed 1440x900; scale it to fit the window. The root is
   position: fixed so the wide artboard never widens the page, and the size is
   read from the layout viewport: on phones window.innerWidth reports the
   zoomed-out width instead, and the artboard would not shrink. */
function fit() {
  const w = component.__w, h = component.__h;
  const vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
  const k = Math.min(vw / w, vh / h);
  root.style.transform = 'translate(' + (vw - w * k) / 2 + 'px,' + (vh - h * k) / 2 + 'px) scale(' + k + ')';
}

function boot() {
  const src = document.getElementById('dc-src');
  const spec = JSON.parse(src.dataset.props || '{}');
  const props = {};
  for (const [k, v] of Object.entries(spec)) if (!k.startsWith('$') && v && 'default' in v) props[k] = v.default;
  const Component = new Function('DCLogic', src.textContent + '\nreturn Component;')(DCLogic);

  tplNodes = Array.from(document.getElementById('dc-tpl').content.childNodes);
  root = document.getElementById('dc-root');
  component = new Component(props);
  component.props = props;
  const preview = spec.$preview || {};
  component.__w = preview.width || 1440;
  component.__h = preview.height || 900;
  Object.assign(root.style, { position: 'fixed', left: '0', top: '0', transformOrigin: '0 0', width: component.__w + 'px', height: component.__h + 'px' });

  render();
  fit();
  window.addEventListener('resize', fit);
  if (component.componentDidMount) component.componentDidMount();
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
