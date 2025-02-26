import logging
import os
from pathlib import Path

app_config_dir = os.path.join(os.path.dirname(__file__),'..','config')

def configure_logging():

    print("Start of logging configuration")
    logging.config.fileConfig(Path(app_config_dir,'logging.ini'), disable_existing_loggers=True)
    logger = logging.getLogger(__name__)

    logger.info(f"Logger configured was: {logging.getLogger().handlers}")
    return logger
