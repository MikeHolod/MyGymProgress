# app.py — Flask backend for Telegram Mini App MyGymProgress

from flask import Flask, request, jsonify
import os, sqlite3, json, datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

DB_PATH = os.environ.get('DB_PATH', 'database.db')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', '')  # numeric chat id
PUBLIC_URL = os.environ.get('PUBLIC_URL', '')

# ---------- DB ----------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id TEXT,
            date TEXT,
            name TEXT,
            muscle TEXT,
            total REAL
        )
    """)
    conn.commit()
    conn.close()

# ---------- ROUTES ----------

@app.route('/')
def index():
    # ✅ ВАЖНО: всегда отдаём index.html из папки static
    return app.send_static_file('index.html')

@app.route('/api/init', methods=['POST'])
def api_init():
    body = request.get_json(silent=True) or {}
    initData = body.get('initData') or {}

    tg_id = 'anon'
    if isinstance(initData, dict) and initData.get('user'):
        tg_id = str(initData['user'].get('id', 'anon'))

    conn = get_db()
