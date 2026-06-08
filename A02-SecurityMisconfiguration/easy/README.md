# A02 Security Misconfiguration - Easy

## 题目信息

- **类型**: Security Misconfiguration（安全配置错误）
- **难度**: Easy
- **技术栈**: Python Flask + 静态网站
- **容器端口**: 80

## 题目描述

星辰科技有限公司刚刚上线了全新的企业官网。开发团队在开发过程中使用了Git进行版本控制，但在部署到生产环境时，可能忘记了一些重要的安全步骤……

你能找到网站中隐藏的秘密吗？

## 访问方式

启动容器后，访问 `http://<host>:<port>/` 即可看到目标网站。

## 提示

- 生产环境部署时，哪些目录不应该被公开访问？
- Git仓库的历史记录中可能藏有秘密

## 部署说明

```bash
docker-compose up --build
```

或

```bash
docker build -t a02-easy .
docker run -p 8080:80 -e DASFLAG=flag{your_flag_here} a02-easy
```
