import os
import json
from flask import Flask, request, make_response, render_template_string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

# AES-128-CBC 密钥（参赛者不可知）
KEY = b'SuperSecretKey!!'


def encrypt_cookie(data: bytes) -> str:
    """加密数据，返回 iv:ciphertext 的 hex 格式"""
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(data, AES.block_size))
    return iv.hex() + ':' + ct.hex()


def decrypt_cookie(cookie: str) -> bytes:
    """解密 cookie"""
    parts = cookie.split(':')
    if len(parts) != 2:
        raise ValueError("Invalid cookie format")
    iv = bytes.fromhex(parts[0])
    ct = bytes.fromhex(parts[1])
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)


INDEX_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>AES Cookie Shop</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .cookie { background: #e7f3ff; padding: 10px; border-radius: 4px; font-family: monospace; word-break: break-all; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; margin: 5px; }
        .info { background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🍪 AES Cookie Shop</h1>
        <p>Welcome to our secure shop. Your identity is stored in an AES-encrypted cookie.</p>
        <div class="info">
            <strong>Your current cookie:</strong><br>
            <div class="cookie">{{ cookie }}</div>
        </div>
        <p>Current role: <strong>{{ role }}</strong></p>
        <p>
            <a href="/flag"><button>🏁 Get Flag</button></a>
            <a href="/reset"><button>Reset Cookie</button></a>
        </p>
        <hr>
        <h3>API Endpoints</h3>
        <ul>
            <li><code>GET /flag</code> - Get the flag (admin only)</li>
            <li><code>GET /reset</code> - Reset your cookie to default guest role</li>
        </ul>
    </div>
</body>
</html>
'''

FLAG_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Flag</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .flag { background: #d4edda; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 1.2em; color: #155724; }
        .error { background: #f8d7da; padding: 15px; border-radius: 4px; color: #721c24; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Flag Page</h1>
        {% if flag %}
            <div class="flag">{{ flag }}</div>
        {% else %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <p><a href="/">← Back to Home</a></p>
    </div>
</body>
</html>
'''


def get_role_from_cookie(cookie):
    try:
        plaintext = decrypt_cookie(cookie)
        data = json.loads(plaintext)
        return data.get('role', 'unknown')
    except Exception:
        return 'invalid'


@app.route('/')
def index():
    cookie = request.cookies.get('session')
    if not cookie:
        # 生成默认 cookie
        data = json.dumps({"user": "guest", "role": "user"}, separators=(',', ':')).encode()
        cookie = encrypt_cookie(data)
        resp = make_response(render_template_string(INDEX_HTML, cookie=cookie, role='user'))
        resp.set_cookie('session', cookie)
        return resp
    role = get_role_from_cookie(cookie)
    return render_template_string(INDEX_HTML, cookie=cookie, role=role)


@app.route('/reset')
def reset():
    data = json.dumps({"user": "guest", "role": "user"}, separators=(',', ':')).encode()
    cookie = encrypt_cookie(data)
    resp = make_response(redirect('/'))
    resp.set_cookie('session', cookie)
    return resp


@app.route('/flag')
def get_flag():
    cookie = request.cookies.get('session')
    if not cookie:
        return render_template_string(FLAG_HTML, flag=None, error="No session cookie found."), 403

    try:
        plaintext = decrypt_cookie(cookie)
    except Exception as e:
        # 解密失败时，检查是否包含目标子串（为了兼容翻转攻击）
        # 实际上翻转攻击应该产生有效的PKCS7填充
        # 这里捕获异常并展示错误
        return render_template_string(FLAG_HTML, flag=None,
                                      error=f"Cookie decryption failed: {str(e)}"), 400

    # 检查是否包含 admin 角色标记
    if b'"role":"admin"' in plaintext:
        try:
            with open('/flag', 'r') as f:
                flag = f.read().strip()
        except:
            flag = "flag{TEST_Dynamic_FLAG}"
        return render_template_string(FLAG_HTML, flag=flag, error=None)

    return render_template_string(FLAG_HTML, flag=None,
                                  error="Access denied. Admin role required."), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
