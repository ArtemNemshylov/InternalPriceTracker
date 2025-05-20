FROM mcr.microsoft.com/playwright/python:v1.43.0

# Робоча директорія
WORKDIR /app

# Копіюємо код
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Інсталюємо браузери
RUN playwright install

# 👉 ЗАМІНИ це, якщо запускаєш streamlit замість fastapi
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]
