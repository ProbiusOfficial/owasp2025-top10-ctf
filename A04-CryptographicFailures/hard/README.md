# A04 Cryptographic Failures - Hard

## 题目信息

- **难度**: Hard
- **类型**: Web / Cryptographic Failures
- **技术栈**: Python Flask + PyJWT + Cryptography
- **端口**: 80

## 题目描述

我们的认证服务支持多种 JWT 算法以确保兼容性，包括 RS256（RSA签名）和 HS256（HMAC签名）。

公钥可以在 `/.well-known/jwks.json` 或 `/public.pem` 获取。

当前你以 `guest` 身份登录。请获取管理员权限并拿到 Flag。

## 题目要求

1. 从 JWKS 端点获取公钥
2. 构造一个 alg 为 HS256 的 JWT
3. 使用公钥内容作为 HMAC 密钥对 Token 进行签名
4. 发送伪造的 admin JWT 到 `/flag` 获取 Flag

## 提示

- RS256 使用私钥签名、公钥验证（非对称）
- HS256 使用对称密钥签名和验证
- 如果服务端在 alg=HS256 时错误地使用了公钥内容作为对称密钥...

## 环境变量

支持通过以下环境变量注入Flag：
- `DASFLAG`
- `FLAG`
- `GZCTF_FLAG`

## 启动方式

```bash
docker-compose up --build
```

访问 http://localhost:8080
