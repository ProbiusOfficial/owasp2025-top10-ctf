# A10-ExceptionHandling - Hard

## 题目名称
异常侧信道 (Exception Side-Channel)

## 题目描述

这是一个安全的密码验证系统。系统提示：密码错误时会给出友好的反馈信息，帮助用户了解自己的输入与正确密码的接近程度。

系统管理员声称密码是不可破解的，因为它使用了复杂的字符串。但是，异常处理模块的设计似乎有些问题...

你能通过系统反馈的异常信息找到正确的密码并获取flag吗？

## 访问方式

- Web: `http://<target>:<port>/`
- API: `POST /api/verify` 或 `GET /verify?password=xxx`

## 提示

- 仔细观察密码错误时的响应信息
- 每次错误的猜测都能获得一些有用的信息
- 思考如何利用这些信息逐步缩小密码范围
- 密码包含字母、数字和特殊字符

## 题目考点

- OWASP A10: Mishandling of Exceptional Conditions
- 异常信息侧信道攻击（Side-Channel Attack via Error Messages）
- 逐字节盲注（Byte-by-Byte Blind Extraction）
