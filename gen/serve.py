"""Serve the built artboard on localhost: the page from build/Main.dc.html, the
runtime from static/dc-runtime.js, and images and the PDF from static/_blob/.

    python3 gen/serve.py          # http://localhost:8000
    python3 gen/serve.py 8080     # another port

The page is re-read from build/Main.dc.html on every request, so after
python3 gen/build.py a browser refresh is enough."""
import http.server, importlib, mimetypes, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content, panels

HERE = pathlib.Path(__file__).parent
BOARD = HERE.parent / "build" / "Main.dc.html"
STATIC = HERE.parent / "static"

def page():
    importlib.reload(content)          # pick up edits without restarting the server
    importlib.reload(panels)
    html = BOARD.read_text()
    helmet = re.search(r"<helmet>(.*?)</helmet>", html, re.S).group(1)
    body = re.search(r"</helmet>(.*?)</x-dc>", html, re.S).group(1)
    script = re.search(r"<script type=\"text/x-dc\" data-dc-script data-props='([^']*)'>(.*?)</script>", html, re.S)
    title = re.search(r"<title>.*?</title>", html, re.S).group(0)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{title}
<meta name="description" content="Hari Priya, software engineer. An interactive portfolio: follow Ping the penguin through an underwater cavern of skills, projects, experience and art.">
<link rel="canonical" href="{panels._html(content.SITE_URL)}">
<meta property="og:url" content="{panels._html(content.SITE_URL)}">
<meta property="og:type" content="website">
<meta property="og:title" content="Hari Priya's Outpost">
<meta property="og:description" content="An interactive portfolio you walk around with Ping the penguin.">
<link rel="icon" type="image/png" href="/_blob/cf2a3e2a7784c9056665ce1bcd502887">
{helmet}
<style>html,body{{height:100%;overflow:hidden}}</style>
</head>
<body>
{panels.mobile_view()}
<div id="dc-root"></div>
<template id="dc-tpl">{body}</template>
<script type="text/x-dc" id="dc-src" data-props='{script.group(1)}'>{script.group(2)}</script>
<script src="/dc-runtime.js"></script>
</body>
</html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self.send(page().encode(), "text/html; charset=utf-8")
        if path == "/dc-runtime.js":
            return self.send((STATIC / "dc-runtime.js").read_bytes(), "text/javascript")
        m = re.fullmatch(r"/_blob/([0-9a-f]{32})", path)
        if m:
            found = list((STATIC / "_blob").glob(m.group(1) + ".*"))
            if found:
                kind = mimetypes.guess_type(found[0].name)[0] or "application/octet-stream"
                return self.send(found[0].read_bytes(), kind)
            print(f"  missing asset {path}: put the file in static/_blob/ as {m.group(1)}.<ext>")
        self.send_error(404)

    def send(self, data, kind):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"serving the outpost at http://localhost:{port}  (ctrl+c to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
