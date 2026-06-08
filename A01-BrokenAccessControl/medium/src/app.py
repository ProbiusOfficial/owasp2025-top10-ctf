from flask import Flask, request, jsonify, render_template_string
import sqlite3
import jwt
import datetime
import os

app = Flask(__name__)

DB_PATH = "/app/data.db"
JWT_SECRET = "weak_secret_key_123"
FLAG = open("/flag", "r").read().strip() if os.path.exists("/flag") else "flag{TEST_Dynamic_FLAG}"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    users = [
        (1, "alice", "alice123", "user"),
        (2, "admin", "admin888", "admin"),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
        users,
    )
    conn.commit()
    conn.close()


INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>安全文档管理平台</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .login-box { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px; }
        input { padding: 10px; margin: 5px; width: 200px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .panel { margin-top: 20px; padding: 20px; background: #e8f4e8; border-radius: 8px; display: none; }
        .admin-link { color: red; font-weight: bold; }
        .hidden { display: none; }
        .user-info { background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🔒 安全文档管理平台</h1>
    <div id="login-section">
        <div class="login-box">
            <h3>用户登录</h3>
            <input type="text" id="username" placeholder="用户名" value="alice"><br>
            <input type="password" id="password" placeholder="密码" value="alice123"><br>
            <button onclick="login()">登录</button>
            <p style="color:#666;font-size:0.85em;">测试账号: alice / alice123</p>
        </div>
    </div>
    <div id="main-section" style="display:none;">
        <div class="user-info">
            <p>欢迎，<span id="uname"></span>！</p>
            <p>您的角色: <span id="role"></span></p>
        </div>
        <h3>普通用户功能区</h3>
        <ul>
            <li>📄 查看个人文档</li>
            <li>✏️ 编辑个人资料</li>
        </ul>
        <div id="admin-panel-link" style="display:none;">
            <p class="admin-link">👑 管理员面板（仅管理员可见）</p>
            <p>点击访问: <a href="#" onclick="goAdmin()">/api/admin/flag</a></p>
        </div>
        <div id="admin-result" class="panel"></div>
    </div>
    <script>
        let token = localStorage.getItem('token');
        if (token) showMain(token);

        function login() {
            fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                })
            }).then(r => r.json()).then(data => {
                if (data.token) {
                    localStorage.setItem('token', data.token);
                    showMain(data.token);
                } else {
                    alert(data.error || '登录失败');
                }
            });
        }

        function showMain(token) {
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('main-section').style.display = 'block';
            try {
                let payload = JSON.parse(atob(token.split('.')[1]));
                document.getElementById('uname').textContent = payload.username;
                document.getElementById('role').textContent = payload.role;
                // 前端根据 role 决定是否显示管理员链接
                if (payload.role === 'admin') {
                    document.getElementById('admin-panel-link').style.display = 'block';
                }
            } catch(e) {}
        }

        function goAdmin() {
            let token = localStorage.getItem('token');
            fetch('/api/admin/flag', {
                headers: {'Authorization': 'Bearer ' + token}
            }).then(r => r.json()).then(data => {
                let div = document.getElementById('admin-result');
                div.style.display = 'block';
                div.innerHTML = '<h3>管理员接口返回:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
            });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    user = c.fetchone()
    conn.close()

    if user:
        payload = {
            "username": user[0],
            "role": user[1],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"error": "用户名或密码错误"}), 401


@app.route("/api/admin/flag")
def admin_flag():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "未提供Token"}), 401

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "无效的Token"}), 401

    # BUG: 后端只验证了JWT是否有效，没有验证 role 是否为 admin
    return jsonify({
        "message": "管理员接口调用成功",
        "flag": FLAG,
        "user": payload["username"],
        "role": payload["role"],
    })


if __name__ == "__main__":
    os.makedirs("/app", exist_ok=True)
    init_db()
    app.run(host="0.0.0.0", port=80)
