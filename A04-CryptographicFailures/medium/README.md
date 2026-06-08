# A04 Cryptographic Failures - Medium

## 题目信息

- **难度**: Medium
- **类型**: Web / Cryptographic Failures
- **技术栈**: Python Flask + PyCryptodome
- **端口**: 80

## 题目描述

欢迎来到 AES Cookie Shop！我们使用工业级 AES-128-CBC 加密来保护您的会话 Cookie。

Cookie 格式为 `iv:ciphertext`（hex编码），内容为 JSON：
```json
{"user":"guest","role":"user"}
```

只有管理员才能查看 Flag，你能突破加密保护吗？

## 题目要求

1. 获取你的加密 Cookie
2. 利用 CBC 模式的特性修改密文
3. 将你的角色从 `user` 提升为 `admin`
4. 使用修改后的 Cookie 访问 `/flag`

## 提示

- CBC 模式中，修改前一个密文块的某个字节会影响下一个明文块的对应字节
- 不需要知道 AES 密钥
- 注意 PKCS7 填充的保持

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
