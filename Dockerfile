FROM python:3.12-slim

# Встановлюємо системні залежності для Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    libgbm1 \
    libx11-xcb1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо проект
COPY . .

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Встановлюємо Playwright браузери
RUN playwright install --with-deps

# Відкриваємо порт FastAPI
EXPOSE 8000

# Запуск FastAPI застосунку через src.main:app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
