#!/bin/sh
set -e

cd /app/static

git init
git config user.email "dev@xingchen-tech.com"
git config user.name "DevOps Team"

cat > config.php << 'EOF'
<?php
// 数据库配置 - 生产环境
$db_host = 'localhost';
$db_user = 'admin';
$db_pass = 'S3cr3tP@ssw0rd_2025!';
$db_name = 'xingchen_production';
$api_key = 'sk-prod-xc-9f8d7e6c5b4a3210';
$flag = '__PLACEHOLDER_FLAG__';
?>
EOF

git add config.php
git commit -m "feat: 添加生产环境配置文件"

rm config.php
git add -A
git commit -m "security: 移除敏感配置文件，避免泄露（紧急修复）"

echo "# 星辰科技官网" > README.md
git add README.md
git commit -m "docs: 添加项目说明文档"

chmod -R 755 /app/static/.git
cd /app
