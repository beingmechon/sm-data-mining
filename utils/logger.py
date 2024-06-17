import logging
import logging.config
from config.settings import LOGGING_CONFIG_FILE

def setup_logging():
    logging.config.fileConfig(LOGGING_CONFIG_FILE)
    return logging.getLogger()
