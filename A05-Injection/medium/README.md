# A05-Injection Medium - SSTI服务器端模板注入（Jinja2）

## 题目描述

这是一个邮件/报告生成系统，用户可以输入Jinja2模板内容，系统会渲染生成邮件正文。

## 题目信息

- **难度**: Medium
- **类型**: Web / SSTI (Server-Side Template Injection)
- **技术栈**: Python Flask + Jinja2

## 访问方式

启动容器后访问 `http://<ip>:<port>/`

## 目标

读取服务器上的 `/flag` 文件。

## 提示

- 系统使用了Jinja2模板引擎
- 部分关键字被过滤
- 尝试使用Jinja2内置过滤器绕过限制
