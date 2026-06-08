FROM node:18-slim

# 安装必要的工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY src/package.json .
RUN npm install

# 复制应用源码
COPY src/ .

# FLAG 注入脚本
RUN echo '#!/bin/sh\n\
if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"\n\
elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"\n\
elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"\n\
else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"\n\
fi\n\
echo "$INSERT_FLAG" > /flag\n\
chmod 644 /flag\n\
exec node app.js' > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 80

ENV PORT=80

ENTRYPOINT ["/entrypoint.sh"]
