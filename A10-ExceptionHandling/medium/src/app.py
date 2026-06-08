#!/usr/bin/env python3
"""
A10-ExceptionHandling - Medium
漏洞：异常处理导致的状态不一致（失败开放 - Fail Open）
"""

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
DATABASE = os.environ.get('DATABASE_PATH', './data.db')
FLAG_PATH = '/flag'

# 读取flag
if os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, 'r') as f:
        REAL_FLAG = f.read().strip()
else:
    REAL_FLAG = "flag{TEST_Dynamic_FLAG}"

# ========== 数据库操作 ==========

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('DROP TABLE IF EXISTS users')
    db.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            password TEXT NOT NULL DEFAULT 'password123'
        )
    ''')
    db.execute("INSERT INTO users (username, role, password) VALUES ('admin', 'admin', 'admin_pass_2025')")
    db.execute("INSERT INTO users (username, role, password) VALUES ('guest', 'user', 'guest_pass')")
    db.execute("INSERT INTO users (username, role, password) VALUES ('user1', 'user', 'user1_pass')")
    db.commit()

# ========== 核心漏洞：失败开放的认证检查 ==========

def check_admin(user_id):
    """
    检查用户是否为管理员。
    漏洞：当数据库查询或数据处理发生任何异常时，
    异常处理器捕获后返回True（失败开放），允许访问。
    """
    try:
        db = get_db()
        # 如果user_id不是整数，这里会触发类型相关的SQL异常
        # 如果user_id是特殊字符串如 "' OR '1'='1"，查询会异常
        # 如果数据库连接断开，也会异常
        query = f"SELECT role FROM users WHERE id = {user_id}"
        cursor = db.execute(query)
        row = cursor.fetchone()
        if row is None:
            return False
        return row['role'] == 'admin'
    except Exception as e:
        # ❌ 设计缺陷：任何异常都被视为"认证通过"
        # 开发者认为"如果查不到就放行"比"阻塞用户"更好
        app.logger.warning(f"Admin check failed with exception: {e}")
        return True

# ========== 路由 ==========

@app.route('/')
def index():
    return """
    <h1>用户管理系统</h1>
    <p>欢迎访问安全用户管理系统。</p>
    <ul>
        <li><a href="/login?user_id=1">以管理员登录 (ID=1)</a></li>
        <li><a href="/login?user_id=2">以访客登录 (ID=2)</a></li>
        <li><a href="/admin/flag">查看Flag（仅管理员）</a></li>
        <li><a href="/api/user?id=1">API: 查询用户信息</a></li>
    </ul>
    <p>提示：系统的认证检查模块正在升级中，遇到异常时会自动放行以避免用户体验受损。</p>
    """

@app.route('/login')
def login():
    user_id = request.args.get('user_id', '2')
    session['user_id'] = user_id
    return f"<p>已登录，用户ID: {user_id}</p><p><a href='/admin/flag'>访问管理区域</a></p>"

@app.route('/admin/flag')
def admin_flag():
    user_id = session.get('user_id')
    if not user_id:
        return "请先登录", 403
    
    # 调用有漏洞的认证检查
    is_admin = check_admin(user_id)
    
    if is_admin:
        return f"<h1>Admin Control Panel</h1><p>Welcome, admin!</p><p>FLAG: {REAL_FLAG}</p>"
    else:
        return "<p>权限不足：需要管理员权限</p>", 403

@app.route('/api/user')
def api_user():
    """提供一个额外的查询接口，帮助参赛者理解user_id的用法"""
    user_id = request.args.get('id', '')
    try:
        db = get_db()
        # 同样存在SQL注入，但这不是本题主要考点
        query = f"SELECT id, username, role FROM users WHERE id = {user_id}"
        row = db.execute(query).fetchone()
        if row:
            return {"id": row['id'], "username": row['username'], "role": row['role']}
        else:
            return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

# ========== 启动 ==========

if __name__ == '__main__':
    os.makedirs('/app', exist_ok=True)
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=80, debug=False)
