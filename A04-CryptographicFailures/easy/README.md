# A04 Cryptographic Failures - Easy

## 题目信息

- **难度**: Easy
- **类型**: Web / Cryptographic Failures
- **技术栈**: Python Flask
- **端口**: 80

## 题目描述

这是一个安全的登录系统。用户可以注册并登录，系统会为每个用户生成一个独特的会话Token。

然而，系统的Token生成算法似乎有些问题...

## 题目要求

1. 分析Token生成算法
2. 预测管理员的会话Token
3. 使用预测的Token访问 `/admin/flag` 获取Flag

## 提示

- 管理员在整点时刻登录过系统
- 注意查看页面源代码
- 你自己的Token生成时间戳会暴露算法规律

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
