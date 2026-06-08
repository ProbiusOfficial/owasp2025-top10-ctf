import os
import base64
import json
import hmac
import hashlib
import jwt
from flask import Flask, request, jsonify, render_template_string
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

# 生成 RSA 密钥对
private_key_obj = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key_obj = private_key_obj.public_key()

# PEM 格式
PRIVATE_KEY_PEM = private_key_obj.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
PUBLIC_KEY_PEM = public_key_obj.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# JWKS 格式
public_numbers = public_key_obj.public_numbers()
n_bytes = public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, 'big')
e_bytes = public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, 'big')

def b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

JWKS = {
    "keys": [
        {
            "kty": "RSA",
            "use": "sig",
            "kid": "key-2025",
            "n": b64url_encode(n_bytes),
            "e": b64url_encode(e_bytes),
            "alg": "RS256"
        }
    ]
}


INDEX_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>JWT Auth Service</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; }
        .box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .jwt { background: #e7f3ff; padding: 10px; border-radius: 4px; font-family: monospace; word-break: break-all; font-size: 0.9em; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; margin: 5px; }
        .info { background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔐 JWT Authentication Service</h1>
        <p>We support both <code>RS256</code> and <code>HS256</code> algorithms for maximum compatibility.</p>

        <div class="info">
            <strong>Your JWT Token:</strong><br>
            <div class="jwt">{{ token }}</div>
            <p>Role: <strong>{{ role }}</strong></p>
        </div>

        <p>
            <a href="/flag"><button>🏁 Get Flag</button></a>
            <a href="/.well-known/jwks.json"><button>View JWKS</button></a>
        </p>

        <hr>
        <h3>API Documentation</h3>
        <ul>
            <li><code>GET /.well-known/jwks.json</code> - Get public key in JWKS format</li>
            <li><code>POST /login</code> - Login as guest (body: <code>{"username":"guest"}</code>)</li>
            <li><code>GET /flag</code> - Get flag (requires admin role)</li>
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
        <h1>Admin Flag</h1>
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


def verify_token(token):
    """验证 JWT Token - 存在算法混淆漏洞 """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")

        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        alg = header.get('alg', 'RS256')

        if alg == 'RS256':
            # 正常 RS256 验证（使用 PyJWT）
            payload = jwt.decode(token, PUBLIC_KEY_PEM, algorithms=['RS256'])
            return payload
        elif alg == 'HS256':
            # 漏洞：使用公钥 PEM 内容作为 HMAC 对称密钥
            # 手动验证 HMAC，绕过 PyJWT 的 key 类型检查
            msg = (parts[0] + '.' + parts[1]).encode('ascii')
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(PUBLIC_KEY_PEM, msg, hashlib.sha256).digest()
            ).rstrip(b'=')
            actual_sig = parts[2].encode('ascii')
            # 处理可能的填充差异
            if not hmac.compare_digest(expected_sig, actual_sig):
                raise ValueError("Invalid HMAC signature")
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            return payload
        else:
            raise ValueError(f"Unsupported algorithm: {alg}")
    except Exception as e:
        raise e


def create_token(payload):
    """使用 RS256 签发 Token"""
    return jwt.encode(payload, PRIVATE_KEY_PEM, algorithm='RS256', headers={"kid": "key-2025"})


@app.route('/')
def index():
    token = request.cookies.get('jwt')
    role = 'guest'
    if token:
        try:
            payload = verify_token(token)
            role = payload.get('role', 'guest')
        except:
            pass
    else:
        # 自动创建 guest token
        payload = {"sub": "guest", "role": "guest"}
        token = create_token(payload)
    return render_template_string(INDEX_HTML, token=token, role=role)


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
    except:
        data = {}
    username = data.get('username', 'guest')
    payload = {"sub": username, "role": "guest"}
    token = create_token(payload)
    resp = jsonify({"token": token, "role": "guest"})
    resp.set_cookie('jwt', token)
    return resp


@app.route('/.well-known/jwks.json')
def jwks():
    return jsonify(JWKS)


@app.route('/public.pem')
def public_pem():
    """直接暴露原始公钥 PEM"""
    return PUBLIC_KEY_PEM.decode('ascii'), 200, {'Content-Type': 'text/plain'}


@app.route('/flag')
def get_flag():
    token = request.cookies.get('jwt')
    if not token:
        # 也尝试从 Authorization header 获取
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth[7:]

    if not token:
        return render_template_string(FLAG_HTML, flag=None,
                                      error="No JWT token provided."), 403

    try:
        payload = verify_token(token)
    except Exception as e:
        return render_template_string(FLAG_HTML, flag=None,
                                      error=f"Token verification failed: {str(e)}"), 403

    if payload.get('role') == 'admin' and payload.get('sub') == 'admin':
        try:
            with open('/flag', 'r') as f:
                flag = f.read().strip()
        except:
            flag = "flag{TEST_Dynamic_FLAG}"
        return render_template_string(FLAG_HTML, flag=flag, error=None)

    return render_template_string(FLAG_HTML, flag=None,
                                  error="Access denied. Admin privileges required."), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
