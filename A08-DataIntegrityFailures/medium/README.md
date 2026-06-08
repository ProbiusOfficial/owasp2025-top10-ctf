# A08 Data Integrity Failures - Medium

## 题目信息

- **难度**: Medium
- **考点**: Python Pickle 反序列化漏洞（Deserialization RCE）
- **技术栈**: Python Flask

## 题目描述

这是一个数据序列化/反序列化服务平台。你可以提交 Base64 编码的 Python pickle 序列化数据，系统将为你反序列化。

服务器上似乎存放着一些敏感文件，你能利用反序列化功能获取它们吗？

## 接口说明

### GET /
首页，提供反序列化测试表单。

### POST /deserialize
反序列化用户提交的 Base64 编码 pickle 数据。

**参数**:
- `data` — Base64 编码的 Python pickle 序列化数据

### GET /static/<filename>
访问 static 目录下的文件。

## 提示

- Python 的 `pickle` 模块在反序列化时会执行对象中的 `__reduce__` 方法
- 构造特殊的对象，让服务器执行任意命令
- flag 文件位于 `/flag`

## 运行方式

```bash
docker-compose up --build
```

访问 http://localhost:8080
