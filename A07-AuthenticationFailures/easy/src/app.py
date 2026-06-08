import os
import sqlite3
import hashlib
from flask import Flask, request, session, redirect, render_template_string, g

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
                        password TEXT NOT NULL
                    )''')
        db.commit()

        # Insert admin user with weak password
        weak_passwords = ['password123', 'admin123', '12345678', 'qwerty123']
        import random
        chosen_password = random.choice(weak_passwords)
        hashed = hashlib.sha256(chosen_password.encode()).hexdigest()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ('admin', hashed))
            db.commit()
        except sqlite3.IntegrityError:
            pass


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Login - A07 Easy</title></head>
<body>
<h2>Login</h2>
<form method="POST" action="/login">
    <label>Username: <input type="text" name="username" required></label><br><br>
    <label>Password: <input type="password" name="password" required></label><br><br>
    <button type="submit">Login</button>
</form>
{% if msg %}
    <p style="color:red;">{{ msg }}</p>
{% endif %}
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Admin Panel</title></head>
<body>
<h2>Welcome, Admin!</h2>
<p>Flag: {{ flag }}</p>
<a href="/logout">Logout</a>
</body>
</html>
'''


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            msg = "用户不存在"
        else:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if hashed == user['password']:
                session['username'] = username
                return redirect('/admin')
            else:
                msg = "密码错误"
    return render_template_string(LOGIN_TEMPLATE, msg=msg)


@app.route('/admin')
def admin():
    if 'username' not in session or session['username'] != 'admin':
        return redirect('/login')
    flag = "flag{TEST_Dynamic_FLAG}"
    if os.path.exists('/flag'):
        with open('/flag', 'r') as f:
            flag = f.read().strip()
    return render_template_string(ADMIN_TEMPLATE, flag=flag)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
