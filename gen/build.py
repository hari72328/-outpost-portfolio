"""Assemble build/Main.dc.html from the template and the generated parts.

    python3 gen/build.py

Every %%NAME%% in main_template.html is filled from parts.json (sprite markup) or
panels.PARTS (content from content.py). The result must pass check.py, or
nothing is written.
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check, panels

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "build" / "Main.dc.html"

def main():
    html = (HERE / "main_template.html").read_text()
    fill = {}
    fill.update(json.loads((HERE / "parts.json").read_text()))
    fill.update({name: make() for name, make in panels.PARTS.items()})
    for key in re.findall(r"%%([A-Z_]+)%%", html):
        if key not in fill:
            sys.exit(f"no content for %%{key}%%")
        html = html.replace(f"%%{key}%%", fill[key])
    left = re.findall(r"%%[A-Z_]+%%", html)
    if left:
        sys.exit(f"unfilled placeholders: {left}")
    problems = check.run(html)
    if problems:
        sys.exit("refusing to write, the artboard would be broken:\n"
                 + "\n".join("  " + p for p in problems))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(html):,} bytes), all checks pass")

if __name__ == "__main__":
    main()
