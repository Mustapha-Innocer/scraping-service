import logging

LOGGER = logging.getLogger(__name__)

# Configure logging
LOGGER.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: <%(filename)s> %(message)s"
)

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)

# Add handlers to the logger
LOGGER.addHandler(ch)
