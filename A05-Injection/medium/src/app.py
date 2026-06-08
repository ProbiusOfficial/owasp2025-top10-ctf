import os
import re
from flask import Flask, request, render_template_string

app = Flask(__name__)

BLACKLIST = ["__", "class", "base", "mro"]


def waf_check(text):
    """简单的WAF过滤，禁止包含黑名单关键字的输入"""
    for bad in BLACKLIST:
        if bad in text.lower():
            return False, bad
    return True, None


@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>邮件模板生成器</title></head>
<body>
    <h1>邮件模板生成器</h1>
    <p>输入Jinja2模板，系统将为您生成邮件内容。</p>
    <form action="/generate" method="post">
        <p>收件人姓名: <input type="text" name="name" value="CTFer"></p>
        <p>模板内容:</p>
        <textarea name="template" rows="10" cols="60">
亲爱的 {{ name }}，

欢迎参加本次CTF竞赛！

祝您比赛顺利！
        </textarea><br>
        <button type="submit">生成邮件</button>
    </form>
    <hr>
    <p>提示：模板使用Jinja2语法，支持 <code>{{ name }}</code> 等变量。</p>
</body>
</html>
''')


@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name", "CTFer")
    template = request.form.get("template", "")

    ok, bad = waf_check(template)
    if not ok:
        return f"<h2>安全检查失败</h2><p>检测到危险关键字: <code>{bad}</code></p><br><a href='/'>返回</a>", 403

    try:
        result = render_template_string(template, name=name)
    except Exception as e:
        return f"<h2>模板渲染错误</h2><pre>{str(e)}</pre><br><a href='/'>返回</a>"

    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>生成结果</title></head>
<body>
    <h1>生成结果</h1>
    <pre>{{ result }}</pre>
    <hr>
    <a href="/">返回</a>
</body>
</html>
''', result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
