# A02 Security Misconfiguration - Hard

## 题目信息

- **类型**: Security Misconfiguration（安全配置错误）
- **难度**: Hard
- **技术栈**: Python Flask + xml.etree.ElementTree
- **容器端口**: 80

## 题目描述

星辰数据处理中心提供企业级 XML 数据解析服务。系统支持多种编码格式（UTF-8、UTF-16等），可以解析复杂的XML文档结构并返回结构化数据。

系统的XML解析器在配置时似乎忽略了一些安全建议……你能利用这个配置错误获取服务器上的敏感信息吗？

## 访问方式

启动容器后，访问 `http://<host>:<port>/` 查看XML解析服务。

## 提示

- 这是一个XML解析服务，思考一下XML解析器常见的配置安全问题
- 系统支持文件上传和直接文本输入两种方式
- 系统声明支持UTF-16编码
- 服务器上有一个 `/flag` 文件

## 部署说明

```bash
docker-compose up --build
```

或

```bash
docker build -t a02-hard .
docker run -p 8082:80 -e DASFLAG=flag{your_flag_here} a02-hard
```
