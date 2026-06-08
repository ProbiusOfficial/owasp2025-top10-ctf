FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN { \
    echo '#!/bin/sh'; \
    echo 'if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"'; \
    echo 'elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"'; \
    echo 'elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"'; \
    echo 'else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"'; \
    echo 'fi'; \
    echo 'echo "$INSERT_FLAG" > /flag'; \
    echo 'python /app/app.py'; \
} > /start.sh && chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
