# A08 Data Integrity Failures - Easy

## 题目信息

- **难度**: Easy
- **考点**: JavaScript 原型污染 (Prototype Pollution)
- **技术栈**: Node.js + Express + lodash@4.17.4

## 题目描述

欢迎来到用户配置中心！你可以通过 `POST /api/update` 接口更新你的个性化配置。系统使用深度合并来整合你的配置与默认配置。

管理员区域 `/admin/flag` 存放着珍贵的 flag，但只有管理员才能访问。

你能通过配置更新接口获取 flag 吗？

## 接口说明

### POST /api/update
更新用户配置。

**请求头**: `Content-Type: application/json`

**请求体示例**:
```json
{
  "theme": "dark",
  "language": "zh"
}
```

### GET /admin/flag
获取 flag（需要管理员权限）。

## 提示

- 系统使用了 `lodash.merge()` 进行深度合并
- 检查你的配置是否能"影响"到其他对象？

## 运行方式

```bash
docker-compose up --build
```

访问 http://localhost:8080
