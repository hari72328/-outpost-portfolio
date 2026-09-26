"""Turn gen/content.py into the pieces of the page.

The laptop world: each entry in PARTS fills the %%NAME%% of the same name in
main_template.html. Fragments are markup, except the *_JS ones, which are
JavaScript source for the component class.

The phone page: mobile_view() builds its markup from the same content, with its
styles in mobile.css and its behaviour in mobile.js; serve.py (and so export.py)
places it next to the world.
"""
import json, pathlib

import content


# ---- helpers ----------------------------------------------------------------
def _asset(name):
    """A file next to this one, read fresh each build (the phone page's CSS and JS)."""
    return (pathlib.Path(__file__).parent / name).read_text()


def _js(text):
    """Escape text for a single-quoted JavaScript string."""
    return text.replace("\\", "\\\\").replace("'", "\\'")


def _html(text):
    """Escape text for HTML content or a double-quoted attribute."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


_SPRITES = json.loads((pathlib.Path(__file__).parent / "parts.json").read_text())


_ICONS = {
    "resume": '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M6 2h9l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15 2v5h5M9 12h8M9 16h8" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M3 6l9 7 9-7" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>',
    "github": '<svg viewBox="0 0 16 16" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="2" y="2" width="20" height="20" fill="currentColor"/><rect x="6" y="9.5" width="3" height="8.5" style="fill:var(--surface,#0b1226)"/><rect x="6" y="5" width="3" height="3" style="fill:var(--surface,#0b1226)"/><path d="M11 18V9.5h3v1.3c.6-.9 1.6-1.5 3-1.5 2.1 0 3 1.4 3 3.8V18h-3v-4.6c0-1.2-.4-1.8-1.4-1.8s-1.6.7-1.6 1.8V18z" style="fill:var(--surface,#0b1226)"/></svg>',
}


SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


# ---- the laptop world: fragments for main_template.html -----------------------
def _role(title, sub, dates, card, pin, bullets, skills=(), expandable=True):
    """One role on the experience timeline. Always shown: the title, company and
    dates. The bullets (and the skills used) open on click, so the timeline stays
    easy to scan. Shared by the laptop panel and the phone page."""
    h = _html
    items = "".join('<li style="margin: 0 0 8px;">%s</li>' % h(b) for b in bullets)
    points = '<ul style="margin: 0; padding-left: 20px; font: 400 16px/1.55 %s; color: #1b1f3b;">%s</ul>' % (SANS, items)
    if skills:
        points += ('<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 12px;">'
                   '<span style="font: 600 13px/1 %s; color: #57534e; margin-right: 2px;">Skills used:</span>%s</div>'
                   % (SANS, "".join('<span style="padding: 4px 9px; font: 500 13px/1.2 %s; color: #1b1f3b; '
                                    'background: rgba(255,255,255,.7); border: 2px solid #1b1f3b;">%s</span>' % (SANS, h(k))
                                    for k in skills)))
    if expandable:
        points = ('<details class="role-more"><summary class="pf">'
                  '<span class="when-closed">VIEW DETAILS</span><span class="when-open">HIDE DETAILS</span>'
                  '</summary><div style="padding-top: 14px;">%s</div></details>' % points)
    date_pill = ('<span style="flex: none; padding: 5px 10px; font: 600 13px/1.2 %s; color: #fdf1d6; background: #1b1f3b;">%s</span>'
                 % (SANS, h(dates))) if dates else ""
    return (
        '<article class="role" style="position: relative; display: flex; flex-direction: column; gap: 14px; '
        'padding: 20px 22px; background: %s; color: #1b1f3b; box-shadow: 5px 5px 0 rgba(0,0,0,.3);">' % card
        + '<span aria-hidden="true" style="position: absolute; left: -33px; top: 24px; width: 16px; height: 16px; '
          'background: %s; border: 3px solid #1b1f3b; box-sizing: border-box;"></span>' % pin
        + '<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 8px 14px;">'
          '<div><div class="pf" style="font-size: 12px; line-height: 1.5;">%s</div>'
          '<div style="margin-top: 4px; font: 500 16px/1.3 %s; color: #57534e;">%s</div></div>%s</div>'
          % (h(title), SANS, h(sub), date_pill)
        + points + "</article>")


def _timeline(cards):
    """The roles on a vertical line, a dot for each."""
    return ('<div style="position: relative; display: flex; flex-direction: column; gap: 20px; '
            'margin-left: 12px; padding-left: 26px; border-left: 4px solid rgba(27,31,59,.35);">%s</div>' % "".join(cards))


def _roles():
    cards = [_role(r["title"], r["where"], r["dates"], r["card"], r["pin"], r["bullets"], r.get("skills", []))
             for r in content.EXPERIENCE]
    ed = content.EDUCATION_CARD
    cards.append(_role(ed["title"], ed["org"], "", ed["card"], ed["pin"],
                       [" \u00b7 ".join(x for x in (e["degree"], e["where"], e["dates"], e["note"]) if x)
                        for e in content.EDUCATION], expandable=False))
    return _timeline(cards)


def experience_articles():
    """The laptop's experience panel: every role in full on the timeline."""
    return _roles()


