# The Outpost

A portfolio you can walk around. Ping the penguin waits on a sunrise (or starry
night) shore, dives into an underwater cavern, and five objects down there open
close up panels: skills, projects, experience, the art studio and a mailbox.
VIEW RESUME opens the CV itself, and a toggle swaps the sky.

## Quick start

```
python3 gen/build.py     # build the page
python3 gen/serve.py     # preview it at http://localhost:8000
```

Python 3 is the only requirement.

## Layout

```
gen/                        everything you edit, plus the build
  content.py                every fact on the site, written once, start here
  main_template.html        the page: markup, styles and the component class
  panels.py                 turns content.py into markup and JS for the template
  parts.json                sprite markup (reef, fish, mailbox, logos)
  build.py                  fills the template, runs the checks, writes build/
  check.py                  the checks a build must pass
  serve.py                  local preview server
  export.py                 the static website for GitHub Pages, into site/
  resume_pages.js           turns the resume PDF into page images (macOS only)
static/
  dc-runtime.js             the small runtime that renders the page
  _blob/                    every image and the resume PDF, named <id>.<ext>
.github/workflows/pages.yml build, export and deploy to GitHub Pages

Generated, not committed: build/ (build.py), site/ (export.py), out/ (resume_pages.js)
```

## How it works

No framework, no bundler, no package manager, no dependencies.

* **The page** is one 1440x900 artboard in `gen/main_template.html`: plain
  HTML with inline styles, one `<style>` block for animations and shared
  classes, and one JavaScript class, `Component extends DCLogic`, that holds
  state and returns the values the markup reads.
* **Templating:** `{{hole}}` for values, `<sc-if>` for branches, `<sc-for>` for
  repeats, `onClick="{{fn}}"` for events. `static/dc-runtime.js` renders it in
  the browser and scales the artboard to fit the window. The format comes from
  claude.ai Design artifacts, where the page was first built.
* **The build:** `%%NAME%%` placeholders in the template are filled by
  `build.py`, from `panels.py` (content) and `parts.json` (sprites).
* **Graphics:** scenery is inline SVG and CSS shapes. Ping, the painting, the
  artwork and the resume pages are images, drawn at whole number scales with
  `image-rendering: pixelated`.
* **Fonts:** Press Start 2P for labels and VT323 for body text, from Google Fonts.
* **Contact:** the mailbox builds a `mailto:` link, so the visitor's own mail
  app sends the letter. There is no server.

## Common changes

**Text, dates, projects, skills, links.** Edit `gen/content.py`, then
`python3 gen/build.py`. The skills archive is `SKILL_SHELVES` (one line per
shelf: name, colour, skills). The sidebar, contact panel and mail link read
`NAME`, `ROLE`, `EMAIL` and `LINKEDIN_*` from there.

**Copy that is not a CV fact** (the welcome card, Ping's lines, the sky notes)
lives in `gen/main_template.html`. Rebuild after editing.

**A new resume.**

1. From the project folder, render its pages:
   `osascript -l JavaScript gen/resume_pages.js path/to/new.pdf`, which writes
   `out/resume-page-N.png`.
2. Copy the PDF and each page image into `static/_blob/` as `<id>.<ext>`, and
   put those `/_blob/<id>` values in `RESUME_PDF_BLOB` and `RESUME_PAGES` in
   `content.py`. Any 32 hex characters make an id; `md5 -q <file>` gives one.
   Delete the old files from `static/_blob/`.
3. Rebuild and check the preview.

**New artwork.** Copy the image into `static/_blob/` as `<id>.<ext>`, add
`/_blob/<id>` and a line of alt text to `ARTWORKS` in `content.py`, and rebuild.
The wall is a three column grid that grows by itself.

**The typewriter line.** Any element with `class="typed"` types itself out.
Set `--n` in its style to the number of characters, or the line is cut off.

## Deploying

Push to `main`. The workflow in `.github/workflows/pages.yml` runs `build.py`
and `export.py` and publishes `site/` to GitHub Pages; the Actions tab shows
progress. (First time setup: **Settings > Pages > Source: GitHub Actions**.)

To see exactly what will be published:

```
python3 gen/build.py && python3 gen/export.py
cd site && python3 -m http.server 8001     # http://localhost:8001
```

## House rules

* **Never touch the DOM from the component class.** No `document.*`,
  `innerHTML`, `appendChild`, `createElement`, `Blob` or `URL`. Inputs are
  controlled through state; files are plain `<a download>` links.
* **Controlled inputs use `onChange`**, not `onInput`.
* **`{{hole}}` is a lookup, never an expression.** Compute in `renderVals()`.
* **Every `<sc-if>` and `<sc-for>` needs its `hint-*` attribute.**
* **No em or en dashes in copy.**
* **Pixel font labels use plain letters.** Press Start 2P has no capital
  accented letters, so labels say RESUME, not RÉSUMÉ. Body text can use them.

These keep the page valid for the Design format it comes from. `gen/check.py`
runs on every build and blocks the write if any fail: every `{{hole}}`
resolves; paired tags balance; every `<sc-if>` and `<sc-for>` has its hint; no
banned DOM calls; no `onInput`; no expressions in holes; no em or en dashes,
however they are written; and the component class parses as JavaScript
(`node --check`, or a bracket balance fallback without node).

## The component class

`renderVals()` is composed of four parts:

* `palette(night)`: every colour that depends on the sky
* `scenery()`: the procedural lists (stars, bubbles, shelves), all drawn from one
  seed so they fall the same way on every render
* `navigation(st, night)`: the sidebar rows and the place name
* `renderVals()`: state, the three above, and the event handlers
