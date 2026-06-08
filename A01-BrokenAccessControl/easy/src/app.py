from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/app/data.db"
FLAG = open("/flag", "r").read().strip() if os.path.exists("/flag") else "flag{TEST_Dynamic_FLAG}"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            owner TEXT
        )
    """)
    # Insert sample data
    docs = [
        (1, "我的日记", "今天天气不错，去公园散步了。", "alice"),
        (2, "项目笔记", "Flask项目进度汇报...", "alice"),
        (3, "购物清单", "牛奶、鸡蛋、面包、咖啡", "alice"),
        (4, "工作文档", "Q3季度销售报告", "bob"),
        (5, "会议纪要", "周一团队会议记录", "bob"),
        (6, "旅行计划", "国庆节去云南旅游攻略", "bob"),
        (0, "系统管理文档", f"恭喜你发现了隐藏的flag！{FLAG}", "admin"),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO documents (id, title, content, owner) VALUES (?, ?, ?, ?)",
        docs,
    )
    conn.commit()
    conn.close()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>个人文档中心</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .doc-list { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        .doc-item { padding: 10px; margin: 5px 0; background: white; border-radius: 4px; }
        .doc-content { margin-top: 20px; padding: 20px; background: #e8f4e8; border-radius: 8px; }
        .hint { color: #666; font-size: 0.9em; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>📄 个人文档中心</h1>
    <p>欢迎，alice！以下是您的文档列表（ID: 1-3）：</p>
    <div class="doc-list">
        <div class="doc-item">📄 文档 #1 - 我的日记</div>
        <div class="doc-item">📄 文档 #2 - 项目笔记</div>
        <div class="doc-item">📄 文档 #3 - 购物清单</div>
    </div>
    <div class="hint">
        <p>提示：点击文档查看详情。URL格式：<code>/doc?id=1</code></p>
    </div>
    {% if doc %}
    <div class="doc-content">
        <h2>{{ doc[1] }}</h2>
        <p><strong>文档ID:</strong> {{ doc[0] }}</p>
        <p><strong>作者:</strong> {{ doc[3] }}</p>
        <hr>
        <p>{{ doc[2] }}</p>
    </div>
    {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, doc=None)


@app.route("/doc")
def view_doc():
    doc_id = request.args.get("id", "1")
    try:
        doc_id = int(doc_id)
    except ValueError:
        return "无效的文档ID", 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, content, owner FROM documents WHERE id = ?", (doc_id,))
    doc = c.fetchone()
    conn.close()

    if doc:
        return render_template_string(HTML_TEMPLATE, doc=doc)
    else:
        return "文档不存在", 404


if __name__ == "__main__":
    os.makedirs("/app", exist_ok=True)
    init_db()
    app.run(host="0.0.0.0", port=80)
