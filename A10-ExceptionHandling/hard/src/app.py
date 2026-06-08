#!/usr/bin/env python3
"""
A10-ExceptionHandling - Hard
漏洞：异常信息侧信道（逐字节盲注密码）
"""

import os
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG_PATH = '/flag'

# 读取flag
if os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, 'r') as f:
        REAL_FLAG = f.read().strip()
else:
    REAL_FLAG = "flag{TEST_Dynamic_FLAG}"

# 目标密码（参赛者需要通过侧信道爆破）
CORRECT_PASSWORD = "S3cr3tP@ssw0rd123"

class InvalidPassword(Exception):
    """自定义密码错误异常"""
    pass

# 注册自定义异常处理器 —— 返回详细的错误信息
def handle_invalid_password(e):
    # 返回异常消息中的匹配长度信息
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400

app.register_error_handler(InvalidPassword, handle_invalid_password)

# 全局异常处理器也返回详细信息（用于其他异常）
@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    return jsonify({
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc().split('\n')
    }), 500

# ========== 核心漏洞：侧信道泄露 ==========

def verify_password(pwd):
    """
    密码验证函数。
    漏洞：当密码不正确时，异常信息泄露了匹配前缀的长度。
    参赛者可以利用这个信息逐字节爆破密码。
    """
    if pwd == CORRECT_PASSWORD:
        return True
    
    # ❌ 侧信道泄露：计算匹配前缀长度并放入异常消息
    match_len = sum(1 for a, b in zip(pwd, CORRECT_PASSWORD) if a == b)
    raise InvalidPassword(f"Password incorrect. Matched {match_len} chars.")

# ========== 路由 ==========

@app.route('/')
def index():
    return render_template_string('''
    <h1>安全密码验证系统</h1>
    <p>本系统使用军工级密码验证算法。</p>
    <p>请通过API提交密码进行验证：</p>
    <pre>POST /api/verify
Content-Type: application/json

{"password": "your_guess"}</pre>
    <p>提示：密码长度与 "S3cr3tP@ssw0rd123" 相同。</p>
    <p>如果密码错误，系统会给出友好的提示信息。</p>
    ''')

@app.route('/api/verify', methods=['POST'])
def api_verify():
    data = request.get_json(force=True, silent=True) or {}
    pwd = data.get('password', '')
    
    # 调用有漏洞的验证函数
    if verify_password(pwd):
        return jsonify({
            "success": True,
            "message": "验证通过！",
            "flag": REAL_FLAG
        })
    
    # 正常流程不会到这里，因为verify_password会在错误时抛出异常
    return jsonify({"success": False, "error": "Unknown error"}), 500

# 提供一个GET版本方便测试
@app.route('/verify')
def verify_get():
    pwd = request.args.get('password', '')
    if verify_password(pwd):
        return jsonify({
            "success": True,
            "message": "验证通过！",
            "flag": REAL_FLAG
        })
    return jsonify({"success": False, "error": "Unknown error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
