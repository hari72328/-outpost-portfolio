"""Turn gen/content.py into the artboard fragments that carry CV facts.

Each entry in PARTS fills the %%NAME%% of the same name in main_template.html.
Fragments are markup, except the *_JS ones, which are JavaScript source for the
component class.
"""
import content


def _js(text):
    """Escape text for a single-quoted JavaScript string."""
    return text.replace("\\", "\\\\").replace("'", "\\'")


def _html(text):
    """Escape text for HTML content or a double-quoted attribute."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def _card(card, pin, title, org, bullets):
    lines = [
        '<article style="position: relative; padding: 16px 20px; display: flex; '
        'flex-direction: column; gap: 7px; background: %s; color: #1b1f3b; '
        'box-shadow: 5px 5px 0 rgba(0,0,0,.3);">' % card,
        '<span style="position: absolute; left: 50%%; top: -7px; width: 14px; height: 14px; '
        'background: %s; box-shadow: 2px 2px 0 rgba(0,0,0,.45);"></span>' % pin,
        '<div class="pf" style="font-size: 11px; line-height: 1.4;">%s</div>' % title,
        '<div style="font-size: 21px; color: #57534e;">%s</div>' % org,
    ]
    body = "".join('<div style="font-size: 22px; line-height: 1.12;">\u25aa %s</div>' % b
                   for b in bullets)
    return "\n".join(lines) + "\n" + body + "\n</article>"


def experience_articles():
    """One pinned card per role on the bulletin board, then the education card."""
    out = [_card(r["card"], r["pin"], r["title"],
                 "%s \u00b7 %s" % (r["where"], r["dates"]), r["bullets"])
           for r in content.EXPERIENCE]
    ed = content.EDUCATION_CARD
    out.append(_card(ed["card"], ed["pin"], ed["title"], ed["org"], [
        " \u00b7 ".join(x for x in (e["degree"], e["where"], e["dates"], e["note"]) if x)
        for e in content.EDUCATION]))
    return "".join(out)


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


def artworks_js():
    """The studio wall as data, so each piece can carry its own click handler."""
    rows = ["  { blob: '%s', alt: '%s' }" % (a["blob"], _js(a["alt"]))
            for a in content.ARTWORKS]
    return "const ARTWORKS = [\n" + ",\n".join(rows) + "\n];"


PARTS = {
    "NAME": lambda: _html(content.NAME),
    "ROLE": lambda: _html(content.ROLE),
    "EMAIL_JS": lambda: _js(content.EMAIL),
    "LINKEDIN_URL": lambda: _html(content.LINKEDIN_URL),
    "LINKEDIN_TEXT": lambda: _html(content.LINKEDIN_TEXT),
    "RESUME_PDF": lambda: content.RESUME_PDF_BLOB,
    "RESUME_PAGES": resume_pages,
    "EXPERIENCE_ARTICLES": experience_articles,
    "PROJECTS_JS": projects_js,
    "SKILL_BOOKS_JS": skill_books_js,
    "SKILL_SHELVES": skill_shelves,
    "ARTWORKS_JS": artworks_js,
}
