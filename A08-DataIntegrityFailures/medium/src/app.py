import pickle
import base64
import os
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)

# 确保 static 目录存在
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Data Serializer</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f8f9fa; }
        h1 { color: #333; }
        .box { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        textarea { width: 100%; padding: 10px; box-sizing: border-box; font-family: monospace; }
        button { padding: 10px 20px; margin-top: 10px; cursor: pointer; }
        pre { background: #272822; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; }
        .hint { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <h1>🗃️ Data Serializer</h1>
    <div class="box">
        <h3>序列化 / 反序列化服务</h3>
        <p class="hint">提交 Base64 编码的序列化数据，系统将为你反序列化并展示对象信息。</p>
        <form method="POST" action="/deserialize">
            <textarea name="data" rows="8" placeholder="请输入 Base64 编码的序列化数据...">{{ default_payload }}</textarea><br>
            <button type="submit">反序列化</button>
        </form>
    </div>
    {% if result %}
    <div class="box">
        <h3>结果</h3>
        <pre>{{ result }}</pre>
    </div>
    {% endif %}
    <div class="box">
        <h3>API 文档</h3>
        <p><b>POST /deserialize</b></p>
        <p>参数：<code>data</code> — Base64 编码的 Python pickle 序列化数据</p>
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    # 提供一个默认的合法 payload 示例
    sample = pickle.dumps({"message": "Hello, CTF!"})
    default_payload = base64.b64encode(sample).decode()
    return render_template_string(HTML_TEMPLATE, default_payload=default_payload, result=None)


@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.form.get('data', '')
    result = None
    try:
        # ⚠️ 存在反序列化漏洞：直接反序列化用户输入
        obj = pickle.loads(base64.b64decode(data))
        result = f"反序列化成功！对象类型: {type(obj).__name__}\n对象内容: {repr(obj)}"
    except Exception as e:
        result = f"反序列化失败: {str(e)}"

    sample = pickle.dumps({"message": "Hello, CTF!"})
    default_payload = base64.b64encode(sample).decode()
    return render_template_string(HTML_TEMPLATE, default_payload=default_payload, result=result)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
