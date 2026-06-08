# A05-Injection Hard - 命令注入（过滤绕过）

## 题目描述

这是一个网络连通性测试工具，输入IP地址或域名后，服务器会执行ping命令测试网络连通性。

## 题目信息

- **难度**: Hard
- **类型**: Web / Command Injection
- **技术栈**: Python Flask

## 访问方式

启动容器后访问 `http://<ip>:<port>/`

## 目标

读取服务器上的 `/flag` 文件。

## 提示

- 系统已过滤多种危险字符
- 尝试使用Linux shell的特殊语法绕过过滤
- `${IFS}` 可能是你的好朋友
