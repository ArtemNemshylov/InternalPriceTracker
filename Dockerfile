# Базовий образ з Python
FROM python:3.12-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Встановлення Playwright
RUN pip install --no-cache-dir playwright

# Встановлення браузерів для Playwright
RUN playwright install --with-deps

# Копіювання вашого додатку в контейнер
WORKDIR /app
COPY . /app

# Відкриття порту
EXPOSE 8000

# Команда для запуску вашого додатку
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
