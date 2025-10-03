import sys
from logger import get_logger
from exception import CustomException
logger=get_logger("test")


try:
    1/0
except Exception as e:
    logger.error(e)
    raise CustomException(e,sys)