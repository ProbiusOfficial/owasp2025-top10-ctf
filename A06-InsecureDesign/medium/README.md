# 限时秒杀 (Medium)

## 题目描述

欢迎来到限时秒杀活动！珍贵的Flag商品仅剩1件。秒杀流程分为三步：检查库存、创建订单、支付订单。你能成功抢到Flag吗？

## 题目信息

- **分类**：A06 Insecure Design
- **难度**：Medium
- **端口**：80

## 访问方式

访问 `http://<target>:80` 查看秒杀页面。

## API说明

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/stock` | GET | 查询库存 |
| `/api/check-stock` | POST | 检查库存是否充足 |
| `/api/create-order` | POST | 创建订单（扣减库存） |
| `/api/pay` | POST | 支付订单，请求体 `{"order_no": "xxx"}` |
