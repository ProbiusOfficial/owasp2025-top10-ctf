from flask import Flask, request, render_template_string, redirect, url_for, make_response
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/app/comments.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sanitize_input(text):
    """有缺陷的过滤函数 - 简单字符串替换，可被绕过"""
    text = text.replace('<script>', '').replace('</script>', '')
    text = text.replace('javascript:', '')
    text = text.replace('onerror=', '')
    return text

HOME_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>留言板 - 星辰社区</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .form-box { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .comment { background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #3498db; }
        .comment-name { font-weight: bold; color: #2c3e50; }
        .comment-time { color: #999; font-size: 12px; }
        input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background: #3498db; color: white; padding: 10px 30px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .nav { margin-bottom: 20px; }
        .nav a { color: #3498db; text-decoration: none; margin-right: 15px; }
        .notice { background: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 4px; margin-bottom: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>星辰社区留言板</h1>
        <p>欢迎留下您的宝贵意见！</p>
    </div>
    <div class="nav">
        <a href="/">首页</a>
        <a href="/admin/view">管理员查看</a>
    </div>
    <div class="form-box">
        <div class="notice">
            <strong>安全提示：</strong>系统已启用XSS过滤，禁止 &lt;script&gt; 标签、javascript: 协议和 onerror 事件。
        </div>
        <form method="POST" action="/comment">
            <label>昵称：</label>
            <input type="text" name="name" placeholder="请输入昵称" required>
            <label>留言内容：</label>
            <textarea name="content" rows="4" placeholder="请输入留言内容" required></textarea>
            <button type="submit">发表留言</button>
        </form>
    </div>
    <h2>最新留言</h2>
    {% for comment in comments %}
    <div class="comment">
        <div class="comment-name">{{ comment.name }}</div>
        <div class="comment-time">{{ comment.created_at }}</div>
        <div class="comment-content">{{ comment.content|safe }}</div>
    </div>
    {% endfor %}
</body>
</html>
'''

ADMIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>管理员查看 - 星辰社区</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: #c0392b; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .comment { background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #c0392b; }
        .secret { background: #2c3e50; color: #2ecc71; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-family: monospace; }
        .nav { margin-bottom: 20px; }
        .nav a { color: #3498db; text-decoration: none; margin-right: 15px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>管理员控制台</h1>
        <p>本页面模拟管理员浏览所有留言（会执行JavaScript）</p>
    </div>
    <div class="nav">
        <a href="/">返回首页</a>
    </div>
    <div class="secret">
        <strong>[管理员密钥]</strong> 当前会话密钥: <span id="admin-key">{{ admin_key }}</span>
    </div>
    <h2>待审核留言</h2>
    {% for comment in comments %}
    <div class="comment">
        <strong>{{ comment.name }}</strong> <span style="color:#999">{{ comment.created_at }}</span>
        <div>{{ comment.content|safe }}</div>
    </div>
    {% endfor %}
</body>
</html>
'''

@app.route('/')
def index():
    conn = get_db()
    comments = conn.execute('SELECT * FROM comments ORDER BY created_at DESC LIMIT 10').fetchall()
    conn.close()
    return render_template_string(HOME_PAGE, comments=comments)

@app.route('/comment', methods=['POST'])
def post_comment():
    name = sanitize_input(request.form.get('name', ''))
    content = sanitize_input(request.form.get('content', ''))
    conn = get_db()
    conn.execute('INSERT INTO comments (name, content) VALUES (?, ?)', (name, content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/admin/view')
def admin_view():
    # 读取flag作为"管理员密钥"
    flag = "flag{TEST_Dynamic_FLAG}"
    if os.path.exists('/flag'):
        with open('/flag', 'r') as f:
            flag = f.read().strip()
    
    conn = get_db()
    comments = conn.execute('SELECT * FROM comments ORDER BY created_at DESC').fetchall()
    conn.close()
    
    resp = make_response(render_template_string(ADMIN_PAGE, comments=comments, admin_key=flag))
    # 安全配置错误：未设置 Content-Security-Policy 头
    # 同时为了方便XSS利用，不设置 HttpOnly（虽然这里flag不在cookie中）
    resp.set_cookie('admin_session', 'super_secret_admin_cookie_value_2025')
    return resp

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=80)
