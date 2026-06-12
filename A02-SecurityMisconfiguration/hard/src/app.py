from flask import Flask, request, render_template_string, jsonify
from lxml import etree as ET
import io
import os

app = Flask(__name__)

INDEX_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>XML解析服务 - 星辰数据处理中心</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: #8e44ad; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .form-box { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .result { background: #2c3e50; color: #2ecc71; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }
        .hint { background: #e8f4fd; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 20px; }
        textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; }
        button { background: #8e44ad; color: white; padding: 10px 30px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #732d91; }
        .sample { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; }
        code { background: #eee; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>星辰数据处理中心</h1>
        <p>企业级 XML 数据解析与转换服务</p>
    </div>
    <div class="hint">
        <strong>使用说明：</strong>上传XML文件或直接粘贴XML内容，系统将解析并返回结构化数据。
        <br>支持标准 XML 1.0 格式，兼容多种编码。
    </div>
    <div class="form-box">
        <h3>XML解析</h3>
        <form method="POST" action="/parse" enctype="multipart/form-data">
            <p><strong>方式一：文件上传</strong></p>
            <input type="file" name="xmlfile" accept=".xml,.txt">
            <p><strong>方式二：直接输入</strong></p>
            <textarea name="xmltext" rows="10" placeholder="在此粘贴XML内容..."><?xml version="1.0"?>
<user>
    <name>张三</name>
    <email>zhangsan@xingchen.com</email>
</user></textarea>
            <br><br>
            <button type="submit">开始解析</button>
        </form>
    </div>
    <div class="form-box">
        <h3>示例格式</h3>
        <div class="sample">
<code>&lt;?xml version="1.0"?&gt;
&lt;company&gt;
    &lt;name&gt;星辰科技&lt;/name&gt;
    &lt;employees&gt;
        &lt;employee&gt;
            &lt;name&gt;张三&lt;/name&gt;
            &lt;department&gt;研发部&lt;/department&gt;
        &lt;/employee&gt;
    &lt;/employees&gt;
&lt;/company&gt;</code>
        </div>
    </div>
    <div class="form-box">
        <h3>高级功能</h3>
        <p>支持 UTF-8、UTF-16、ISO-8859-1 等多种编码格式。</p>
        <p>UTF-16编码示例：将XML内容保存为UTF-16编码后上传，系统可自动识别并解析。</p>
    </div>
</body>
</html>
'''

RESULT_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>解析结果 - 星辰数据处理中心</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: #8e44ad; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .result-box { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .xml-output { background: #2c3e50; color: #2ecc71; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; }
        .nav { margin-top: 20px; }
        .nav a { color: #8e44ad; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>解析结果</h1>
    </div>
    <div class="result-box">
        {% if error %}
        <div class="error">
            <strong>解析错误：</strong><br>{{ error }}
        </div>
        {% else %}
        <h3>解析后的内容：</h3>
        <div class="xml-output">{{ result }}</div>
        <h3>标签结构：</h3>
        <div class="xml-output">{{ tags }}</div>
        {% endif %}
    </div>
    <div class="nav">
        <a href="/">&larr; 返回首页</a>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_PAGE)

@app.route('/parse', methods=['POST'])
def parse_xml():
    xml_data = None
    
    # 从文件或文本框获取XML
    if 'xmlfile' in request.files and request.files['xmlfile'].filename:
        file = request.files['xmlfile']
        xml_data = file.read()
    elif request.form.get('xmltext'):
        xml_data = request.form.get('xmltext').encode('utf-8')
    
    if not xml_data:
        return render_template_string(RESULT_PAGE, error="请提供XML内容或上传文件", result=None, tags=None)
    
    try:
        # 尝试检测并处理UTF-16编码
        if xml_data.startswith(b'\xff\xfe') or xml_data.startswith(b'\xfe\xff'):
            # UTF-16 BOM detected
            xml_text = xml_data.decode('utf-16')
        else:
            try:
                xml_text = xml_data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    xml_text = xml_data.decode('utf-16')
                except:
                    xml_text = xml_data.decode('utf-8', errors='replace')
        
        # 使用 lxml 解析并允许解析外部实体，以模拟存在安全 misconfiguration 的解析器
        parser = ET.XMLParser(resolve_entities=True, no_network=False)
        tree = ET.parse(io.StringIO(xml_text), parser)
        root = tree.getroot()
        
        # 提取文本内容
        result_text = ""
        def extract_text(elem, depth=0):
            nonlocal result_text
            indent = "  " * depth
            if elem.text and elem.text.strip():
                result_text += f"{indent}[{elem.tag}] {elem.text.strip()}\n"
            for child in elem:
                extract_text(child, depth + 1)
                if child.tail and child.tail.strip():
                    result_text += f"{indent}  {child.tail.strip()}\n"
        
        extract_text(root)
        
        # 提取标签结构
        def extract_tags(elem, depth=0):
            indent = "  " * depth
            tag_info = f"{indent}<{elem.tag}>"
            if list(elem):
                tag_info += "\n" + "\n".join([extract_tags(child, depth + 1) for child in elem])
                tag_info += f"\n{indent}</{elem.tag}>"
            else:
                tag_info += f"</{elem.tag}>"
            return tag_info
        
        tags_info = extract_tags(root)
        
        if not result_text.strip():
            result_text = "（标签内容为空或仅包含子标签）"
        
        return render_template_string(RESULT_PAGE, error=None, result=result_text, tags=tags_info)
        
    except ET.ParseError as e:
        return render_template_string(RESULT_PAGE, error=f"XML解析错误: {str(e)}", result=None, tags=None)
    except Exception as e:
        return render_template_string(RESULT_PAGE, error=f"处理错误: {str(e)}", result=None, tags=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
