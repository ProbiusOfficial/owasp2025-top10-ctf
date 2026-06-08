FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./

# FLAG注入脚本 + 双服务启动
RUN echo '#!/bin/sh\n\
if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"\n\
elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"\n\
elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"\n\
else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"\n\
fi\n\
echo "$INSERT_FLAG" > /flag\n\
python /app/flag_service.py &\n\
sleep 1\n\
python /app/app.py' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 80

CMD ["/app/start.sh"]
