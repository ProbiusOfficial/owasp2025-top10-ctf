import os
import sqlite3
import time
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
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            quantity INTEGER
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            order_no TEXT UNIQUE,
            status TEXT,
            product_id INTEGER
        )
    ''')
    db.execute("INSERT OR IGNORE INTO stock (id, product_name, quantity) VALUES (1, 'Flag', 1)")
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


@app.route('/api/stock', methods=['GET'])
def get_stock():
    db = get_db()
    stock = db.execute("SELECT * FROM stock WHERE id = 1").fetchone()
    return jsonify({'product': stock['product_name'], 'quantity': stock['quantity']})


# 步骤1：检查库存
@app.route('/api/check-stock', methods=['POST'])
def check_stock():
    db = get_db()
    stock = db.execute("SELECT * FROM stock WHERE id = 1").fetchone()
    if stock['quantity'] > 0:
        return jsonify({'available': True, 'message': '库存充足'})
    return jsonify({'available': False, 'message': '库存不足'}), 400


# 步骤2：创建订单（扣减库存）- 无事务锁定
@app.route('/api/create-order', methods=['POST'])
def create_order():
    db = get_db()
    # 不安全的设计：检查库存和扣减库存分为两步，没有数据库事务锁定
    stock = db.execute("SELECT * FROM stock WHERE id = 1").fetchone()
    if stock['quantity'] <= 0:
        return jsonify({'success': False, 'message': '库存不足'}), 400

    # 增大竞争窗口，使Race Condition更容易触发
    time.sleep(0.1)

    # 扣减库存
    db.execute("UPDATE stock SET quantity = quantity - 1 WHERE id = 1")
    order_no = f"ORD{os.urandom(4).hex()}"
    db.execute("INSERT INTO orders (order_no, status, product_id) VALUES (?, 'pending', 1)", (order_no,))
    db.commit()
    return jsonify({'success': True, 'order_no': order_no, 'message': '订单创建成功'})


# 步骤3：支付
@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.get_json() or {}
    order_no = data.get('order_no')
    if not order_no:
        return jsonify({'success': False, 'message': '缺少订单号'}), 400

    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE order_no = ?", (order_no,)).fetchone()
    if not order:
        return jsonify({'success': False, 'message': '订单不存在'}), 404

    db.execute("UPDATE orders SET status = 'paid' WHERE order_no = ?", (order_no,))
    db.commit()

    with open('/flag', 'r') as f:
        flag = f.read().strip()
    return jsonify({'success': True, 'message': '支付成功！', 'flag': flag})


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=80, threaded=True)
