import logging
import os
from datetime import datetime

log_dir_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_dir_path,exist_ok=True)


log_filename=f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_filpath=os.path.join(log_dir_path,log_filename)


logging.basicConfig(
    filename=log_filpath,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
                    )

