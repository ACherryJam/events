import logging
from .log import configure_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

configure_logger(logger)
