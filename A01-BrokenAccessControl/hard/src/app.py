from flask import Flask, request, render_template_string, jsonify
import requests
import urllib.parse
import os
import re

app = Flask(__name__)

FLAG = open("/flag", "r").read().strip() if os.path.exists("/flag") else "flag{TEST_Dynamic_FLAG}"

# SSRF 黑名单过滤
BLACKLIST = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "::1",
    "127.0.0",
    "127.1",
]

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>图片获取服务</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .input-box { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px; }
        input { padding: 10px; width: 500px; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .result { margin-top: 20px; padding: 20px; background: #e8f4e8; border-radius: 8px; }
        .error { background: #f8d7da; color: #721c24; }
        .hint { color: #666; font-size: 0.9em; margin-top: 20px; }
        img { max-width: 100%; margin-top: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>🖼️ 在线图片获取服务</h1>
    <p>输入图片URL，我们会帮您获取并展示图片内容。</p>
    <div class="input-box">
        <input type="text" id="url" placeholder="http://example.com/image.jpg" value="http://example.com/image.jpg"><br><br>
        <button onclick="fetchImage()">获取图片</button>
    </div>
    <div class="hint">
        <p>提示：支持 HTTP/HTTPS 协议的图片链接。</p>
        <p>出于安全考虑，以下地址已被禁止访问：127.0.0.1, localhost, 0.0.0.0</p>
    </div>
    <div id="result"></div>
    <script>
        function fetchImage() {
            let url = document.getElementById('url').value;
            fetch('/fetch', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            }).then(r => r.json()).then(data => {
                let div = document.getElementById('result');
                if (data.error) {
                    div.className = 'result error';
                    div.innerHTML = '<p>❌ ' + data.error + '</p>';
                } else if (data.image) {
                    div.className = 'result';
                    div.innerHTML = '<p>✅ 获取成功！</p><img src="data:image/png;base64,' + data.image + '">';
                } else if (data.text) {
                    div.className = 'result';
                    div.innerHTML = '<p>✅ 获取成功（文本内容）：</p><pre>' + data.text + '</pre>';
                }
            });
        }
    </script>
</body>
</html>
"""


def is_blocked(url):
    """检查URL是否命中黑名单"""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    for blocked in BLACKLIST:
        if blocked.lower() in hostname.lower():
            return True
    return False


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/fetch", methods=["POST"])
def fetch_image():
    data = request.get_json()
    url = data.get("url", "")

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "仅支持 HTTP/HTTPS 协议"}), 400

    # 黑名单过滤（可被绕过）
    if is_blocked(url):
        return jsonify({"error": "禁止访问内网地址"}), 403

    try:
        resp = requests.get(url, timeout=5, allow_redirects=True)
        content = resp.content

        # 如果是图片，返回base64
        content_type = resp.headers.get("Content-Type", "")
        if "image" in content_type:
            import base64
            b64 = base64.b64encode(content).decode()
            return jsonify({"image": b64})
        else:
            # 返回文本内容
            text = content.decode("utf-8", errors="replace")
            return jsonify({"text": text[:2000]})

    except requests.exceptions.ConnectionError as e:
        return jsonify({"error": f"连接失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"请求失败: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
