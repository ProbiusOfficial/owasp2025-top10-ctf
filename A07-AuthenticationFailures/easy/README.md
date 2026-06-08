# A07 Authentication Failures - Easy

## 题目描述

这是一个简单的登录系统，管理员用户名为 `admin`。但是管理员设置了一个非常弱的密码，可能是以下常见密码之一：

```
password123
admin123
12345678
qwerty123
```

系统没有登录失败限制、没有验证码、没有IP封锁。你可以尽情尝试！

## 目标

使用暴力破解的方式，找到管理员 `admin` 的正确密码，登录后在管理员页面获取 Flag。

## 接口说明

- `POST /login` - 登录接口，参数 `username` 和 `password`
- `GET /admin` - 管理员页面，登录后可见 Flag
- 登录错误时会返回明确的提示："用户不存在" 或 "密码错误"

## 提示

- 密码使用 SHA256 哈希存储
- 你可以用 Python 编写一个简单的爆破脚本
- 只给了4个候选密码，很快就能试出来

## 启动方式

```bash
docker-compose up --build
```

访问 http://localhost:8087
