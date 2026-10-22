"""Launch the Night Hunter desktop dashboard from the Windows executable."""

from __future__ import annotations

import os
import threading
import webbrowser

from waitress import serve

from api.server import app


HOST = "127.0.0.1"
PORT = int(os.environ.get("NIGHT_HUNTER_PORT", "5000"))
LOCAL_APP_URL = f"http://{HOST}:{PORT}"


def open_dashboard() -> None:
    """Always open the installed local engine, never the cloud dashboard.

    Nmap must execute on the user's computer to inspect their LAN and use
    the locally installed Nmap binary. The public site is an update/download
    channel and must not replace this local scanner.
    """
    print(f"[+] Opening local dashboard: {LOCAL_APP_URL}")
    webbrowser.open_new(LOCAL_APP_URL)


if __name__ == "__main__":
    threading.Timer(1.0, open_dashboard).start()
    serve(app, host=HOST, port=PORT)
