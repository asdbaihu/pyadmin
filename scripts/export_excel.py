# coding=utf-8

import pandas as pd
import psycopg2,logging
from os.path import join, dirname
import numpy as np

logging.basicConfig(
    format='%(levelname)s - %(message)s',
    level=logging.DEBUG
)

def getConnection():
    conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
    return conn

conn = getConnection()
cur = conn.cursor()
cur.execute("select id,agent,link,title,customize,variant_check,correct_check,status,price,currency,condition,availability,image,update_time from linhnguyenthuy1_2018_3_21")
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()
logging.info(rows)
size = 20000000
#
df = pd.DataFrame(rows)
df.columns = ['Stt', 'Agent', 'Link','Title', 'Customize', 'VariantCheck','CorrectCheck', 'Status', 'Price',
              'Currency', 'Condition', 'Availability','Image','Time']
filepath = join(dirname(dirname(__file__)), "data", "test.xlsx")
df.to_excel(filepath.format(size), index=False)
