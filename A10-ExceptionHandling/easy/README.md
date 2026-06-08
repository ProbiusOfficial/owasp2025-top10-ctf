# A10-ExceptionHandling - Easy

## 题目名称
错误信息泄露 (Error Message Disclosure)

## 题目描述

欢迎来到安全文件阅读器！这是一个正在开发中的Web应用，提供了文件阅读和用户登录功能。

管理员区域似乎藏有重要信息，但只有管理员才能访问。你能找到获取flag的方法吗？

## 访问方式

- Web: `http://<target>:<port>/`

## 提示

- 应用在某些情况下会返回详细的错误信息
- 仔细查看错误页面中可能泄露的敏感内容
- Flask应用使用session token来识别用户身份

## 题目考点

- OWASP A10: Mishandling of Exceptional Conditions
- 异常信息泄露（Information Disclosure via Error Messages）
- Flask session 伪造
