# src/main.py

import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routers import router as api_router
from src.configs.logging_conf import setup_logging

# Optional: environment loader
# from src.config import settings  # если у тебя есть .env и pydantic Settings

# Инициализация логгирования
setup_logging()

# Создаем FastAPI app
def create_app() -> FastAPI:
    app = FastAPI(
        title="Parsers Service",
        description="API для запуска парсеров через messagebus.",
        version="1.0.0"
    )

    # Настройка CORS (если нужно подключение с фронта или Swagger извне)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # или конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем роуты
    app.include_router(api_router)

    return app

app = create_app()

# Запуск через `python main.py` (разработка)
if __name__ == "__main__":
    logger.info("Starting FastAPI app...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
