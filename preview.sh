#!/usr/bin/env bash
# Serve the checked-in GitHub Pages site without a build step.
set -euo pipefail

SITE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "$SITE_DIR/index.html" ]]; then
  printf 'Error: index.html is missing beside preview.sh.\n' >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  printf 'Error: Python 3 is required (install python3).\n' >&2
  exit 1
fi

exec python3 - "$SITE_DIR" "$@" <<'PY'
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description="Preview the FlameWM website locally")
parser.add_argument("port", type=int, nargs="?", default=8080, help="Local port (default: 8080)")
parser.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically")
args = parser.parse_args(sys.argv[2:])
if not 0 <= args.port <= 65535:
    parser.error("port must be between 0 and 65535")

root = sys.argv[1]
try:
    server = ThreadingHTTPServer(("127.0.0.1", args.port),
                                 partial(SimpleHTTPRequestHandler, directory=root))
except OSError as error:
    parser.exit(1, f"Cannot start local website server: {error}\nTry another port: ./preview.sh 8081\n")

url = f"http://127.0.0.1:{server.server_address[1]}/"
print(f"FlameWM website preview: {url}", flush=True)
print("Press Ctrl+C to stop. Only accessible from this computer.", flush=True)

try:
    if not args.no_browser and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, url], stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
    server.serve_forever(poll_interval=0.2)
except KeyboardInterrupt:
    print("\nPreview stopped.")
finally:
    server.server_close()
PY
