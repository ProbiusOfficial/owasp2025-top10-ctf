#!/bin/sh

# FLAG 注入
if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

echo "$INSERT_FLAG" > /flag
chmod 644 /flag

# 启动 php-fpm
php-fpm &

# 启动 nginx（前台运行以保持容器活跃）
nginx -g 'daemon off;'
