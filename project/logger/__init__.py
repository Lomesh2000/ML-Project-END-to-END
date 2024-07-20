import logging
import os
from datetime import datetime
from project.utils.folder_paths import create_logs_dir

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

log_dir = 'logs'
logs_path = os.path.join(os.curdir, log_dir, LOG_FILE)
create_logs_dir(log_dir=log_dir)
print(logs_path)
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.DEBUG
) 



