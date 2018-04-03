# coding=utf-8
import pandas as pd
import psycopg2,logging,base64,os
from datetime import datetime

from os.path import join, dirname

logging.basicConfig(level=logging.DEBUG)
logging.warning("Watch out!")
logging.info("I told you so")

def getConnection():
    conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
    return conn

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
today = '%s_%s_%s' % (year, month, day)

print("Ngay can nhap theo dinh dang : nam_thang_ngay (2018_3_28")
day = input("Moi ban nhap ngay : ")
if day =='':
    day = today

# for test case:
# conn = getConnection()
# cur = conn.cursor()
#
# try:
#     cur.execute("drop table  tennhanvien1_%s "%today)
# except:
#     pass
#
# try:
#     cur.execute("drop table  tennhanvien2_%s "%today)
# except:
#     pass
#
# try:
#     cur.execute("drop table  tennhanvien3_%s "%today)
# except:
#     pass
#
# try:
#     cur.execute("create table  tennhanvien1_%s as table tranghuyen1_2018_3_19 "%today)
# except:
#     pass
# try:
#     cur.execute("create table  tennhanvien2_%s as table tranghuyen1_2018_3_19 "%today)
# except:
#     pass
# try:
#     cur.execute("create table  tennhanvien3_%s as table tranghuyen1_2018_3_19 "%today)
# except:
#     pass
#
# conn.commit()
# cur.close()
# conn.close()
#het doan test case


#tao folder chua images:

# image_path = '/var/www/html/images'
# data_path = '/var/www/html/data'
image_path = '/usr/local/www/apache24/images'
data_path = '/usr/local/www/apache24/data/excel_without_images'
#d = '/usr/local/www/apache24/data'

if not os.path.exists(image_path):
    os.makedirs(image_path)
    logging.info("create folder %s"%image_path)

if not os.path.exists(data_path):
    os.makedirs(data_path)
    logging.info("create folder %s"%data_path)

conn = getConnection()
cur = conn.cursor()

cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%%%s%%'  and not tablename ilike '%%master_table%%' and not tablename ilike '%%disagreement%%'" % day)
table_names = cur.fetchall()
conn.commit()
cur.close()
conn.close()

for table_name in table_names:
    conn = getConnection()
    cur = conn.cursor()
    cur.execute("select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,update_time from %s"%table_name[0])
    rows_excel = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    #logging.info(rows_excel)
    size = 20000000

    df = pd.DataFrame(rows_excel)
    df.columns = ['Stt', 'Agent', 'Link','Title', 'Customize', 'VariantCheck','PriceCheck','PageProblem','PriceDetail', 'Price',
                  'Currency', 'Condition', 'Availability','Cds_key','Time']
    #filepath = join(dirname(dirname(__file__)), "data", "%s.xlsx"%table_name)
    filepath ="%s/%s.xlsx"% (data_path,table_name[0])
    df.to_excel(filepath.format(size), index=False)

logging.info("tables: %s",str(table_names))
logging.info("Done!")
