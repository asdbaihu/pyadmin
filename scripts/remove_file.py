# coding=utf-8
# version 1

import logging,os, time,sys,psycopg2
from datetime import datetime,timedelta

logger = logging.getLogger('SmartfileTest')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('SmartfileTest').addHandler(console)
file_logger = logging.FileHandler('/usr/local/www/apache24/data/runtime.log',mode='w')
NEW_FORMAT = '[%(asctime)s] = [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)
file_logger.setFormatter(file_logger_format)
logger.addHandler(file_logger)
logger.setLevel(logging.DEBUG)


# logging.basicConfig(level=logging.DEBUG,
#                     filename='/var/www/wsgi-scripts/pyadmin/scripts/runtime.log',
#                     filemode='w',
#                     format='%(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

# log some stuff!
logger.debug("This is a debug message!")
logger.info("This is an info message!")
logger.warning("This is a warning message")

import os, time

path_data = "/usr/local/www/apache24/data"
path_data_data = "/usr/local/www/apache24/data/data"
path_disagreement_without_image = "/usr/local/www/apache24/data/disagreement_without_image"
path_excel_without_images = "/usr/local/www/apache24/data/excel_without_images"
path_images = "/usr/local/www/apache24/data/images"

def flushdir(dir):
    now = time.time()
    fs = iter(os.listdir(dir))
    while True:
        try:
            f = fs.__next__()
            fullpath = os.path.join(dir,f)
            if os.stat(fullpath).st_mtime < (now - 2*86400):
                if os.path.isfile(fullpath):
                    os.remove(fullpath)
                elif os.path.isdir(fullpath):
                    flushdir(fullpath)
        except StopIteration:
            break

flushdir(path_data)
flushdir(path_data_data)
flushdir(path_disagreement_without_image)
flushdir(path_excel_without_images)
flushdir(path_images)

# drop table

def getConnection():
    conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
    return conn

day_expire = datetime.today() - timedelta(days=2)


conn = getConnection()
cur = conn.cursor()
cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%_20%'")
tables = iter(cur.fetchall())
conn.commit()
cur.close()
conn.close()
import re


while True:
    try:
        table = tables.__next__()[0]
        str_day= "-".join(table.split("_")[-3:])
        day = datetime.strptime(str_day,'%Y-%m-%d')
        if day < datetime.today()-timedelta(days=2):
            conn = getConnection()
            cur = conn.cursor()
            cur.execute(f"drop table {table}")
            conn.commit()
            cur.close()
            conn.close()
    except StopIteration:
        break

logger.info("Done!")
