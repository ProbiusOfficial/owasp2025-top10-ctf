# OWASP Top 10:2025 CTF 挑战题目集

<p align="center">
  <img src="https://img.shields.io/badge/OWASP-Top%2010%202025-red?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP Top 10 2025">
  <img src="https://img.shields.io/badge/CTF-24%20Challenges-blue?style=for-the-badge" alt="24 Challenges">
  <img src="https://img.shields.io/badge/Docker-Supported-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Supported">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT">
</p>

> 基于 **OWASP Top 10:2025** 官方框架命制的 CTF 竞赛题目集，共 **8 个类型 × 3 个梯度 = 24 道题目**，每题均为单容器部署，支持动态 Flag 注入，适用于 CTF 竞赛、安全培训和渗透测试教学。

---

## 📋 目录

- [题目总览](#-题目总览)
- [快速开始](#-快速开始)
- [动态 Flag 注入](#-动态-flag-注入)
- [题目详情](#-题目详情)
- [技术栈分布](#-技术栈分布)
- [使用建议](#-使用建议)
- [参考来源](#-参考来源)
- [生成式人工智能使用说明](#-生成式人工智能使用说明)
- [许可协议](#-许可协议)
- [安全声明](#-安全声明)

---

## 📊 题目总览

| OWASP 类型 | 题目数量 | 简单 (Easy) | 中等 (Medium) | 困难 (Hard) |
|-----------|---------|------------|--------------|------------|
| **A01** Broken Access Control | 3 | IDOR 水平权限绕过 | JWT 前端权限绕过 | SSRF + IP 编码绕过 |
| **A02** Security Misconfiguration | 3 | `.git` 目录泄露 | 安全头缺失 + XSS 绕过 | XXE 外部实体注入 |
| **A04** Cryptographic Failures | 3 | 弱随机数 Token 预测 | CBC 字节翻转攻击 | JWT 算法混淆 RS256→HS256 |
| **A05** Injection | 3 | SQL 注入 | SSTI (Jinja2) | 命令注入 + 黑名单绕过 |
| **A06** Insecure Design | 3 | 支付逻辑绕过 | 条件竞争 (Race Condition) | 批量操作越权设计缺陷 |
| **A07** Authentication Failures | 3 | 弱密码暴力破解 | JWT 弱密钥字典爆破 | 密码重置令牌预测 |
| **A08** Data Integrity Failures | 3 | 原型污染 (lodash) | Pickle 反序列化 RCE | PHP 反序列化 POP 链 |
| **A10** Exception Handling | 3 | 错误信息泄露 | 失败开放 (Fail Open) | 异常信息侧信道盲注 |

**总计：8 类型 × 3 梯度 = 24 道题目**

---

## 🚀 快速开始

### 目录结构

```
CTF-Challenges/
├── A01-BrokenAccessControl/
│   ├── easy/          # IDOR 水平权限绕过
│   ├── medium/        # JWT 前端权限绕过
│   └── hard/          # SSRF + IP 编码绕过
├── A02-SecurityMisconfiguration/
│   ├── easy/          # .git 目录泄露
│   ├── medium/        # 安全头缺失 + XSS 绕过
│   └── hard/          # XXE 外部实体注入
├── A04-CryptographicFailures/
│   ├── easy/          # 弱随机数 Token 预测
│   ├── medium/        # CBC 字节翻转攻击
│   └── hard/          # JWT 算法混淆攻击
├── A05-Injection/
│   ├── easy/          # SQL 注入
│   ├── medium/        # SSTI (Jinja2)
│   └── hard/          # 命令注入 + 黑名单绕过
├── A06-InsecureDesign/
│   ├── easy/          # 支付逻辑绕过
│   ├── medium/        # 条件竞争 (Race Condition)
│   └── hard/          # 批量操作越权
├── A07-AuthenticationFailures/
│   ├── easy/          # 弱密码暴力破解
│   ├── medium/        # JWT 弱密钥字典爆破
│   └── hard/          # 密码重置令牌预测
├── A08-DataIntegrityFailures/
│   ├── easy/          # 原型污染 (Node.js)
│   ├── medium/        # Pickle 反序列化 RCE
│   └── hard/          # PHP 反序列化 POP 链
└── A10-ExceptionHandling/
    ├── easy/          # 错误信息泄露
    ├── medium/        # 失败开放 (Fail Open)
    └── hard/          # 异常信息侧信道盲注
```

### 每个题目的标准文件

```
<difficulty>/
├── src/               # 应用源码
│   ├── app.py         # 主应用 (或 app.js / index.php)
│   ├── requirements.txt / package.json
│   └── ...            # 其他源码文件
├── Dockerfile         # 单容器构建
├── docker-compose.yml # 本地测试用
├── README.md          # 题目描述
└── WriteUP.md         # 完整解题思路
```

---

## 🏴 动态 Flag 注入

所有题目均支持通过环境变量注入动态 Flag：

| 环境变量 | 说明 |
|---------|------|
| `DASFLAG` | 主要 Flag 变量 |
| `FLAG` | 备用 Flag 变量 |
| `GZCTF_FLAG` | GZCTF 平台 Flag 变量 |

启动时自动将 Flag 写入容器内的 `/flag` 文件，供应用读取。

### 本地测试

```bash
cd <题目目录>
docker-compose up -d
# 访问 http://localhost:<port>
```

---

## 📝 题目详情

### A01 - Broken Access Control（失效的访问控制）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 文档查看系统 | IDOR | 修改 URL 参数 `doc_id` 访问未授权文档 |
| Medium | 权限管理系统 | JWT 前端绕过 | 前端隐藏管理员功能，后端 API 未校验角色 |
| Hard | 图片获取服务 | SSRF | 通过十进制/十六进制/八进制 IP 编码绕过黑名单访问内网 |

### A02 - Security Misconfiguration（安全配置错误）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 公司官网 | .git 泄露 | 通过 `.git` 目录获取历史提交中的敏感文件 |
| Medium | 留言板系统 | XSS 绕过 | 双重编码绕过字符串替换过滤，CSP 缺失 |
| Hard | XML 处理服务 | XXE | 利用外部实体读取 `/flag`，UTF-16 编码绕过 |

### A04 - Cryptographic Failures（加密机制失效）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | Token 生成器 | 弱随机数 | 基于时间戳的伪随机数种子预测 |
| Medium | Cookie 加密系统 | CBC 翻转 | 通过修改密文块翻转明文中的 `role` 字段 |
| Hard | JWT 认证系统 | 算法混淆 | RS256 公钥作为 HS256 HMAC 密钥伪造签名 |

### A05 - Injection（注入攻击）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 用户查询系统 | SQL 注入 | 经典字符串拼接 SQL 注入，`UNION SELECT` 读取 flag |
| Medium | 邮件模板生成器 | SSTI | Jinja2 模板注入，使用 `\|attr()` + 列表拼接绕过过滤 |
| Hard | Ping 测试工具 | 命令注入 | 黑名单过滤绕过，换行符 + 输入重定向执行命令 |

### A06 - Insecure Design（不安全的设计）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 金币商店 | 支付逻辑绕过 | 前端计算金额，后端信任前端传入的参数 |
| Medium | 限时秒杀 | 条件竞争 | TOCTOU 漏洞，并发请求导致库存超卖 |
| Hard | 笔记应用 | 批量越权 | 批量查询只校验第一个 ID，后续 ID 未校验 |

### A07 - Authentication Failures（身份认证失败）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 登录系统 | 弱密码 | 无防护的暴力破解，常见弱密码字典 |
| Medium | JWT 认证 | 弱密钥 | HS256 密钥字典爆破，伪造 admin Token |
| Hard | 密码重置 | 令牌预测 | MD5(user_id:时间戳) 可预测，时间窗口内爆破 |

### A08 - Data Integrity Failures（数据完整性故障）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 配置更新服务 | 原型污染 | `_.merge()` 未过滤 `__proto__`，污染 `isAdmin` |
| Medium | 数据序列化服务 | Pickle RCE | `pickle.loads()` 直接反序列化用户输入，命令执行 |
| Hard | 对象反序列化 | PHP POP 链 | `unserialize()` 触发 `__destruct`→`__toString` 链读取文件 |

### A10 - Exception Handling（异常情况处理不当）

| 难度 | 题目名称 | 漏洞类型 | 核心考点 |
|------|---------|---------|---------|
| Easy | 文件查看系统 | 信息泄露 | 异常返回完整堆栈，泄露 SECRET_KEY |
| Medium | 后台管理系统 | 失败开放 | `except Exception: return True` 导致认证绕过 |
| Hard | 密码验证系统 | 侧信道 | 异常信息泄露匹配前缀长度，逐字节盲注 |

---

## 🔧 技术栈分布

| 技术栈 | 题目数量 |
|-------|---------|
| Python Flask | 21 题 |
| Node.js + Express | 1 题 (A08-easy) |
| PHP + Nginx | 1 题 (A08-hard) |

---

## 📖 使用建议

### 作为参赛者
1. 阅读题目目录下的 `README.md` 了解题目背景
2. 尝试独立解题
3. 遇到困难时参考 `WriteUP.md`

### 作为出题者/平台运维
1. 每个题目目录包含完整的 `Dockerfile`，可直接构建镜像
2. 使用 `docker-compose.yml` 进行本地测试
3. 部署时通过环境变量注入动态 Flag
4. 所有题目均为**单容器**，适配各类 CTF 平台（不支持 docker-compose 部署，compose 仅用于本地测试）

---

## 📚 参考来源

本项目题目基于以下权威资源设计：

- **[OWASP Top 10:2025](https://owasp.org/Top10/2025/)** — OWASP 基金会发布的 2025 年十大 Web 安全风险官方列表
- **[OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)** — Web 安全测试指南
- **[PortSwigger Web Security Academy](https://portswigger.net/web-security)** — Web 安全学习资源
- **[CTFHub](https://www.ctfhub.com/)** — CTF 技能树与题目参考
- **[CTFwiki](https://ctf-wiki.org/)** — CTF 竞赛知识库

> ⚠️ **注意**：本项目中的 OWASP 编号（如 A01、A02 等）严格遵循 OWASP Top 10:2025 官方分类。原 2021 版中的部分类别在 2025 版中已合并或调整。

---

## 🤖 生成式人工智能使用说明

本项目的部分文档（包括但不限于根目录 `README.md`、题目描述优化、解题思路整理等）在编写过程中使用了生成式人工智能工具（如 Kimi、GPT 系列等）进行辅助：

- **AI 辅助范围**：文档结构优化、语言表达润色、格式规范化、翻译辅助。
- **人工审核**：所有安全相关的技术内容、漏洞设计、源码实现均由人工编写和审核，确保技术准确性。
- **免责声明**：AI 生成的内容仅供参考，实际漏洞利用和修复方案需结合具体环境进行验证。

如果您发现任何由 AI 辅助产生的不准确之处，欢迎提交 Issue 或 Pull Request 进行修正。

---

## 📜 许可协议

本项目采用 [MIT 许可证](LICENSE) 开源。

```text
MIT License

Copyright (c) 2026 ProbiusOfficial

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> ⚠️ 尽管代码以 MIT 协议开源，但题目中的漏洞均为**故意设计**，仅供安全学习用途。请勿将相关技术用于未经授权的系统测试。

---

## ⚠️ 安全声明

本题目集仅供安全学习、CTF 竞赛和渗透测试培训使用。所有漏洞均为故意设计，请勿用于非法用途。

使用本项目时，请确保：
- 仅在授权环境下运行题目容器
- 遵守当地法律法规
- 不对任何第三方系统使用题目中涉及的技术手段

---

<p align="center">
  基于 <a href="https://owasp.org/Top10/2025/">OWASP Top 10:2025</a> 官方内容命制<br>
  Made with ❤️ for the CTF & Security Community
</p>
