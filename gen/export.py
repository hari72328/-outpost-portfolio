"""Export the built artboard as a static website in site/, for GitHub Pages or
any static host.

    python3 gen/build.py && python3 gen/export.py

It is the page gen/serve.py serves, made portable: every URL becomes relative
(so it works under a sub-path like user.github.io/repo/), and each /_blob/<id>
points at the real file, static/_blob/<id>.<ext>, since a static host cannot
guess an extension. Only the files the page uses are copied.
"""
import pathlib, re, shutil, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import serve

HERE = pathlib.Path(__file__).parent
STATIC = HERE.parent / "static"
SITE = HERE.parent / "site"


def main():
    html = serve.page().replace('<script src="/dc-runtime.js">', '<script src="dc-runtime.js">')
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "_blob").mkdir(parents=True)

    missing = []
    def static_file(m):
        found = sorted((STATIC / "_blob").glob(m.group(1) + ".*"))
        if not found:
            missing.append(m.group(1))
            return m.group(0)
        shutil.copyfile(found[0], SITE / "_blob" / found[0].name)
        return "_blob/" + found[0].name
    html = re.sub(r"/_blob/([0-9a-f]{32})", static_file, html)
    if missing:
        sys.exit("no file in static/_blob/ for: " + ", ".join(sorted(set(missing))))

    (SITE / "index.html").write_text(html)
    shutil.copyfile(STATIC / "dc-runtime.js", SITE / "dc-runtime.js")
    (SITE / ".nojekyll").write_text("")          # serve _blob/ as-is on GitHub Pages
    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in files)
    print(f"exported {len(files)} files ({size / 1e6:.1f} MB) to {SITE}")


if __name__ == "__main__":
    main()
