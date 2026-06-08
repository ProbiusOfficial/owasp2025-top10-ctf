import os
import re
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 黑名单过滤
BLACKLIST_CHARS = r'[;&|$(`)\'"\\]'


def sanitize_input(user_input):
    """过滤危险字符，尝试防止命令注入"""
    return re.sub(BLACKLIST_CHARS, '', user_input)


@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>网络连通性测试</title></head>
<body>
    <h1>网络连通性测试工具</h1>
    <p>输入IP地址或域名，测试网络连通性。</p>
    <form action="/ping" method="post">
        <input type="text" name="ip" placeholder="例如: 127.0.0.1">
        <button type="submit">Ping测试</button>
    </form>
    <hr>
    <p>注意：系统已启用安全防护，禁止输入特殊字符。</p>
</body>
</html>
''')


@app.route("/ping", methods=["POST"])
def ping():
    ip = request.form.get("ip", "")
    sanitized = sanitize_input(ip)

    if not sanitized:
        return "<h2>错误</h2><p>无效的输入</p><br><a href='/'>返回</a>", 400

    try:
        cmd = f"ping -c 1 {sanitized}"
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        output = result.decode('utf-8', errors='replace')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8', errors='replace') if e.output else str(e)
    except Exception as e:
        output = str(e)

    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Ping结果</title></head>
<body>
    <h1>Ping测试结果</h1>
    <p>执行的命令: <code>{{ cmd }}</code></p>
    <pre>{{ output }}</pre>
    <hr>
    <a href="/">返回</a>
</body>
</html>
''', cmd=cmd, output=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
