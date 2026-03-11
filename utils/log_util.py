"""Logging utilities for example scripts."""

from __future__ import annotations

import logging
import os
import re
import sys
from logging import handlers
from pathlib import Path


ROOT_PATH = Path.cwd()
LOG_DIR = ROOT_PATH / "logs" / os.environ.get("LOG_NAME", "default")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "service"
LOG_LEVEL = os.environ.get("SERVICE_LOG_LEVEL", "INFO").upper()

DEFAULT_FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
)


def _build_stream_handler() -> logging.Handler:
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(DEFAULT_FORMATTER)
    return handler


def _build_file_handler() -> logging.Handler:
    handler = handlers.TimedRotatingFileHandler(
        filename=LOG_PATH,
        when="MIDNIGHT",
        interval=1,
        backupCount=10,
        encoding="utf-8",
    )
    handler.suffix = "%Y-%m-%d.log"
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}\.log$")
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(DEFAULT_FORMATTER)
    return handler


logger = logging.getLogger("orproj")
logger.setLevel(LOG_LEVEL)
logger.propagate = False

if not logger.handlers:
    logger.addHandler(_build_stream_handler())
    logger.addHandler(_build_file_handler())


def main() -> None:
    logger.info("log util ready")


if __name__ == "__main__":
    main()
