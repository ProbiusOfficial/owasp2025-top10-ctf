# A08 Data Integrity Failures - Hard

## 题目信息

- **难度**: Hard
- **考点**: PHP 反序列化 + POP链（Property Oriented Programming）
- **技术栈**: PHP + Nginx

## 题目描述

欢迎来到 Secure Config Manager！本系统提供 PHP 对象的序列化与反序列化服务。

系统中存在多个内置类，你能通过精心构造的序列化数据，触发 POP 链，最终读取到 `/flag` 吗？

## 接口说明

### GET /
首页，提供反序列化测试表单和系统信息。

### POST /?action=api
反序列化用户提交的 PHP 序列化字符串。

**参数**:
- `data` — PHP 序列化字符串

**响应**: JSON 格式，包含反序列化结果信息。

## 提示

- 系统使用了 PHP 原生的 `unserialize()` 函数
- 注意观察源码中类的 `__destruct()` 和 `__toString()` 魔术方法
- flag 文件位于 `/flag`

## 运行方式

```bash
docker-compose up --build
```

访问 http://localhost:8080
