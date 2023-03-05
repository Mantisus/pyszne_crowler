from pathlib import Path

from loguru import logger

LOG_FOLDER = Path(Path(__file__).parents[1], "log")

logger.add(
    Path(LOG_FOLDER, "pyszne_{time}.log"),
    format="{time} {level} {message}",
    retention="10 days",
    rotation="1 day",
    level="INFO",
    enqueue=True,
)
