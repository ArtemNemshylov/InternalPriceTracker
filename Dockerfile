FROM mcr.microsoft.com/playwright:v1.50.0-noble

# Встановлюємо Python і pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Робоча директорія
WORKDIR /app

# Копіюємо проєкт
COPY . .

# Встановлюємо Python-залежності
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]
