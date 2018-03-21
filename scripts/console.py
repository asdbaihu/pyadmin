# coding=utf-8

# source: https://www.smartfile.com/blog/what-is-good-logging-in-python/
import logging

# create the logging instance for logging to file only
logger = logging.getLogger('SmartfileTest')

# create the handler for the main logger
file_logger = logging.FileHandler('smartfile_test.log')
NEW_FORMAT = '[%(asctime)s - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
logger.addHandler(file_logger)

# remember that by default, logging will start at 'warning' unless
# we set it manually
logger.setLevel(logging.DEBUG)

# log some stuff!
logger.debug("This is a debug message!")
logger.info("This is an info message!")
logger.warning("This is a warning message!")

