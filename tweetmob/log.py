import os
import logging
from tweetmob.config    import get_config_value

# Fixes Database Absolute Location
FILE_CWD = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_CWD)

LOG_FILE = get_config_value('log_file') or (FILE_DIR+'/tweetmob.log')

logging.basicConfig(
    format='%(message)s',
    filename=LOG_FILE,
    level=logging.INFO
)

log = lambda msg: logging.info(msg)