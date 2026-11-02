"""Project Compass MVP: offline/local-first SQLite-backed project dashboard.
Run: python server.py   (Python 3.9+, no third-party packages)
"""
from __future__ import annotations

import json
import sqlite3
import threading
import webbrowser
from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4
import os
import sys

BASE = Path(__file__).resolve().parent
WEB = BASE / 'web'
DATA = BASE / 'data'
DATA.mkdir(exist_ok=True)
DB = DATA / 'projects.sqlite3'
HOST = '127.0.0.1'
PORT = int(os.environ.get('PROJECT_COMPASS_PORT', '8765'))
LOCK = threading.Lock()


def iso(dt):
    return dt.strftime('%Y-%m-%d')


def example_project(title, status, priority, progress, weeks, category, pinned=False):
    now = datetime.now(timezone.utc)
    return {
        'id': str(uuid4()), 'title': title, 'kind': 'project', 'status': status,
        'priority': priority, 'progress': progress, 'pinned': pinned,
        'category': category, 'tags': [], 'deadline': '', 'goals': '', 'notes': '',
        'folder': '', 'links': [], 'tasks': [],
        'history': [{'date': iso(now - timedelta(days=7 * (len(weeks) - 1 - i))), 'progress': v}
                    for i, v in enumerate(weeks)],
        'activity': [{'at': now.isoformat(), 'text': 'Example project. Edit or delete it to begin.'}],
        'createdAt': now.isoformat(), 'updatedAt': now.isoformat(), 'example': True,
    }


def sample_state():
    return {
        'schemaVersion': 1,
        'projects': [
            example_project('Example · Revit steel frame', 'active', 1, 64, [18, 30, 45, 55, 64], 'Engineering', True),
            example_project('Example · Django application', 'active', 2, 48, [10, 21, 25, 39, 48], 'Software', True),
            example_project('Example · English learning', 'active', 3, 32, [12, 16, 20, 22, 32], 'Personal', True),
            example_project('Example · Business idea', 'on_hold', 4, 25, [10, 18, 25, 25, 25], 'Business'),
        ],
        'settings': {'theme': 'light'},
        'demo': True,
    }


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY CHECK (id = 1), payload TEXT NOT NULL)')
        if not conn.execute('SELECT id FROM app_state WHERE id=1').fetchone():
            conn.execute('INSERT INTO app_state (id, payload) VALUES (1, ?)', (json.dumps(sample_state()),))


def read_state():
    with LOCK, sqlite3.connect(DB) as conn:
        row = conn.execute('SELECT payload FROM app_state WHERE id=1').fetchone()
    return json.loads(row[0])


def write_state(payload):
    with LOCK, sqlite3.connect(DB) as conn:
        conn.execute('UPDATE app_state SET payload=? WHERE id=1', (json.dumps(payload, ensure_ascii=False),))


def valid_state(state):
    if not isinstance(state, dict) or state.get('schemaVersion') != 1:
        return False
    projects = state.get('projects')
    if not isinstance(projects, list) or len(projects) > 3000:
        return False
    for p in projects:
        if not isinstance(p, dict) or not isinstance(p.get('id'), str) or not isinstance(p.get('title'), str):
            return False
        if len(p['title']) > 300:
            return False
    return isinstance(state.get('settings', {}), dict)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def log_message(self, fmt, *args):
        # Local server logging only.
        sys.stdout.write('%s - %s\n' % (self.address_string(), fmt % args))

    def api(self, code, data):
        encoded = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if urlparse(self.path).path == '/api/state':
            self.api(200, read_state())
        elif urlparse(self.path).path in ('/', '/index.html'):
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()

    def do_PUT(self):
        if urlparse(self.path).path != '/api/state':
            self.api(404, {'error': 'Not found'})
            return
        origin = self.headers.get('Origin', '')
        if origin and origin not in (f'http://{HOST}:{PORT}', f'http://localhost:{PORT}'):
            self.api(403, {'error': 'Origin not allowed'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 8 * 1024 * 1024:
                self.api(413, {'error': 'Invalid size (max 8 MB)'})
                return
            state = json.loads(self.rfile.read(size))
            if not valid_state(state):
                self.api(400, {'error': 'Invalid project data'})
                return
            write_state(state)
            self.api(200, {'ok': True})
        except (ValueError, UnicodeError, json.JSONDecodeError) as e:
            self.api(400, {'error': str(e)})


def main():
    init_db()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Project Compass running at http://{HOST}:{PORT}')
    print(f'Database: {DB}')
    print('Close this window to stop the server. Your data stays in data/projects.sqlite3.')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
    finally:
        httpd.server_close()


if __name__ == '__main__':
    main()
