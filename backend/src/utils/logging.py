"""Logging configuration"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", format: Optional[str] = None) -> None:
    """Setup logging configuration"""
    if format is None:
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)