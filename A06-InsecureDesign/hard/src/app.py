import os
import sqlite3
from flask import Flask, request, jsonify, render_template, g

app = Flask(__name__)
DATABASE = '/app/data.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT
        )
    ''')
    db.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'player')")
    db.execute("INSERT OR IGNORE INTO users (id, username) VALUES (999, 'admin')")
    db.execute("INSERT OR IGNORE INTO notes (id, user_id, title, content) VALUES (1, 1, '我的笔记', '这是一篇普通笔记')")
    db.execute("INSERT OR IGNORE INTO notes (id, user_id, title, content) VALUES (2, 1, '待办事项', '记得买牛奶')")
    db.execute("INSERT OR IGNORE INTO notes (id, user_id, title, content) VALUES (999, 999, '管理员机密', 'flag_placeholder')")
    db.commit()
    db.close()


def get_flag():
    if os.path.exists('/flag'):
        with open('/flag', 'r') as f:
            return f.read().strip()
    return "flag{TEST_Dynamic_FLAG}"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_current_user_id():
    return 1


@app.route('/')
def index():
    return render_template('index.html')


# 单条查询 - 有完整权限校验
@app.route('/api/note/<int:note_id>', methods=['GET'])
def get_note(note_id):
    user_id = get_current_user_id()
    db = get_db()
    note = db.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user_id)
    ).fetchone()
    if not note:
        return jsonify({'success': False, 'message': '笔记不存在或无权限'}), 403
    content = note['content']
    if note['id'] == 999:
        content = get_flag()
    return jsonify({
        'success': True,
        'id': note['id'],
        'title': note['title'],
        'content': content
    })


# 批量查询 - 设计缺陷：只校验了ids列表的第一个
@app.route('/api/notes/batch', methods=['POST'])
def batch_get_notes():
    data = request.get_json() or {}
    ids = data.get('ids', [])

    if not ids or not isinstance(ids, list):
        return jsonify({'success': False, 'message': '请提供ids列表'}), 400

    try:
        ids = [int(i) for i in ids]
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'ids必须为整数列表'}), 400

    user_id = get_current_user_id()
    db = get_db()

    # 不安全的设计：只校验第一个id是否属于当前用户
    first_note = db.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?",
        (ids[0], user_id)
    ).fetchone()
    if not first_note:
        return jsonify({'success': False, 'message': '无权访问'}), 403

    # 查询所有ids的笔记，不再校验权限
    placeholders = ','.join('?' * len(ids))
    notes = db.execute(
        f"SELECT * FROM notes WHERE id IN ({placeholders})",
        ids
    ).fetchall()

    result = []
    for n in notes:
        content = n['content']
        if n['id'] == 999:
            content = get_flag()
        result.append({'id': n['id'], 'title': n['title'], 'content': content})

    return jsonify({
        'success': True,
        'notes': result
    })


@app.route('/api/my-notes', methods=['GET'])
def get_my_notes():
    user_id = get_current_user_id()
    db = get_db()
    notes = db.execute(
        "SELECT id, title FROM notes WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    return jsonify({
        'success': True,
        'notes': [{'id': n['id'], 'title': n['title']} for n in notes]
    })


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=80)
