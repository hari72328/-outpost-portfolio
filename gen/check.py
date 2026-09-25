"""Checks the built artboard must pass. build.py runs these on every build.

Each one corresponds to a failure that renders silently rather than erroring: a hole
with no value renders blank, an unclosed tag swallows the rest of the page,
a missing hint- attribute breaks the streaming placeholder, and a DOM call in
the component class makes the whole artboard render "An error occurred".
"""
import re, shutil, subprocess, tempfile

BANNED_IN_LOGIC = ("document.", "innerHTML", "appendChild", "createElement",
                   "window.location", "new Blob", "URL.createObjectURL")
PAIRED_TAGS = ("div", "span", "sc-if", "sc-for", "button", "a", "section",
               "nav", "form", "textarea", "p", "h1", "h2", "h3", "article", "svg")


def run(html):
    """Return a list of problems; empty means the artboard is safe to publish."""
    bad = []
    cut = html.index('<script type="text/x-dc"')
    markup, logic = html[:cut], html[cut:]

    # every {{hole}} resolves to something renderVals() returns or a loop variable
    holes = set(re.findall(r"\{\{([a-zA-Z_$][\w$]*)\}\}", markup))
    known = set(re.findall(r"([a-zA-Z_$][\w$]*)\s*:", logic))
    known |= set(re.findall(r"(?:const|let|var)\s+([a-zA-Z_$][\w$]*)", logic))
    known |= set(re.findall(r'as="([\w$]+)"', markup)) | {"true", "false"}
    for h in sorted(holes - known):
        bad.append("hole {{%s}} has no value in renderVals()" % h)

    for tag in PAIRED_TAGS:
        opens = len(re.findall(r"<%s[\s>]" % tag, html))
        closes = len(re.findall(r"</%s>" % tag, html))
        if opens != closes:
            bad.append("<%s> unbalanced: %d open, %d close" % (tag, opens, closes))

    # streaming placeholders
    for tag, attr in (("sc-if", "hint-placeholder-val"), ("sc-for", "hint-placeholder-count")):
        total = len(re.findall(r"<%s" % tag, html))
        hinted = len(re.findall(r"<%s[^>]*%s" % (tag, attr), html))
        if total != hinted:
            bad.append("%d of %d <%s> missing %s" % (total - hinted, total, tag, attr))

    for call in BANNED_IN_LOGIC:
        if call in logic:
            bad.append("component class calls %s, which the runtime rejects" % call)

    # controlled inputs need onChange; onInput leaves them read-only in React
    if "onInput" in markup:
        bad.append("onInput found; controlled inputs must use onChange")

    for hole in re.findall(r"\{\{[^}]*[+()!][^}]*\}\}", markup):
        bad.append("%s is an expression; holes are lookups only" % hole)

    # house style: copy carries no em or en dashes, however they are spelled
    for dash in ("—", "–", "\\u2014", "\\u2013", "&mdash;", "&ndash;", "&#8212;", "&#8211;"):
        for line in [l.strip() for l in html.splitlines() if dash in l][:3]:
            bad.append("dash %r in: %s" % (dash, line[:80]))

    bad += _js_parses(logic)
    return bad


def _js_parses(logic):
    """The component class must be valid JavaScript. A syntax error here renders
    the whole artboard as "An error occurred" with nothing in the page to show why."""
    src = logic[logic.index(">") + 1:logic.rindex("</script>")]
    node = shutil.which("node")
    if not node:                      # no node: fall back to bracket balance
        depth = {"{": 0, "(": 0, "[": 0}
        pairs = {"}": "{", ")": "(", "]": "["}
        for ch in re.sub(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|/\*.*?\*/", "", src, flags=re.S):
            if ch in depth:
                depth[ch] += 1
            elif ch in pairs:
                depth[pairs[ch]] -= 1
        off = [k for k, v in depth.items() if v]
        return ["component class has unbalanced %s" % ", ".join(off)] if off else []
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write("class DCLogic{}\n" + src)
        path = fh.name
    r = subprocess.run([node, "--check", path], capture_output=True, text=True)
    if r.returncode:
        first = [l for l in r.stderr.splitlines() if "Error" in l or "^" in l][:2]
        return ["component class is not valid JavaScript: " + " ".join(x.strip() for x in first)]
    return []


if __name__ == "__main__":
    import pathlib, sys
    built = pathlib.Path(__file__).resolve().parent.parent / "build" / "Main.dc.html"
    problems = run(built.read_text())
    print("\n".join("  " + p for p in problems) if problems else "  all checks pass")
    sys.exit(1 if problems else 0)
