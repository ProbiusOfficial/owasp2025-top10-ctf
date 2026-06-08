# A07 Authentication Failures - Hard

## 题目描述

这是一个带有密码重置功能的系统。密码重置流程如下：
1. 输入注册邮箱，系统生成一个重置 token
2. 使用 token 和新密码访问重置接口即可修改密码

然而，系统的 token 生成算法存在缺陷，而且还有一个调试接口泄露了最近生成的 token 信息...

## 目标

1. 注册一个普通账户
2. 请求密码重置，观察 token 的生成规律
3. 访问调试信息泄露页面，查看 token 详情
4. 分析 token 生成算法，预测管理员账户的 token
5. 重置管理员密码并登录，获取 Flag

## 接口说明

- `POST /register` - 注册，参数 `username`, `email`, `password`
- `POST /login` - 登录，参数 `username`, `password`
- `POST /forgot-password` - 请求密码重置，参数 `email`
- `POST /reset-password` - 使用 token 重置密码，参数 `token`, `new_password`
- `GET /check-token?token=xxx` - 验证 token 是否有效（可用于测试猜测的 token）
- `GET /debug/tokens` - **调试信息泄露页面**，显示最近生成的 token 列表

## 提示

- 管理员的邮箱是 `admin@ctf.local`，用户名是 `admin`
- token 生成可能与用户ID和时间有关
- 管理员的用户ID通常是 `1`
- 你可以利用 `/check-token` 接口快速验证猜测的 token
- 时间精度可能没有你想的那么细

## 启动方式

```bash
docker-compose up --build
```

访问 http://localhost:8089
