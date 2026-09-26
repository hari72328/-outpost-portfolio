# The Outpost

A portfolio website you can explore like a small game, with a clean, readable
version for phones.

On a laptop, a penguin guide named Ping stands on a seaside cliff. Dive in and
the view travels down to an underwater cavern where five objects open panels:
a bookshelf (skills), a computer (projects), a bulletin board (experience), an
easel (art) and a mailbox (contact). On a phone, the same content appears as a
simple scrolling page.

No framework, no package manager, nothing to install except Python 3.

**Live site:** https://hpriya03.github.io/outpost-portfolio/

## Features

* **An explorable world** for laptops and desktops, with a sunrise and a night sky
* **A phone version** with a menu, a night and a sunrise theme, and an option to
  open the world anyway
* **A resume viewer** that shows the CV pages and offers the PDF for download
* **A contact form** with validation that delivers messages to your inbox
  (through Web3Forms), plus Copy email, LinkedIn and GitHub buttons
* **One content file:** every name, job, project, skill and artwork is edited in
  one place and appears everywhere
* **Automatic publishing** to GitHub Pages on every push

## Quick start

You need **Python 3** (already installed on macOS and most Linux systems).

```
python3 gen/build.py     # build the page
python3 gen/serve.py     # preview it at http://localhost:8000
```

After any change, run `python3 gen/build.py` again and refresh the browser.

To see the phone version on a computer, open the preview in Chrome, press
**Cmd+Option+I** (Windows: **Ctrl+Shift+I**), then **Cmd+Shift+M** (Windows:
**Ctrl+Shift+M**) and pick a phone.

## Make it your own

Almost everything lives in **`gen/content.py`**. Edit it, rebuild, refresh.

| What | Where in `gen/content.py` |
| --- | --- |
| Name, role, email | `NAME`, `ROLE`, `EMAIL` |
| Your site's address | `SITE_URL` |
| LinkedIn and GitHub links | `LINKEDIN_URL`, `GITHUB_URL` (set to `""` to hide) |
| Phone introduction | `INTRO` |
| "Open to opportunities" line | `AVAILABILITY`, `AVAILABILITY_MORE` (set to `""` to hide) |
| Jobs and education | `EXPERIENCE`, `EDUCATION` |
| Projects | `PROJECTS` |
| Skills | `SKILL_SHELVES` (one line per group: name, colour, skills), `SKILL_EXTRAS` |
| Artwork | `ARTWORKS`, and `STUDIO_PHONE_COUNT` for how many the phone shows |
| What Ping says | `PING_LINES` (both versions), `PING_PHONE` and `PING_INTRO` (phone only) |
| Contact form key | `WEB3FORMS_KEY` (see below) |
| Resume | `RESUME_PDF_BLOB`, `RESUME_PAGES` (see below) |

The laptop welcome message and the sky descriptions are in
`gen/main_template.html`.

### Images and files

Images and the resume PDF live in `static/_blob/`, each named with an id and its
extension, for example `3df64a6d88fe4f43c3836fb9e775d86e.png`. The site refers to
them as `/_blob/<id>`. Any 32 letters and digits make an id; on macOS,
`md5 -q <file>` prints a suitable one.

### Your resume

1. Turn the PDF pages into images (macOS):
   ```
   osascript -l JavaScript gen/resume_pages.js path/to/resume.pdf
   ```
   This writes `out/resume-page-1.png`, `out/resume-page-2.png` and so on.
2. Copy the PDF and the page images into `static/_blob/`, each under a new id.
3. Put those ids in `RESUME_PDF_BLOB` and `RESUME_PAGES`, and rebuild.

### Your artwork

1. Copy the image into `static/_blob/` under a new id.
2. Make a small preview for the phone page and copy it in under its own id:
   ```
   magick art.jpg -resize 360x360 -quality 80 thumb.webp
   ```
   (`magick` is ImageMagick; any tool that makes a small WebP works.)
3. Add an entry to `ARTWORKS` with `blob`, `thumb` and `alt` (a short
   description for screen readers), and rebuild.

### The contact form

Messages are delivered by [Web3Forms](https://web3forms.com), which is free for
up to 250 messages a month.

1. On web3forms.com, create an access key for your email address and enter your
   website's address when asked.
2. Put the key in `WEB3FORMS_KEY` and rebuild.

The key only works from the website address you registered, so sending from
the local preview is expected to fail. Test it on the live site.

## Publish on GitHub Pages

1. Create a GitHub repository and push this project to its `main` branch.
2. In the repository, open **Settings > Pages** and set **Source** to
   **GitHub Actions**.
3. Open the **Actions** tab. After a minute, the run shows a green tick and your
   site is live at `https://<your username>.github.io/<repository name>/`.

Every later push publishes the new version automatically. If a run fails, start
a fresh one from **Actions > Deploy to GitHub Pages > Run workflow**.

To check exactly what will be published:

```
python3 gen/build.py && python3 gen/export.py
cd site && python3 -m http.server 8001     # open http://localhost:8001
```

**Other hosts** (Netlify, Vercel, Cloudflare Pages): use the build command
`python3 gen/build.py && python3 gen/export.py` and the output folder `site`.

## Project structure

```
gen/
  content.py            all the content: start here
  main_template.html    the laptop world: layout, styles and logic
  panels.py             turns content.py into pieces of the page
  mobile.css            the phone version's styles and themes
  mobile.js             the phone version's behaviour
  parts.json            drawings for the reef, fish, mailbox and icons
  build.py              assembles the page and runs the checks
  check.py              the checks every build must pass
  serve.py              the local preview
  export.py             the final website, written to site/
  resume_pages.js       resume PDF to page images (macOS)
static/
  dc-runtime.js         the small script that runs the world in the browser
  _blob/                images and the resume PDF
.github/workflows/      publishes to GitHub Pages
```

`build/`, `site/` and `out/` are generated and not part of the repository.

## How it works

* **The world** is one 1440 by 900 scene that scales to fit the window. Its
  template uses three small tags: `{{name}}` inserts a value, `<sc-if>` shows
  something conditionally and `<sc-for>` repeats it. `static/dc-runtime.js`
  turns that into the live page.
* **The build** fills the template's `%%NAME%%` placeholders from `content.py`
  and checks the result for common mistakes (missing values, unclosed tags,
  invalid JavaScript). If a check fails, nothing is written.
* **The phone version** is built from the same content by `mobile_view()` in
  `gen/panels.py` and shown instead of the world on small screens.
* **Fonts** are Press Start 2P and VT323, from Google Fonts.

## Rules for editing the world's template

The build enforces these, because breaking them makes parts of the page
disappear without an error:

* The JavaScript class never edits the page directly (no `document`,
  `innerHTML` and similar). It only updates its state, and the page redraws.
* Text inputs use `onChange`, not `onInput`.
* `{{name}}` looks up a value and cannot contain a calculation; calculate it in
  `renderVals()` instead.
* Every `<sc-if>` and `<sc-for>` carries a `hint-*` attribute.
* Page text uses no em or en dashes.
* Labels in the Press Start 2P font use plain letters (RESUME, not RÉSUMÉ),
  because the font has no accented capitals.

## Reusing this project

You are welcome to use the code as a starting point. The artwork, the resume and
the personal details in `gen/content.py` and `static/_blob/` belong to the
original author, so please replace them with your own.
