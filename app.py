# app.py — Flask backend that serves Mini App and provides simple API
# Run: python app.py
from flask import Flask, request, jsonify, send_from_directory
import os, sqlite3, json, datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

DB_PATH = os.environ.get('DB_PATH', 'database.db')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', '')  # numeric chat id for admin to receive "Open app" button

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id TEXT,
        date TEXT,
        name TEXT,
        muscle TEXT,
        total REAL
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/init', methods=['POST'])
def api_init():
    body = request.get_json(silent=True) or {}
    initData = body.get('initData') or {}
    tg_id = None
    if isinstance(initData, dict) and initData.get('user'):
        tg_id = str(initData['user'].get('id'))
    if not tg_id:
        tg_id = 'anon'
    conn = get_db()
    cur = conn.execute('SELECT date,name,total FROM workouts WHERE tg_id = ? ORDER BY id DESC LIMIT 10', (tg_id,))
    rows = cur.fetchall()
    history = [{'date':r['date'], 'name':r['name'], 'total':r['total']} for r in rows]
    conn.close()
    return jsonify({'message':'Приложение готово', 'history': history})

@app.route('/api/log', methods=['POST'])
def api_log():
    body = request.get_json(silent=True) or {}
    muscle = body.get('muscle_group', '—')
    name = body.get('name', 'Без названия')
    sets = body.get('sets', [])
    initData = body.get('initData') or {}
    tg_id = None
    if isinstance(initData, dict) and initData.get('user'):
        tg_id = str(initData['user'].get('id'))
    if not tg_id:
        tg_id = 'anon'
    total = 0.0
    for s in sets:
        try:
            reps = float(s.get('reps', 0))
            weight = float(s.get('weight', 0))
        except:
            reps = 0
            weight = 0
        total += reps * weight
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = get_db()
    conn.execute('INSERT INTO workouts (tg_id,date,name,muscle,total) VALUES (?,?,?,?,?)', (tg_id, date, name, muscle, total))
    conn.commit()
    cur = conn.execute('SELECT date,name,total FROM workouts WHERE tg_id = ? ORDER BY id DESC LIMIT 10', (tg_id,))
    rows = cur.fetchall()
    history = [{'date':r['date'], 'name':r['name'], 'total':r['total']} for r in rows]
    conn.close()
    return jsonify({'exercise_total': total, 'history': history})

# Endpoint to send a message with Web App button to ADMIN_CHAT_ID (call once from browser)
@app.route('/send_button')
def send_button():
    if not BOT_TOKEN:
        return 'BOT_TOKEN not set in env', 400
    if not ADMIN_CHAT_ID:
        return 'ADMIN_CHAT_ID not set in env', 400
    import requests
    base = f'https://api.telegram.org/bot{BOT_TOKEN}'
    # Replace with your public URL where this app is hosted
    public_url = os.environ.get('PUBLIC_URL', '')
    if not public_url:
        return 'Set PUBLIC_URL env to your app URL (e.g. https://your-app.onrender.com)', 400
    keyboard = {
      "inline_keyboard": [[
        {"text":"Открыть MyGymProgress","web_app":{"url": public_url}}
      ]]
    }
    params = {
      'chat_id': ADMIN_CHAT_ID,
      'text': 'Открыть приложение MyGymProgress',
      'reply_markup': json.dumps(keyboard)
    }
    r = requests.get(base + '/sendMessage', params=params)
    return ('OK' if r.ok else ('ERR: ' + r.text)), (200 if r.ok else 500)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
