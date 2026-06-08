import os
import sqlite3
import hashlib
import time
from flask import Flask, request, jsonify, g, render_template_string

app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = '/app/data.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT DEFAULT 'user'
                    )''')
        db.execute('''CREATE TABLE IF NOT EXISTS reset_tokens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        token TEXT NOT NULL,
                        created_at INTEGER NOT NULL,
                        used INTEGER DEFAULT 0
                    )''')
        db.commit()
        # Insert admin user
        try:
            db.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       ('admin', 'admin@ctf.local', 'SuperSecureAdminPass123!', 'admin'))
            db.commit()
        except sqlite3.IntegrityError:
            pass


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def generate_token(user_id):
    # Token based on user_id and current minute timestamp
    minute_ts = int(time.time() // 60) * 60
    raw = f"{user_id}:{minute_ts}"
    return hashlib.md5(raw.encode()).hexdigest(), minute_ts


def verify_admin_token(token):
    """Verify if token matches admin (user_id=1) in a reasonable time window."""
    current_minute_ts = int(time.time() // 60) * 60
    # Search within +/- 10 minutes window
    for offset in range(-600, 601, 60):
        ts = current_minute_ts + offset
        candidate = hashlib.md5(f"1:{ts}".encode()).hexdigest()
        if candidate == token:
            return True, 1
    return False, None


INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Password Reset System</title></head>
<body>
<h1>Password Reset System</h1>
<ul>
    <li>POST /register - username, email, password</li>
    <li>POST /login - username, password</li>
    <li>POST /forgot-password - email</li>
    <li>POST /reset-password - token, new_password</li>
    <li>GET /check-token?token=xxx - check if token is valid</li>
    <li>GET /debug/tokens - debug info (leak)</li>
</ul>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)


@app.route('/register', methods=['POST'])
def register():
    data = request.form if request.form else request.get_json(force=True)
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    if not username or not email or not password:
        return jsonify({'error': 'username, email and password required'}), 400
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
        db.commit()
        return jsonify({'message': 'registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'username or email already exists'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.form if request.form else request.get_json(force=True)
    username = data.get('username', '')
    password = data.get('password', '')
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None or user['password'] != password:
        return jsonify({'error': 'invalid username or password'}), 401
    flag = "flag{TEST_Dynamic_FLAG}"
    if user['role'] == 'admin' and os.path.exists('/flag'):
        with open('/flag', 'r') as f:
            flag = f.read().strip()
    return jsonify({'message': 'login successful', 'role': user['role'],
                    'flag': flag if user['role'] == 'admin' else None})


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.form if request.form else request.get_json(force=True)
    email = data.get('email', '')
    if not email:
        return jsonify({'error': 'email required'}), 400
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user is None:
        return jsonify({'error': 'email not found'}), 404
    token, minute_ts = generate_token(user['id'])
    db.execute("INSERT INTO reset_tokens (user_id, token, created_at) VALUES (?, ?, ?)",
               (user['id'], token, minute_ts))
    db.commit()
    return jsonify({
        'message': 'reset token generated',
        'token': token,
        'note': 'In production this would be sent via email. Here we show it for demo.'
    })


@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.form if request.form else request.get_json(force=True)
    token = data.get('token', '')
    new_password = data.get('new_password', '')
    if not token or not new_password:
        return jsonify({'error': 'token and new_password required'}), 400
    db = get_db()
    row = db.execute("SELECT * FROM reset_tokens WHERE token = ? AND used = 0", (token,)).fetchone()
    if row is None:
        # Also check real-time admin token prediction
        is_valid, user_id = verify_admin_token(token)
        if is_valid:
            db.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
            db.commit()
            return jsonify({'message': 'password reset successful'})
        return jsonify({'error': 'invalid or used token'}), 400
    db.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, row['user_id']))
    db.execute("UPDATE reset_tokens SET used = 1 WHERE id = ?", (row['id'],))
    db.commit()
    return jsonify({'message': 'password reset successful'})


@app.route('/check-token')
def check_token():
    token = request.args.get('token', '')
    db = get_db()
    row = db.execute("SELECT * FROM reset_tokens WHERE token = ? AND used = 0", (token,)).fetchone()
    if row:
        return jsonify({'valid': True, 'user_id': row['user_id']})
    # Also check real-time admin token prediction
    is_valid, user_id = verify_admin_token(token)
    if is_valid:
        return jsonify({'valid': True, 'user_id': user_id})
    return jsonify({'valid': False})


@app.route('/debug/tokens')
def debug_tokens():
    # Simulated information leak - debug endpoint
    db = get_db()
    tokens = db.execute("SELECT rt.token, rt.user_id, rt.created_at, u.username, u.email \
                         FROM reset_tokens rt JOIN users u ON rt.user_id = u.id \
                         ORDER BY rt.id DESC LIMIT 20").fetchall()
    result = []
    for t in tokens:
        result.append({
            'token': t['token'],
            'user_id': t['user_id'],
            'username': t['username'],
            'email': t['email'],
            'created_at': t['created_at']
        })
    return jsonify({'debug_info': 'recent reset tokens', 'tokens': result})


if __name__ == '__main__':
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
