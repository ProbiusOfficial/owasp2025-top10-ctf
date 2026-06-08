import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_PATH = "/app/data.db"


def init_db():
    os.makedirs("/app", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        role TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS secret (
        id INTEGER PRIMARY KEY,
        flag TEXT
    )''')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin@ctf.local', 'admin')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'guest', 'guest@ctf.local', 'user')")
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'alice', 'alice@ctf.local', 'user')")
    # flag will be inserted by entrypoint, fallback here for local dev
    flag = open("/flag", "r").read().strip() if os.path.exists("/flag") else "flag{TEST_Dynamic_FLAG}"
    c.execute("DELETE FROM secret")
    c.execute("INSERT INTO secret (flag) VALUES (?)", (flag,))
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>用户查询系统</title></head>
<body>
    <h1>用户查询系统</h1>
    <p>通过用户ID查询信息</p>
    <form action="/search" method="get">
        <input type="text" name="id" placeholder="输入用户ID">
        <button type="submit">查询</button>
    </form>
    <hr>
    <p>示例：<code>?id=1</code></p>
</body>
</html>
''')


@app.route("/search")
def search():
    user_id = request.args.get("id", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 故意使用字符串拼接，存在SQL注入漏洞
    sql = f"SELECT * FROM users WHERE id = '{user_id}'"
    try:
        c.execute(sql)
        rows = c.fetchall()
    except Exception as e:
        conn.close()
        return f"<h2>查询错误</h2><pre>{str(e)}</pre><br><a href='/'>返回</a>"
    conn.close()

    html = "<h1>查询结果</h1><table border='1'>"
    html += "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table><br><a href='/'>返回</a>"
    html += f"<hr><p>执行的SQL:</p><pre>{sql}</pre>"
    return html


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=80)
