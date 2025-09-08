import logging
import sys

logger = logging.getLogger("MiddleEarth")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler("logs/main.log")


# This is the format in which logs will be displayed in log file
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# assign the formatter to file_handler object
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add the handler to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

