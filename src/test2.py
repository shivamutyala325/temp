from logger import get_logger
from exception import CustomException
import sys
logger=get_logger("test2")
x=3
y='a'
try:
    print(x+y)
except Exception as e:
    logger.error(e)
    raise CustomException(e,sys)