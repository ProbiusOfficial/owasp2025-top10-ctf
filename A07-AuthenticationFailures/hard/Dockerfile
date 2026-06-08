FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

# FLAG注入
RUN echo '#!/bin/sh\n\
if [ "$DASFLAG" ]; then INSERT_FLAG="$DASFLAG"\n\
elif [ "$FLAG" ]; then INSERT_FLAG="$FLAG"\n\
elif [ "$GZCTF_FLAG" ]; then INSERT_FLAG="$GZCTF_FLAG"\n\
else INSERT_FLAG="flag{TEST_Dynamic_FLAG}"\n\
fi\n\
echo "$INSERT_FLAG" > /flag\n\
chmod 644 /flag\n\
python /app/app.py\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/entrypoint.sh"]