def projects_js():
    """The array the projects terminal lists and runs."""
    rows = []
    for p in content.PROJECTS:
        stack = ", ".join("'%s'" % _js(s) for s in p["stack"])
        rows.append(
            "  { num: '%s', slug: '%s', name: '%s', tag: '%s',\n"
            "    desc: '%s',\n"
            "    desc2: '%s',\n"
            "    stack: [%s] }"
            % (p["num"], _js(p["slug"]), _js(p["name"]), _js(p["tag"]),
               _js(p["desc"]), _js(p["desc2"]), stack))
    return "const PROJECTS = [\n" + ",\n".join(rows) + "\n];"


def skill_books_js():
    """Spine labels for the bookshelf."""
    return "const titles = [" + ", ".join("'%s'" % _js(t) for t in content.SKILL_BOOKS) + "];"


def skill_shelves():
    """The skills archive: each shelf is one row, its label on the left and its
    books on the right, standing on a single plank, so a label can only belong
    to the books beside it."""
    esc = _html
    rows = []
    for label, colour, books in content.SKILL_SHELVES:
        spines = "".join(
            '<span class="book" style="display: inline-flex; align-items: center; gap: 8px; padding: 4px 10px 4px 7px; '
            f'background: {colour}; border: 3px solid #2a170d; box-shadow: inset 0 4px 0 rgba(255,255,255,.2), '
            'inset 0 -4px 0 rgba(0,0,0,.28), 2px 2px 0 rgba(0,0,0,.35);">'
            '<span style="width: 6px; height: 22px; background: #f3e6c8;"></span>'
            f'<span style="font-size: 22px; line-height: 1; color: #fdf3e0;">{esc(b)}</span></span>'
            for b in books)
        rows.append(
            '<div style="display: grid; grid-template-columns: 132px 1fr; gap: 12px; align-items: center; padding: 6px 10px;">'
            f'<div class="pf" style="font-size: 10px; line-height: 1.7; color: #fbe3a6;">{esc(label)}</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 7px;">{spines}</div></div>'
            '<div style="height: 8px; margin: 0 4px; background: #6d4728; box-shadow: inset 0 4px 0 rgba(255,255,255,.14), 0 4px 8px rgba(0,0,0,.45);"></div>')
    extras = " &middot; ".join(esc(x) for x in content.SKILL_EXTRAS)
    rows.append('<p style="margin: 0; padding: 10px 12px 0; font-size: 22px; line-height: 1.25; color: #e0c69a;">'
                f'Smaller volumes: {extras}</p>')
    return '<div style="display: flex; flex-direction: column;">' + "".join(rows) + "</div>"


def resume_pages():
    """The resume panel: each page of the PDF as an image, stacked like a PDF viewer."""
    pages = content.RESUME_PAGES
    return "\n".join(
        f'<img src="{src}" width="900" height="1273" alt="Hari Priya\'s r&eacute;sum&eacute;, '
        f'page {i} of {len(pages)}. DOWNLOAD PDF has the same r&eacute;sum&eacute; as selectable text." '
        'style="display: block; flex-shrink: 0; width: 900px; height: auto; background: #fff; '
        'box-shadow: 0 6px 18px rgba(0,0,0,.35);">'
        for i, src in enumerate(pages, 1))


