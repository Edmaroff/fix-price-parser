FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libffi-dev \
       libssl-dev \
       libxml2-dev \
       libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска по умолчанию для контейнера
CMD ["scrapy", "crawl", "fix_price"]