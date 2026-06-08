FROM python:3.11-slim

# 安装必要的工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制依赖并安装
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 创建 static 目录
RUN mkdir -p /app/static

# 复制应用源码
COPY src/ .

# FLAG 注入脚本 + 启动应用
RUN echo '#!/bin/sh\n\
if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"\n\
elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"\n\
elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"\n\
else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"\n\
fi\n\
echo "$INSERT_FLAG" > /flag\n\
chmod 644 /flag\n\
exec python app.py' > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
