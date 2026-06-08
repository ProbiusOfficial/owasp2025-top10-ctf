FROM python:3.11-slim

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制应用代码
COPY src/ /app/

# 安装Python依赖
RUN pip install --no-cache-dir flask

# 构建 .git 目录（模拟部署时忘记删除）
RUN chmod +x /app/setup_git.sh && /app/setup_git.sh

# 复制启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
