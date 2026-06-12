FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/

RUN pip install --no-cache-dir flask lxml

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
