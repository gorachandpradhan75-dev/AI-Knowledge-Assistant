"""
Centralized logging configuration using loguru.

Provides structured, rotated file logs plus readable console output.
Import `logger` anywhere in the app instead of `logging.getLogger`.
"""
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)

    logger.remove()  # remove default handler

    # Console sink — human readable
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # File sink — rotated, retained, JSON-free but structured
    logger.add(
        f"{settings.LOG_DIR}/app.log",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        backtrace=True,
        diagnose=False,
        enqueue=True,
    )

    # Separate sink purely for errors, useful for alerting pipelines
    logger.add(
        f"{settings.LOG_DIR}/errors.log",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
    )


__all__ = ["logger", "configure_logging"]