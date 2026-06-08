import os
import random
import time
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# 服务器启动时间戳
START_TIME = int(time.time())
# 管理员在服务器启动时登录（取最近的整点时间戳）
ADMIN_LOGIN_TIME = START_TIME - (START_TIME % 3600)
random.seed(ADMIN_LOGIN_TIME)
ADMIN_TOKEN = ''.join([str(random.randint(0, 9)) for _ in range(10)])

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Secure Login System</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        input { padding: 8px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .hint { background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .code { background: #f4f4f4; padding: 10px; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Secure Login System</h1>
        <p>Welcome to our secure system. Please login to get your session token.</p>

        <div class="hint">
            <strong>Hint:</strong> The admin logged in at Unix timestamp <strong>{{ admin_time }}</strong> (on the hour).
        </div>

        <form action="/login" method="post">
            <label>Username:</label>
            <input type="text" name="username" placeholder="Enter username">
            <label>Password:</label>
            <input type="password" name="password" placeholder="Enter password">
            <button type="submit">Login</button>
        </form>

        <hr>
        <p><a href="/admin/flag">🏁 Get Flag (Admin Only)</a></p>
    </div>

    <!--
    ==========================================
    Developer Note: Token Generation Algorithm
    ==========================================
    import random
    import time

    random.seed(int(time.time()))
    token = ''.join([str(random.randint(0,9)) for _ in range(10)])

    The admin token was generated at server startup.
    ==========================================
    -->
</body>
</html>
'''

LOGIN_RESULT_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Login Result</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .token { background: #d4edda; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Welcome, {{ username }}!</h1>
        <p>Your session token has been generated:</p>
        <div class="token">{{ token }}</div>
        <p>Token generated at timestamp: <strong>{{ gen_time }}</strong></p>
        <p><a href="/">← Back to Home</a></p>
    </div>
</body>
</html>
'''

FLAG_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .flag { background: #d4edda; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 1.2em; color: #155724; }
        .error { background: #f8d7da; padding: 15px; border-radius: 4px; color: #721c24; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Admin Panel</h1>
        {% if flag %}
            <div class="flag">{{ flag }}</div>
        {% else %}
            <div class="error">Access denied. Valid admin token required.</div>
            <p>Please provide your token via <code>?token=YOUR_TOKEN</code></p>
        {% endif %}
        <p><a href="/">← Back to Home</a></p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, admin_time=ADMIN_LOGIN_TIME)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return "Username and password required.", 400

    if username.lower() == 'admin':
        return "Admin account cannot be logged in directly.", 403

    # 生成基于当前时间戳的token
    current_time = int(time.time())
    random.seed(current_time)
    token = ''.join([str(random.randint(0, 9)) for _ in range(10)])

    return render_template_string(LOGIN_RESULT_HTML,
                                  username=username,
                                  token=token,
                                  gen_time=current_time)

@app.route('/admin/flag')
def admin_flag():
    token = request.args.get('token', '').strip()
    if token == ADMIN_TOKEN:
        try:
            with open('/flag', 'r') as f:
                flag = f.read().strip()
        except:
            flag = "flag{TEST_Dynamic_FLAG}"
        return render_template_string(FLAG_HTML, flag=flag)
    return render_template_string(FLAG_HTML, flag=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