def ping_lines_js():
    """Ping's lines as the object lines() returns: one list of lines per place."""
    rows = ["      %s: ['%s']" % (place, _js(line))
            for place, line in content.PING_LINES.items()]
    return "{\n" + ",\n".join(rows) + "\n    }"


def artworks_js():
    """The studio wall as data, so each piece can carry its own click handler."""
    rows = ["  { blob: '%s', alt: '%s' }" % (a["blob"], _js(a["alt"]))
            for a in content.ARTWORKS]
    return "const ARTWORKS = [\n" + ",\n".join(rows) + "\n];"


def github_button():
    """The laptop contact panel's GitHub button, or nothing when GITHUB_URL is empty."""
    if not content.GITHUB_URL:
        return ""
    return ('<a class="cbtn" href="%s" target="_blank" rel="noopener noreferrer" style="flex: 1; display: flex; '
            'align-items: center; justify-content: center; gap: 14px; padding: 12px 16px; background: #f3ece0; '
            'color: #14243c; text-decoration: none; box-shadow: 4px 4px 0 rgba(0,0,0,.4);">'
            '<span style="line-height: 0;">%s</span><span style="font-size: 26px; line-height: 1;">GitHub</span></a>'
            % (_html(content.GITHUB_URL), _ICONS["github"].replace('width="22" height="22"', 'width="30" height="30"')))


def availability_line():
    """The laptop sidebar's availability line under the name: the short form of
    the phone's line (AVAILABILITY only), or nothing when it is empty."""
    if not content.AVAILABILITY:
        return ""
    return ('<div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 4px; '
            'font-size: 18px; line-height: 1.1; color: #86efac; white-space: nowrap;">'
            '<span class="avail-dot" aria-hidden="true"></span>%s</div>' % _html(content.AVAILABILITY.rstrip(".")))


def name_letters():
    """The laptop sidebar name: the full name for screen readers, then one span
    per letter so each can move on its own (see .sb-name in main_template.html)."""
    letters = "".join('<span class="nl-sp"> </span>' if c == " " else
                      '<span class="nl" style="--i: %d;">%s</span>' % (i, _html(c))
                      for i, c in enumerate(content.NAME))
    return '<span class="sr-only">%s</span><span aria-hidden="true">%s</span>' % (_html(content.NAME.title()), letters)


# ---- the phone page -------------------------------------------------------------
def _links(labels=False):
    """Resume as the main button, email and LinkedIn as square icon buttons
    (or, with labels, short labelled buttons), never the raw address or URL."""
    h = _html
    gh = h(content.GITHUB_URL)
    gh_label = ('<a class="lbtn" href="%s" target="_blank" rel="noopener">%s<span>GitHub</span></a>' % (gh, _ICONS["github"])) if gh else ""
    gh_icon = ('<a class="ibtn" href="%s" target="_blank" rel="noopener" aria-label="GitHub profile" title="GitHub">%s</a>' % (gh, _ICONS["github"])) if gh else ""
    if labels:
        return ('<div class="links labelled">'
                '<button class="lbtn copy" type="button" data-email="%s">%s<span>Copy email</span></button>'
                '<a class="lbtn" href="%s" target="_blank" rel="noopener">%s<span>LinkedIn</span></a>%s</div>'
                % (h(content.EMAIL), _ICONS["mail"], h(content.LINKEDIN_URL), _ICONS["linkedin"], gh_label))
    return ('<div class="links">'
            '<a class="resume-btn pf" href="%s" target="_blank" rel="noopener">%s<span>RESUME</span></a>'
            '<a class="ibtn" href="#m-contact" aria-label="Send Hari Priya a message" title="Send a message">%s</a>'
            '<a class="ibtn" href="%s" target="_blank" rel="noopener" aria-label="LinkedIn profile" title="LinkedIn">%s</a>%s</div>'
            % (content.RESUME_PDF_BLOB, _ICONS["resume"], _ICONS["mail"], h(content.LINKEDIN_URL), _ICONS["linkedin"], gh_icon))


