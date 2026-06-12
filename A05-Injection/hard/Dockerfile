FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/

RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask

EXPOSE 80

CMD sh -c 'if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"; \
    elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"; \
    elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"; \
    else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"; fi && \
    echo "$INSERT_FLAG" > /flag && chmod 644 /flag && \
    python /app/app.py'
