#!/usr/bin/env python3
"""
A10-ExceptionHandling - Easy
漏洞：错误信息泄露（详细堆栈跟踪泄露敏感信息）
"""

import os
from flask import Flask, request, session, redirect, url_for, render_template_string
from itsdangerous import URLSafeTimedSerializer, BadSignature

app = Flask(__name__)

# 硬编码的敏感配置（将在异常堆栈中泄露）
app.config['SECRET_KEY'] = 'flask_easy_2025_super_secret_key_0xdeadbeef'
DATABASE_URI = 'sqlite:///app.db?flag_path=/flag'
FLAG_PATH = '/flag'

# 简单用户数据库
users = {
    'guest': {'role': 'user'},
    'admin': {'role': 'admin'}
}

# 读取flag
if os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, 'r') as f:
        REAL_FLAG = f.read().strip()
else:
    REAL_FLAG = "flag{TEST_Dynamic_FLAG}"

# 注册自定义错误处理 —— 设计缺陷：返回完整堆栈跟踪
def handle_exception(e):
    import traceback
    tb = traceback.format_exc()
    # 错误页面返回完整的堆栈跟踪
    error_html = f"""
    <h1>500 Internal Server Error</h1>
    <p>Something went wrong. Here are the details:</p>
    <pre style="background:#f4f4f4;padding:10px;border:1px solid #ccc;overflow:auto;">{tb}</pre>
    """
    return error_html, 500

for code in [400, 401, 403, 404, 500]:
    app.register_error_handler(code, handle_exception)

# 捕获所有未处理异常
@app.errorhandler(Exception)
def all_exceptions(e):
    return handle_exception(e)

@app.route('/')
def index():
    return """
    <h1>文件阅读器</h1>
    <p>这是一个安全的文件阅读服务（开发中）。</p>
    <ul>
        <li><a href="/read?file=welcome.txt">阅读欢迎文件</a></li>
        <li><a href="/read?file=about.txt">关于我们</a></li>
        <li><a href="/login?name=guest">以访客身份登录</a></li>
        <li><a href="/admin/flag">管理员区域</a></li>
    </ul>
    """

@app.route('/read')
def read_file():
    filename = request.args.get('file', '')
    # 开发调试遗留：使用了SECRET_KEY进行无意义的文件校验
    check_value = app.config['SECRET_KEY'][:16]
    try:
        # 故意不检查文件是否存在，直接打开，触发FileNotFoundError
        with open(filename, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        # ❌ 设计缺陷：为了方便调试，将敏感配置附加到异常消息中重新抛出
        # 在生产环境中这将导致敏感信息泄露
        raise RuntimeError(
            f"Failed to read file '{filename}'. "
            f"Debug info: SECRET_KEY={app.config['SECRET_KEY']}, "
            f"DB_URI={DATABASE_URI}, FLAG_PATH={FLAG_PATH}"
        ) from e

@app.route('/login')
def login():
    name = request.args.get('name', 'guest')
    # 使用URLSafeTimedSerializer作为session token（依赖于SECRET_KEY）
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = s.dumps({'user': name, 'role': users.get(name, {}).get('role', 'user')})
    session['token'] = token
    return f"""
    <p>已登录为: {name}</p>
    <p>Token: <code>{token}</code></p>
    <p><a href="/admin/flag">访问管理区域</a></p>
    """

@app.route('/admin/flag')
def admin_flag():
    token = session.get('token', '')
    if not token:
        return "请先登录", 403
    
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token, max_age=3600)
    except BadSignature:
        return "无效token", 403
    
    # 异常处理中的另一个缺陷：如果data格式异常，会触发500并泄露堆栈
    if data['role'] == 'admin':
        return f"<h1>Admin Panel</h1><p>FLAG: {REAL_FLAG}</p>"
    else:
        return f"<p>权限不足。你的角色是: {data.get('role', 'unknown')}</p>"

if __name__ == '__main__':
    # 创建一些测试文件
    os.makedirs('files', exist_ok=True)
    with open('files/welcome.txt', 'w') as f:
        f.write("欢迎使用文件阅读器！")
    with open('files/about.txt', 'w') as f:
        f.write("这是一个用于演示错误处理的简单应用。")
    
    app.run(host='0.0.0.0', port=80, debug=False)
