# A05-Injection Easy - SQL注入（经典字符串拼接）

## 题目描述

欢迎来到用户查询系统！这是一个简单的用户信息查询平台，你可以通过用户ID查询用户信息。

## 题目信息

- **难度**: Easy
- **类型**: Web / SQL Injection
- **技术栈**: Python Flask + SQLite

## 访问方式

启动容器后访问 `http://<ip>:<port>/`

## 目标

获取数据库中的 flag。

## 提示

- 查询功能可能存在 SQL 注入漏洞
- 数据库中有一个名为 `secret` 的表
- 尝试通过输入构造特殊的查询语句
