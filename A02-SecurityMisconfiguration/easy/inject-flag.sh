#!/bin/sh

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

echo "$INSERT_FLAG" > /flag
chmod 644 /flag

# 将 flag 植入 Git 历史中的 config.php
cd /app/static

git config user.email "dev@xingchen-tech.com"
git config user.name "DevOps Team"
git config advice.detachedHead false

OLD_COMMIT=$(git rev-list --max-parents=0 HEAD)

git checkout -f "$OLD_COMMIT"
sed -i "s|__PLACEHOLDER_FLAG__|$INSERT_FLAG|g" config.php
git add config.php
git commit --amend --no-edit

NEW_COMMIT=$(git rev-parse HEAD)

git checkout -f master
export GIT_EDITOR=true
git rebase --onto "$NEW_COMMIT" "$OLD_COMMIT" master || {
    git rm -f config.php || true
    git rebase --continue
}

git config --global --add safe.directory /app/static
git update-server-info

chmod -R 755 .git
