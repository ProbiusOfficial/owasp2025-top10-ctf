#!/bin/sh
# 通用FLAG注入脚本 - 参考靶机参考文件夹的docker-entrypoint.sh
# 支持 DASFLAG / FLAG / GZCTF_FLAG 环境变量

if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

# 默认将flag写入 /flag 文件（可被题目源码读取）
echo "$INSERT_FLAG" > /flag
chmod 644 /flag

# 如果题目需要数据库中的flag，可在各题目的entrypoint中自行扩展
# 例如：sqlite3 /app/db.sqlite "INSERT INTO flags VALUES ('flag','$INSERT_FLAG');"
