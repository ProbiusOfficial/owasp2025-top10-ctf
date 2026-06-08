# A07 Authentication Failures - Medium

## 题目描述

这是一个使用 JWT (JSON Web Token) 进行身份认证的系统。系统注册和登录后会返回一个 JWT Token，你需要分析这个 Token 的签名机制，找到服务器使用的弱密钥，然后伪造一个管理员身份的 Token 来获取 Flag。

## 目标

1. 注册一个普通账户并登录，获取 JWT Token
2. 分析 JWT 头部，发现使用 HS256 算法
3. 使用字典爆破找到服务器签名使用的密钥
4. 用找到的密钥伪造 `role=admin` 的 JWT
5. 访问 `/admin/flag` 获取 Flag

## 接口说明

- `POST /register` - 注册，参数 `username`, `password`
- `POST /login` - 登录，参数 `username`, `password`，返回 JWT Token
- `GET /profile` - 查看个人信息，Header 携带 `Authorization: Bearer <token>`
- `GET /admin/flag` - 管理员接口，需要 `role=admin`

## 提示

- JWT 头部使用了 `alg: HS256`
- 密钥是一个常见的英文单词（4-8个字母）
- `src/english_words.txt` 中提供了一个常见单词字典（约50个单词），可以作为爆破字典
- 你可以使用 Python 的 `PyJWT` 库进行爆破和伪造

## 启动方式

```bash
docker-compose up --build
```

访问 http://localhost:8088
