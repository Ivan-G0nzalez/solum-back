import logging
from logging.handlers import TimedRotatingFileHandler

from .config_utils import GlobalConfig
from .os_utils import create_folder_if_not_exists, get_full_filename


create_folder_if_not_exists(GlobalConfig.get_log_path())
filename = get_full_filename(GlobalConfig.get_log_path(), GlobalConfig.get_log_filename())

logHandler = TimedRotatingFileHandler(filename, when="midnight", delay=True)
logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logHandler.setFormatter(logFormatter)
logger = logging.getLogger("uvicorn")
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