def mobile_view():
    """The portfolio for phones, where the 1440x900 scene would be far too small
    to read: the same content from content.py as one scrolling page, in one card
    style, coloured by one of two skies (night, the default, or sunrise). serve.py
    adds it beside the scene; CSS shows one or the other by screen size, and the
    Explore world buttons open the full scene anyway."""
    h = _html

    skills = "".join(
        f'<div class="shelf"><div class="shelf-name"><span class="dot" style="background:{colour}"></span>{h(label)}</div><div class="chips">'
        + "".join(f'<span class="chip book" style="--spine:{colour}">{h(s)}</span>' for s in books)
        + "</div></div>"
        for label, colour, books in content.SKILL_SHELVES)
    skills += f'<p class="extra">Also: {" &middot; ".join(h(x) for x in content.SKILL_EXTRAS)}</p>'

    projects = "".join(
        f'<article class="card proj"><div class="proj-top"><span class="proj-num">{h(p["num"])}</span>'
        f'<span class="proj-tag">{h(p["tag"])}</span></div>'
        f'<h3 class="pf">{h(p["name"])}</h3>'
        f'<details class="more"><summary class="pf"><span class="when-closed">VIEW DETAILS</span>'
        f'<span class="when-open">HIDE DETAILS</span></summary>'
        f'<p>{h(p["desc"])}</p><p>{h(p["desc2"])}</p>'
        f'<div class="chips">{"".join(f"<span class=chip>{h(s)}</span>" for s in p["stack"])}</div></details></article>'
        for p in content.PROJECTS)

    def role(title, sub, dates, pin, bullets, skills=(), expandable=True):
        pts = "<ul class=\"pts\">" + "".join(f"<li>{h(b)}</li>" for b in bullets) + "</ul>"
        if skills:
            pts += ('<div class="used"><span>Skills used:</span>'
                    + "".join(f'<span class="chip">{h(k)}</span>' for k in skills) + "</div>")
        if expandable:
            pts = ('<details class="more"><summary class="pf"><span class="when-closed">VIEW DETAILS</span>'
                   f'<span class="when-open">HIDE DETAILS</span></summary>{pts}</details>')
        pill = f'<span class="pill">{h(dates)}</span>' if dates else ""
        return (f'<article class="card mrole"><span class="mdot" style="background:{pin}"></span>'
                f'<div class="mrole-head"><div><h3 class="pf">{h(title)}</h3><div class="sub">{h(sub)}</div></div>{pill}</div>{pts}</article>')
    jobs = ('<div class="cork"><div class="tl">'
            + "".join(role(r["title"], r["where"], r["dates"], r["pin"], r["bullets"], r.get("skills", []))
                      for r in content.EXPERIENCE)
            + role(content.EDUCATION_CARD["title"], content.EDUCATION_CARD["org"], "", content.EDUCATION_CARD["pin"],
                   [" \u00b7 ".join(x for x in (e["degree"], e["where"], e["dates"], e["note"]) if x) for e in content.EDUCATION],
                   expandable=False)
            + "</div></div>")

    art = "".join(f'<figure class="frame"><img src="{a["thumb"]}" alt="{h(a["alt"])}" width="360" height="360"></figure>'
                  for a in content.ARTWORKS[:content.STUDIO_PHONE_COUNT])

    email, linkedin, pdf = h(content.EMAIL), h(content.LINKEDIN_URL), content.RESUME_PDF_BLOB
    name_letters = "".join('<span class="sp" aria-hidden="true"> </span>' if c == " " else
                           '<span class="ch" aria-hidden="true" style="--i:%d">%s</span>' % (i, h(c))
                           for i, c in enumerate(content.NAME))
    explore_js = "outpostWorld(true)"
    avail = (f'<p class="avail"><span class="live" aria-hidden="true"></span>'
             f'<span><strong>{h(content.AVAILABILITY)}</strong> {h(content.AVAILABILITY_MORE)}</span></p>\n') if content.AVAILABILITY else ""
    return f"""<style>
{_asset('mobile.css')}</style>
<button id="m-back" class="pf" type="button" onclick="history.state &amp;&amp; history.state.world ? history.back() : outpostWorld(false)">BACK TO QUICK VIEW</button>
<main id="mobile" class="night">
<script>try {{ if (localStorage.getItem('outpost-sky') === 'sunrise') document.getElementById('mobile').classList.remove('night'); }} catch (e) {{}}</script>
<button class="sky-btn" type="button" aria-label="Switch to night sky" title="Sky: sunrise or night"><svg class="sun" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="8" y="8" width="8" height="8" fill="currentColor"/><path d="M11 1h2v4h-2zM11 19h2v4h-2zM1 11h4v2H1zM19 11h4v2h-4zM4 4.5l1.5-1.5 2.8 2.8-1.5 1.5zM15.7 17.2l1.5-1.5 2.8 2.8-1.5 1.5zM4 19.5l2.8-2.8 1.5 1.5L5.5 21zM15.7 6.8l2.8-2.8 1.5 1.5-2.8 2.8z" fill="currentColor"/></svg><svg class="moon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M15 3a9 9 0 1 0 6 13A8 8 0 0 1 15 3z" fill="currentColor"/><rect x="18" y="3" width="2" height="2" fill="currentColor"/><rect x="21" y="7" width="2" height="2" fill="currentColor"/></svg></button>
<button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="m-menu"><span></span><span></span><span></span></button>
<div class="menu-shade" hidden></div>
<nav class="menu" id="m-menu" aria-label="Menu" tabindex="-1" hidden>
<div class="menu-head"><a class="pf home" href="#m-top">{h(content.NAME)}</a><button class="menu-close" type="button" aria-label="Close menu">&times;</button></div>
<a href="#m-experience">Experience</a><a href="#m-skills">Skills</a><a href="#m-projects">Projects</a><a href="#m-studio" data-open-art>Studio</a>
<a href="#m-contact">Contact</a>
{_links()}
<button class="explore" type="button" onclick="{explore_js}">EXPLORE WORLD</button>
</nav>
<div class="intro" id="m-top">
<h1 class="pf name" aria-label="{h(content.NAME.title())}">{name_letters}</h1>
<p class="lead">{h(content.INTRO)}</p>
{avail}{_links()}
</div>
<div class="hero"><p class="meet">{h(content.PING_INTRO)}</p>
<img class="ping" src="/_blob/a7f5f6d223d9c34b80f7ce0919da0426" width="79" height="57" alt="Ping the penguin">
<p class="speech"><span class="who pf">PING</span>{h(content.PING_PHONE["hello"])}</p>
<div class="choice pf"><button class="explore" type="button" onclick="{explore_js}">EXPLORE WORLD</button><a class="dive" href="#m-dive">QUICK TOUR</a></div></div>
<div class="sea" id="m-dive">
<section id="m-experience"><h2 class="sec pf" style="--c:#c08a4e">EXPERIENCE<span class="obj">Journey board</span></h2><div class="guide"><img src="/_blob/cf2a3e2a7784c9056665ce1bcd502887" width="36" height="34" alt=""><p class="speech"><span class="who pf">PING</span>{h(content.PING_LINES["experience"])}</p></div>{jobs}</section>
<section id="m-skills"><h2 class="sec pf" style="--c:#b91c1c">SKILLS<span class="obj">Bookshelf</span></h2><div class="guide"><img src="/_blob/cf2a3e2a7784c9056665ce1bcd502887" width="36" height="34" alt=""><p class="speech"><span class="who pf">PING</span>{h(content.PING_LINES["skills"])}</p></div><div class="card">{skills}</div></section>
<section id="m-projects"><h2 class="sec pf" style="--c:#67e8f9">PROJECTS<span class="obj">Computer</span></h2><div class="guide"><img src="/_blob/cf2a3e2a7784c9056665ce1bcd502887" width="36" height="34" alt=""><p class="speech"><span class="who pf">PING</span>{h(content.PING_LINES["projects"])}</p></div><div class="window"><div class="titlebar"><span></span><span></span><span></span><em>~/projects</em></div><div class="stack-list">{projects}</div></div></section>
<section id="m-studio"><h2 class="sec pf" style="--c:#e879f9">STUDIO<span class="obj">Easel &amp; frames</span></h2><div class="guide"><img src="/_blob/cf2a3e2a7784c9056665ce1bcd502887" width="36" height="34" alt=""><p class="speech"><span class="who pf">PING</span>{h(content.PING_PHONE["art"])}</p></div><details class="card studio"><summary class="pf"><span class="when-closed">SEE A FEW OF MY PIECES</span><span class="when-open">HIDE</span></summary><div class="gallery">{art}</div></details></section>
<section id="m-contact"><h2 class="sec pf" style="--c:#fb7185">CONTACT<span class="obj">Mail box</span></h2><div class="guide"><img src="/_blob/cf2a3e2a7784c9056665ce1bcd502887" width="36" height="34" alt=""><p class="speech"><span class="who pf">PING</span>{h(content.PING_LINES["contact"])}</p></div><div>
<form class="card letter airmail" id="m-letter" data-key="{h(content.WEB3FORMS_KEY)}" novalidate>
<span class="stamp" aria-hidden="true"></span><div class="pf letter-title">DROP A LETTER IN</div>
<label>Name<input name="name" type="text" autocomplete="name" placeholder="Your name" aria-describedby="m-err-name"></label>
<p class="err" id="m-err-name" hidden>Name must be at least 2 characters</p>
<label>Email<input name="from" type="email" autocomplete="email" placeholder="you@example.com" aria-describedby="m-err-from"></label>
<p class="err" id="m-err-from" hidden>Please enter a valid email address</p>
<label>Message<textarea name="msg" rows="4" placeholder="Say hi, or tell me about a role you&#39;re hiring for" aria-describedby="m-err-msg"></textarea></label>
<p class="err" id="m-err-msg" hidden>Message must be at least 10 characters</p>
<button class="send pf" type="submit">SEND IT DOWN</button>
<p class="sent-ok" id="m-sent" role="status" hidden>Message sent! Hari Priya will get back to you soon.</p>
<p class="err" id="m-fail" role="alert" hidden>Couldn&#39;t send just now. Please try again, or use Copy email below.</p>
<p class="hint">Your message goes straight to Hari Priya&#39;s inbox.</p>
</form>
<p class="or">Prefer something else?</p>
{_links(labels=True)}</div></section>
<footer class="foot"><a class="top pf" href="#m-top">BACK TO TOP</a></footer>
</div>
</main>
<script>
{_asset('mobile.js')}</script>"""


