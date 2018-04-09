# coding=utf-8
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='/var/www/wsgi-scripts/pyadmin/scripts/runtime.log',
                    filemode='w',
                    format='%(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

# log some stuff!
logging.debug("This is a debug message!")
logging.info("This is an info message!")
logging.warning("This is a warning message")
