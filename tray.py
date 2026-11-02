"""Project Compass system-tray launcher.
Run: pythonw tray.py   (needs: pip install -r requirements.txt)
Runs the server from server.py in a background thread and keeps a tray icon
with "Open Project Compass" (left-click) and "Quit".
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent

# pythonw has no console: sys.stdout/stderr are None, and server.Handler.log_message
# writes to sys.stdout, so give them somewhere to go before anything else runs.
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    (BASE / 'data').mkdir(exist_ok=True)
    sys.stderr = open(BASE / 'data' / 'tray.log', 'a', encoding='utf-8')

import pystray
from PIL import Image, ImageDraw, ImageFont

import server

URL = f'http://{server.HOST}:{server.PORT}'


class TrayHTTPServer(server.ThreadingHTTPServer):
    # Without this, Windows lets a second server bind the same port silently.
    allow_reuse_address = False


def port_in_use():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((server.HOST, server.PORT)) == 0


def open_app(*_):
    # Same browser detection order as start_windows.bat.
    pf = os.environ.get('ProgramFiles', r'C:\Program Files')
    pf86 = os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')
    for exe in (Path(pf) / 'Google/Chrome/Application/chrome.exe',
                Path(pf86) / 'Microsoft/Edge/Application/msedge.exe',
                Path(pf) / 'Microsoft/Edge/Application/msedge.exe'):
        if exe.exists():
            subprocess.Popen([str(exe), f'--app={URL}'])
            return
    webbrowser.open(URL)


def make_icon():
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=14, fill='#6256e9')
    try:
        font = ImageFont.truetype('segoeuib.ttf', 30)
    except OSError:
        font = ImageFont.load_default()
    draw.text((size / 2, size / 2), 'PC', fill='white', font=font, anchor='mm')
    return img


def main():
    if port_in_use():
        # Already running (another tray or server.py): just show the app.
        open_app()
        return
    server.init_db()
    try:
        httpd = TrayHTTPServer((server.HOST, server.PORT), server.Handler)
    except OSError:
        open_app()
        return
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    def quit_app(icon, _item):
        icon.stop()
        httpd.shutdown()
        httpd.server_close()

    icon = pystray.Icon('project_compass', make_icon(), 'Project Compass', menu=pystray.Menu(
        pystray.MenuItem('Open Project Compass', open_app, default=True),
        pystray.MenuItem('Quit', quit_app),
    ))
    open_app()
    icon.run()


if __name__ == '__main__':
    main()
