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
            username TEXT UNIQUE,
            balance INTEGER DEFAULT 100
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            status TEXT
        )
    ''')
    db.execute("INSERT OR IGNORE INTO users (id, username, balance) VALUES (1, 'player', 100)")
    db.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (1, 'Flag', 10000)")
    db.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (2, '普通道具', 10)")
    db.commit()
    db.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/user', methods=['GET'])
def get_user():
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = 1").fetchone()
    return jsonify({'id': user['id'], 'username': user['username'], 'balance': user['balance']})


@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return jsonify([{'id': p['id'], 'name': p['name'], 'price': p['price']} for p in products])


@app.route('/api/recharge', methods=['POST'])
def recharge():
    data = request.get_json() or {}
    amount = data.get('amount', 0)
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': '金额格式错误'}), 400

    if amount <= 0:
        return jsonify({'success': False, 'message': '充值金额必须大于0'}), 400

    # 不安全的设计：直接根据前端传来的amount增加余额，没有任何支付验证
    db = get_db()
    db.execute("UPDATE users SET balance = balance + ? WHERE id = 1", (amount,))
    db.commit()
    return jsonify({'success': True, 'message': f'充值成功，增加{amount}金币'})


@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({'success': False, 'message': '缺少商品ID'}), 400

    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': '商品ID格式错误'}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = 1").fetchone()
    product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

    if not product:
        return jsonify({'success': False, 'message': '商品不存在'}), 404

    if user['balance'] < product['price']:
        return jsonify({'success': False, 'message': '余额不足'}), 400

    db.execute("UPDATE users SET balance = balance - ? WHERE id = 1", (product['price'],))
    db.execute("INSERT INTO orders (user_id, product_id, status) VALUES (?, ?, 'success')", (1, product_id))
    db.commit()

    if product['name'] == 'Flag':
        with open('/flag', 'r') as f:
            flag = f.read().strip()
        return jsonify({'success': True, 'message': '购买成功！', 'flag': flag})

    return jsonify({'success': True, 'message': '购买成功！'})


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=80)
