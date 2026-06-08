<?php
error_reporting(0);

class FileReader {
    public $file = "/etc/hostname";
    public function __toString() {
        return file_get_contents($this->file);
    }
}

class Logger {
    public $msg = "log initialized";
    public function __destruct() {
        echo $this->msg;
    }
}

class Config {
    public $settings = [];
    public function __construct() {
        $this->settings = ['theme' => 'light'];
    }
}

$action = $_GET['action'] ?? 'home';

if ($action === 'api') {
    header('Content-Type: application/json');
    $data = $_POST['data'] ?? '';
    if (empty($data)) {
        echo json_encode(['error' => 'missing data']);
        exit;
    }
    // ⚠️ 不安全的反序列化
    $obj = unserialize($data);
    echo json_encode([
        'message' => 'Object deserialized successfully',
        'type' => get_class($obj)
    ]);
    exit;
}
?>
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Secure Config Manager</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f8f9fa; }
        h1 { color: #333; }
        .box { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        code { background: #eee; padding: 2px 6px; border-radius: 4px; }
        pre { background: #272822; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; }
        textarea { width: 100%; padding: 10px; box-sizing: border-box; font-family: monospace; }
        button { padding: 10px 20px; margin-top: 10px; cursor: pointer; }
        .hint { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <h1>🔧 Secure Config Manager</h1>
    <div class="box">
        <h3>关于本系统</h3>
        <p>本系统提供配置对象的序列化与反序列化服务，使用 PHP 原生序列化格式。</p>
        <p class="hint">系统包含以下内置类：FileReader、Logger、Config</p>
    </div>
    <div class="box">
        <h3>反序列化测试</h3>
        <p class="hint">提交序列化数据，系统将反序列化对象并返回类型信息。</p>
        <form method="POST" action="/?action=api">
            <textarea name="data" rows="6" placeholder="输入序列化字符串...">O:6:"Config":1:{s:8:"settings";a:1:{s:5:"theme";s:4:"dark";}}</textarea><br>
            <button type="submit">提交</button>
        </form>
    </div>
    <div class="box">
        <h3>API 文档</h3>
        <p><b>POST /?action=api</b></p>
        <p>参数：<code>data</code> — PHP 序列化字符串</p>
        <p>系统会将数据反序列化并返回对象类型。</p>
    </div>
    <div class="box">
        <h3>源码片段</h3>
        <pre>$obj = unserialize($data);
echo get_class($obj);</pre>
    </div>
</body>
</html>
