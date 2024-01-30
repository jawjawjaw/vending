from logging import getLogger
import logging

from app.core.config import settings


logging.basicConfig(
    level=settings.LOGLEVEL,  # Set the desired log level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

log = getLogger(__name__)
