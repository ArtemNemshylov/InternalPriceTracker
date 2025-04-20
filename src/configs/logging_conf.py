import os
import sys
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        os.path.join(log_dir, "parser.log"),
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format=log_format,
        level="DEBUG",
        enqueue=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG, force=True)

    logger.debug("Logger initialized with asyncio support!")