# ---- every %%NAME%% the build fills --------------------------------------------
PARTS = {
    "NAME_LETTERS": name_letters,
    "ROLE": lambda: _html(content.ROLE),
    "EMAIL_JS": lambda: _js(content.EMAIL),
    "LINKEDIN_URL": lambda: _html(content.LINKEDIN_URL),
    "WEB3FORMS_KEY_JS": lambda: _js(content.WEB3FORMS_KEY),
    "GITHUB_BUTTON": github_button,
    "AVAILABILITY_LINE": availability_line,
    # the mailbox's icons at exactly half size, for the laptop contact buttons
    "LOGO_MAIL_SMALL": lambda: _SPRITES["LOGO_MAIL"].replace('width="90" height="60"', 'width="45" height="30"', 1),
    "LOGO_LINKEDIN_SMALL": lambda: _SPRITES["LOGO_LINKEDIN"].replace('width="70" height="60"', 'width="35" height="30"', 1),
    "RESUME_PDF": lambda: content.RESUME_PDF_BLOB,
    "RESUME_PAGES": resume_pages,
    "EXPERIENCE_ARTICLES": experience_articles,
    "PROJECTS_JS": projects_js,
    "SKILL_BOOKS_JS": skill_books_js,
    "SKILL_SHELVES": skill_shelves,
    "ARTWORKS_JS": artworks_js,
    "PING_LINES_JS": ping_lines_js,
}
