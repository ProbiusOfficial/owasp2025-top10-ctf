#!/bin/sh
set -e

# 支持 GZCTF / DAS 注入的 flag 环境变量
if [ -n "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
elif [ -n "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
elif [ -n "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

# 写入 /flag（兼容部分解法的直接读取）
echo "$INSERT_FLAG" > /flag
chmod 644 /flag

# 将 flag 植入 Git 历史中的 config.php
cd /app/static

# 配置 git 身份，避免 amend/rebase 失败
git config user.email "dev@xingchen-tech.com"
git config user.name "DevOps Team"
git config advice.detachedHead false

# setup_git.sh 生成的历史：
#   HEAD~2 (root): feat: 添加生产环境配置文件  <-- config.php 含 __PLACEHOLDER_FLAG__
#   HEAD~1:        security: 移除敏感配置文件
#   HEAD:          docs: 添加项目说明文档
OLD_COMMIT=$(git rev-list --max-parents=0 HEAD)

# 切到第一个提交，替换占位符，amend 提交
git checkout -f "$OLD_COMMIT"
sed -i "s|__PLACEHOLDER_FLAG__|$INSERT_FLAG|g" config.php
git add config.php
git commit --amend --no-edit

NEW_COMMIT=$(git rev-parse HEAD)

# 回到 master，把后续提交 rebase 到修改后的根提交上
git checkout -f master
export GIT_EDITOR=true
git rebase --onto "$NEW_COMMIT" "$OLD_COMMIT" master || {
    # 解决 modify/delete 冲突：保留删除操作（config.php 在后续提交中被移除）
    git rm -f config.php || true
    git rebase --continue
}

# 生成 dumb HTTP 克隆所需的索引
git config --global --add safe.directory /app/static
git update-server-info

# 确保 .git 可被 Web 访问
chmod -R 755 .git

cd /app
exec python /app/app.py
