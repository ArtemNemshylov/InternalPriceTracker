# src/main.py

import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routers import router as api_router
from src.configs.logging_conf import setup_logging


setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Parsers Service",
        description="API для запуска парсеров через messagebus.",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    logger.info("Starting FastAPI app...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
