# The Outpost

An interactive portfolio website you explore like a small game.

A penguin guide named Ping stands on a seaside cliff. Dive in and the view
travels down into an underwater cavern, where five objects each open a panel:

| Object | Opens |
| --- | --- |
| Bookshelf | Skills, grouped by shelf |
| Computer | Projects, as a terminal you can browse |
| Bulletin board | Work experience and education |
| Easel and frames | An art gallery |
| Mailbox | Contact links and a message form |

A sidebar gives direct links to every panel, a **VIEW RESUME** button shows the
CV as pages with a PDF download, and a switch changes the sky between sunrise
and a starry night.

## Run it on your computer

You only need **Python 3** (preinstalled on macOS and most Linux systems).

```
python3 gen/build.py     # build the page
python3 gen/serve.py     # open http://localhost:8000
```

After changing any file, run `python3 gen/build.py` again and refresh the
browser.

## How it is built

There is no framework, no package manager and nothing to install.

* **One page.** The whole site is a single 1440 by 900 scene that scales to
  fit the browser window. Its markup, styles and logic live in one template,
  `gen/main_template.html`.
* **Content kept separately.** Every fact shown on the site (skills, projects,
  jobs, links, artwork) lives in one file, `gen/content.py`. A build script
  merges it into the template, so a change is made in one place only.
* **A tiny runtime.** The template uses a small set of tags: `{{name}}` inserts
  a value, `<sc-if>` shows something conditionally and `<sc-for>` repeats it.
  `static/dc-runtime.js` (about 200 lines) turns that into the live page in the
  browser.
* **Built in checks.** Every build is checked for common mistakes, such as a
  missing value or an unclosed tag, and nothing is written if a check fails.
* **Graphics.** The scenery is drawn with SVG and CSS. Characters, artwork and
  resume pages are image files, kept crisp with `image-rendering: pixelated`.
* **Fonts.** Press Start 2P for labels and VT323 for text, from Google Fonts.
* **Contact.** The message form opens the visitor's own email app with the
  message filled in, so no server is needed.

## Project structure

```
gen/                           source code and build scripts
  content.py                   all site content, start here
  main_template.html           the page: layout, styles and interactive logic
  panels.py                    turns content.py into pieces of the page
  parts.json                   pixel art for the reef, fish, mailbox and icons
  build.py                     assembles the page and runs the checks
  check.py                     the checks every build must pass
  serve.py                     local preview server
  export.py                    produces the final website folder, site/
  resume_pages.js              turns a resume PDF into page images (macOS only)
static/
  dc-runtime.js                runs the page in the browser
  _blob/                       images and the resume PDF
.github/workflows/pages.yml    publishes the site to GitHub Pages
```

`build/`, `site/` and `out/` are created by the scripts and are not part of the
repository.

## Making changes

**Text, skills, projects, experience and links:** edit `gen/content.py` and
rebuild. For example, the skills panel is the `SKILL_SHELVES` list, one line
per shelf with its name, colour and skills.

**Other wording** (the welcome message, the guide's speech lines, the sky
descriptions) is in `gen/main_template.html`.

**Images and files** live in `static/_blob/`, each named with an id plus its
extension, for example `3df64a6d88fe4f43c3836fb9e775d86e.png`. The site refers
to them as `/_blob/<id>`. To add one, copy it in under a new id (`md5 -q
<file>` prints a suitable one on macOS) and use that id in `content.py`.

**A new resume:**

1. Render its pages:
   `osascript -l JavaScript gen/resume_pages.js path/to/resume.pdf`
   (writes `out/resume-page-1.png`, `out/resume-page-2.png` and so on).
2. Copy the PDF and the page images into `static/_blob/` under new ids, delete
   the old ones, and update `RESUME_PDF_BLOB` and `RESUME_PAGES` in
   `content.py`.
3. Rebuild and check the preview.

**New artwork:** copy the image into `static/_blob/`, add its id and a short
description to `ARTWORKS` in `content.py`, and rebuild. The gallery grid grows
by itself.

**The typing effect:** any element with `class="typed"` types itself out. Set
`--n` in its style to the number of characters in the text.

## Publishing

The site is published with GitHub Pages. Every push to the `main` branch runs
the workflow in `.github/workflows/pages.yml`, which builds the site and
publishes it. Progress shows in the repository's **Actions** tab.

To set it up in a new repository, open **Settings > Pages** and set
**Source** to **GitHub Actions**. If a deploy fails, start a new run from
**Actions > Deploy to GitHub Pages > Run workflow** rather than re running the
failed one.

To preview exactly what gets published:

```
python3 gen/build.py && python3 gen/export.py
cd site && python3 -m http.server 8001     # open http://localhost:8001
```

The `site/` folder is plain static files, so it can also be hosted on Netlify,
Vercel, Cloudflare Pages or any web server. Use the build command
`python3 gen/build.py && python3 gen/export.py` and the output folder `site`.

## Rules for editing the template

The build checks enforce these, because breaking them makes parts of the page
silently disappear:

* The JavaScript class in the template never edits the page directly (no
  `document`, `innerHTML` and similar). It only updates its state, and the
  runtime redraws the page.
* Text inputs use `onChange`, not `onInput`.
* `{{name}}` looks up a value; it cannot contain a calculation. Calculate it in
  `renderVals()` instead.
* Every `<sc-if>` and `<sc-for>` carries a `hint-*` attribute.
* Text on the page uses no em or en dashes.
* Labels in the pixel font use plain letters (RESUME, not RÉSUMÉ), because the
  font has no accented capitals.
