FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

# FLAG注入脚本
RUN printf '%s\n' '#!/bin/sh' \
    'if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"' \
    'elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"' \
    'elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"' \
    'else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"' \
    'fi' \
    'echo "$INSERT_FLAG" > /flag' \
    'chmod 644 /flag' \
    'python /app/app.py' \
    > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/bin/sh", "/entrypoint.sh"]
