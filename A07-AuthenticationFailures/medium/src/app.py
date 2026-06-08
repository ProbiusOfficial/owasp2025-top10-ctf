import os
import sqlite3
import jwt
import datetime
from flask import Flask, request, jsonify, g

app = Flask(__name__)

# Weak secret key - a common English word
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

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
                        password TEXT NOT NULL,
                        role TEXT DEFAULT 'user'
                    )''')
        db.commit()
        # Insert admin
        try:
            db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin_password_not_guessable', 'admin'))
            db.commit()
        except sqlite3.IntegrityError:
            pass


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


@app.route('/')
def index():
    return '''
    <h1>JWT Auth System</h1>
    <p>Endpoints:</p>
    <ul>
        <li>POST /register - username, password</li>
        <li>POST /login - username, password</li>
        <li>GET /profile - Header: Authorization: Bearer &lt;token&gt;</li>
        <li>GET /admin/flag - Header: Authorization: Bearer &lt;token&gt; (admin only)</li>
    </ul>
    '''


@app.route('/register', methods=['POST'])
def register():
    data = request.form if request.form else request.get_json(force=True)
    username = data.get('username', '')
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return jsonify({'message': 'registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'username already exists'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.form if request.form else request.get_json(force=True)
    username = data.get('username', '')
    password = data.get('password', '')
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None or user['password'] != password:
        return jsonify({'error': 'invalid username or password'}), 401
    token = generate_token(user['username'], user['role'])
    return jsonify({'token': token})


@app.route('/profile', methods=['GET'])
def profile():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'missing token'}), 401
    token = auth_header.split(' ')[1]
    try:
        payload = decode_token(token)
        return jsonify({'username': payload['username'], 'role': payload['role']})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'invalid token'}), 401


@app.route('/admin/flag', methods=['GET'])
def admin_flag():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'missing token'}), 401
    token = auth_header.split(' ')[1]
    try:
        payload = decode_token(token)
        if payload.get('role') != 'admin':
            return jsonify({'error': 'admin only'}), 403
        flag = "flag{TEST_Dynamic_FLAG}"
        if os.path.exists('/flag'):
            with open('/flag', 'r') as f:
                flag = f.read().strip()
        return jsonify({'flag': flag})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'invalid token'}), 401


if __name__ == '__main__':
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
