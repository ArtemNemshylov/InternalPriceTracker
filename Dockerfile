FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn
CMD ["python", "-c", "import fastapi; print('✅ FastAPI OK')"]
