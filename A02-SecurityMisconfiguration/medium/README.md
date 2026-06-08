# A02 Security Misconfiguration - Medium

## 题目信息

- **类型**: Security Misconfiguration（安全配置错误）
- **难度**: Medium
- **技术栈**: Python Flask + SQLite
- **容器端口**: 80

## 题目描述

星辰社区刚刚上线了一个留言板系统。开发团队声称已经实施了"强大的XSS防护措施"，包括过滤 `<script>` 标签、`javascript:` 协议和 `onerror` 事件。然而，安全团队在审查时发现，系统似乎缺少了一些重要的HTTP安全头……

你能突破防护，获取管理员面板中的秘密密钥吗？

## 访问方式

启动容器后，访问 `http://<host>:<port>/` 查看留言板。

管理员查看页面：`http://<host>:<port>/admin/view`

## 提示

- 有时候，简单的字符串替换并不是真正的安全
- 思考 "双重编码" 或 "嵌套标签" 的绕过方式
- 管理员页面会渲染并执行留言中的JavaScript
- 缺少 Content-Security-Policy 头意味着什么？

## 部署说明

```bash
docker-compose up --build
```

或

```bash
docker build -t a02-medium .
docker run -p 8081:80 -e DASFLAG=flag{your_flag_here} a02-medium
```
