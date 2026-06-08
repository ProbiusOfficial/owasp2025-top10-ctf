const express = require('express');
const bodyParser = require('body-parser');
const _ = require('lodash');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());

// 模拟用户会话中间件
app.use((req, res, next) => {
    req.user = {};
    next();
});

// 首页
app.get('/', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>User Config Center</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f8f9fa; }
        h1 { color: #333; }
        .box { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        code { background: #eee; padding: 2px 6px; border-radius: 4px; }
        pre { background: #272822; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { padding: 10px 20px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🛠️ User Config Center</h1>
    <div class="box">
        <h3>API 文档</h3>
        <p><b>POST /api/update</b> — 更新用户配置（JSON格式）</p>
        <p>请求体示例：</p>
        <pre>{"theme": "dark", "language": "zh"}</pre>
        <p>系统会将你的配置与默认配置深度合并。</p>
    </div>
    <div class="box">
        <h3>测试接口</h3>
        <p><b>GET /admin/flag</b> — 管理员区域（需要 isAdmin 权限）</p>
    </div>
    <div class="box">
        <h3>在线测试</h3>
        <textarea id="jsonInput" rows="6" placeholder='{"theme":"dark"}'>{"theme":"dark"}</textarea><br>
        <button onclick="updateConfig()">提交配置</button>
        <pre id="result"></pre>
    </div>
    <script>
        async function updateConfig() {
            try {
                const data = JSON.parse(document.getElementById('jsonInput').value);
                const res = await fetch('/api/update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const text = await res.text();
                document.getElementById('result').textContent = text;
            } catch(e) {
                document.getElementById('result').textContent = 'Error: ' + e.message;
            }
        }
    </script>
</body>
</html>
    `);
});

// 配置更新接口 — 存在原型污染漏洞
app.post('/api/update', (req, res) => {
    const defaultConfig = { theme: 'light', language: 'en' };
    const userConfig = req.body;

    // 使用 lodash.merge 合并配置 — 存在原型污染漏洞 (CVE-2019-10744 之前版本)
    const merged = _.merge({}, defaultConfig, userConfig);

    res.json({
        message: 'Config updated successfully',
        config: merged
    });
});

// 管理员区域 — 检查 isAdmin
app.get('/admin/flag', (req, res) => {
    // 从原型链中查找 isAdmin（如果被污染，Object.prototype.isAdmin 将为 true）
    if (req.user.isAdmin) {
        const flag = fs.readFileSync('/flag', 'utf8').trim();
        res.json({ success: true, flag: flag });
    } else {
        res.status(403).json({ success: false, message: 'Forbidden: Admin only' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`A08 Easy app listening on port ${PORT}`);
});
