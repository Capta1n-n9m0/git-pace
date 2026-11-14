"""Git pace: a local web page that shows how much work went into a git repository over time.

Usage:  python gitpace.py [REPO_PATH] [--port 8765] [--no-browser]

Reads the history with `git log --numstat` on every page load (so a refresh shows new commits) and
serves index.html next to this file. Binds to 127.0.0.1 only. Standard library only.
"""

import argparse
import json
import re
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
RS, US = "\x1e", "\x1f"
BRACE_RENAME = re.compile(r"\{([^{}]*) => ([^{}]*)\}")


def new_path(path: str) -> str:
    """Turn git's rename notation ('a/{x => y}/f' or 'old => new') into the new path."""
    if "=>" not in path:
        return path
    if "{" in path:
        return re.sub(r"/+", "/", BRACE_RENAME.sub(lambda m: m.group(2), path)).strip("/")
    return path.split(" => ", 1)[1]


def read_history(repo: Path) -> dict:
    out = subprocess.run(
        ["git", "-C", str(repo), "log", "--no-merges", "--numstat", "-z",
         f"--format={RS}%H{US}%at{US}%an{US}%s"],
        capture_output=True, check=True,
    ).stdout.decode("utf-8", errors="replace")
    commits = []
    for chunk in out.split(RS)[1:]:
        header, _, body = chunk.partition("\n")
        sha, ts, author, subject = header.split(US, 3)
        files = {}
        # With -z, each numstat entry is "add\tdel\tpath\0"; a rename is "add\tdel\t\0old\0new\0".
        parts = body.split("\0")
        i = 0
        while i < len(parts):
            entry = parts[i].strip("\n")
            i += 1
            if not entry:
                continue
            fields = entry.split("\t")
            if len(fields) < 3:
                continue
            added, deleted, path = fields[0], fields[1], fields[2]
            if path == "":  # rename: the next two parts are old and new path
                path = parts[i + 1] if i + 1 < len(parts) else ""
                i += 2
            path = new_path(path)
            top = path.split("/", 1)[0] if "/" in path else "(root files)"
            a = int(added) if added.isdigit() else 0  # "-" means a binary file
            d = int(deleted) if deleted.isdigit() else 0
            fa, fd = files.get(top, (0, 0))
            files[top] = (fa + a, fd + d)
        commits.append({"h": sha[:7], "t": int(ts), "a": author, "s": subject.strip("\0\n"),
                        "f": {k: list(v) for k, v in files.items()}})
    commits.sort(key=lambda c: c["t"])
    return {"repo": repo.name, "path": str(repo), "commits": commits}


def make_handler(repo: Path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = self.path.split("?", 1)[0]
            if route in ("/", "/index.html"):
                self.send(200, "text/html; charset=utf-8", (HERE / "index.html").read_bytes())
            elif route == "/api/data":
                try:
                    body = json.dumps(read_history(repo)).encode()
                    self.send(200, "application/json", body)
                except subprocess.CalledProcessError as e:
                    self.send(500, "text/plain", e.stderr or b"git failed")
            else:
                self.send(404, "text/plain", b"not found")

        def send(self, code, ctype, body):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("repo", nargs="?", default=".", help="path to a git repository (default: .)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-browser", action="store_true")
    args = p.parse_args()
    repo = Path(args.repo).resolve()
    if subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-dir"],
                      capture_output=True).returncode != 0:
        sys.exit(f"Not a git repository: {repo}")
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(repo))
    except OSError:  # port taken, or reserved by Windows: let the system pick a free one
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(repo))
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"Git pace for {repo}\n  {url}   (Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
