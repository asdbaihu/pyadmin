# coding=utf-8
import pandas as pd
import psycopg2,logging,base64,os
from datetime import datetime

#from os.path import join, dirname

logging.basicConfig(level=logging.DEBUG)
#logging.warning("Watch out!")
#logging.info("I told you so")

def getConnection():
    conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
    return conn

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
today = '%s_%s_%s' % (year, month, day)
print("Vi du: Dien ten bang theo cau truc: linhnguyenthuy1_2018_3_22 (tennhanvien_nam_thang_ngay)")
table_name = input("Dien ten bang can truy xuat: ")
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
data_path = '/usr/local/www/apache24/data'
#d = '/usr/local/www/apache24/data'

if not os.path.exists(image_path):
    os.makedirs(image_path)
    logging.info("create folder %s"%image_path)

if not os.path.exists(data_path):
    os.makedirs(data_path)
    logging.info("create folder %s"%data_path)

# conn = getConnection()
# cur = conn.cursor()
#
# cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%%%s%%'" % today)
# table_names = cur.fetchall()
# conn.commit()
# cur.close()
# conn.close()

conn = getConnection()
cur = conn.cursor()
logging.info("table name : %s "%table_name)
cur.execute("select id,img_data from %s where img_data ilike '%%data:image%%' "%table_name)
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()

for row in rows:
    #logging.info("img_data : %s"%row[1])
    img64 = row[1].replace('data:image/png;base64,','')
    data = img64.replace(" ","+")
    imgdata = base64.b64decode(data)
    filename = '%s/%s_%s.jpg'%(image_path,table_name,row[0])  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

    conn = getConnection()
    cur = conn.cursor()

    cur.execute("update %s set image ='http://172.16.23.7/images/%s_%s.jpg', img_data=null where id=%s "%(table_name,table_name,row[0],row[0]))
    conn.commit()
    cur.close()
    conn.close()

conn = getConnection()
cur = conn.cursor()
cur.execute("select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,image,update_time from %s"%table_name)
rows_excel = cur.fetchall()
conn.commit()
cur.close()
conn.close()
#logging.info(rows_excel)
size = 20000000

df = pd.DataFrame(rows_excel)
df.columns = ['Stt', 'Agent', 'Link','Title', 'Customize', 'VariantCheck','PriceCheck','PageProblem', 'PriceDetail', 'Price',
              'Currency', 'Condition', 'Availability','Cds_key','Image','Time']
#filepath = join(dirname(dirname(__file__)), "data", "%s.xlsx"%table_name)
filepath ="%s/%s.xlsx"% (data_path,table_name)
df.to_excel(filepath.format(size), index=False)

logging.info("table: %s",str(table_name))
logging.info("Done!")
