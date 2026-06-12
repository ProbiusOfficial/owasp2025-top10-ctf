import requests
from urllib.parse import unquote

TARGET = "http://110.42.47.58:33451"

# 1. 获取原始 cookie
session = requests.Session()
resp = session.get(TARGET)
cookie = session.cookies.get('session')
print(f"[+] Original cookie: {cookie}")

# 2. 解析 cookie
iv_hex, ct_hex = cookie.split(':')
iv = bytes.fromhex(iv_hex)
ct = bytes.fromhex(ct_hex)

# 分块（AES块大小 = 16）
c1 = ct[:16]
c2 = ct[16:]

# 3. 原始明文块2（已知）
p2 = b'"role":"user"}\x02\x02'
# 4. 目标明文块2
p2_target = b'"role":"admin"}\x01'

# 5. 翻转 C1 的字节
c1_new = bytearray(c1)
for i in range(len(p2)):
    c1_new[i] ^= p2[i] ^ p2_target[i]

# 6. 构造新 cookie
new_ct = bytes(c1_new) + c2
new_cookie = iv.hex() + ':' + new_ct.hex()
print(f"[+] Modified cookie: {new_cookie}")

# 7. 发送请求获取 flag
session2 = requests.Session()
session2.cookies.set('session', new_cookie)
flag_resp = session2.get(f"{TARGET}/flag")
print(flag_resp.text)