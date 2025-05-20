FROM mcr.microsoft.com/playwright:v1.50.0-noble

# 🛠 Встановлюємо Python і потрібні build-залежності
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Задаємо робочу директорію
WORKDIR /app

# Копіюємо все у контейнер
COPY . .

# Переконуємось, що pip працює
RUN python3 -m pip install --upgrade pip

# Інсталюємо Python-залежності
RUN pip3 install --no-cache-dir -r requirements.txt

# ✅ Playwright вже встановлений, але підстрахуємось
RUN npx playwright install --with-deps

# Відкриваємо порт
EXPOSE 8000

# 🔥 Запуск FastAPI через uvicorn
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
