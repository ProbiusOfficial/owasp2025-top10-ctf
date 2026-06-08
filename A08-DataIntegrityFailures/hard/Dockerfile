FROM php:7.3-fpm-alpine

# 安装 nginx
RUN apk add --update --no-cache nginx

# 复制 nginx 配置文件
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# 复制 web 项目源码
COPY src /var/www/html
RUN chown -R www-data:www-data /var/www/html

# 复制入口脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 设置工作目录
WORKDIR /var/www/html

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
