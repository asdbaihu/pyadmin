# -*-coding:utf-8 -*-
import pandas as pd
import psycopg2,logging,base64,os
from datetime import datetime

#from os.path import join, dirname

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

# print("Ngay can nhap theo dinh dang : nam_thang_ngay (2018_3_28")
# day = input("Moi ban nhap ngay : ")
#
# if day !='':
#     today = day

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
image_path = '/usr/local/www/apache24/data/images'
data_path = '/usr/local/www/apache24/data'
#d = '/usr/local/www/apache24/data'

if not os.path.exists(image_path):
    os.makedirs(image_path)
    logging.info("create folder %s"%image_path)

if not os.path.exists(data_path):
    os.makedirs(data_path)
    logging.info("create folder %s"%data_path)

conn = getConnection()
cur = conn.cursor()
cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%%%s%%'  and not tablename ilike '%%master_table%%' and not tablename ilike '%%disagreement%%'" % today)
table_names = iter(cur.fetchall())
conn.commit()
cur.close()
conn.close()

# for table_name in table_names:
#     conn = getConnection()
#     cur = conn.cursor()
#     logging.info("table name : %s "%table_name)
#     cur.execute("select id,img_data from %s where img_data ilike '%%data:image%%' "%table_name)
#     rows = cur.fetchall()
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     for row in rows:
#         #logging.info("img_data : %s"%row[1])
#         img64 = row[1].replace('data:image/png;base64,','')
#         data = img64.replace(" ","+")
#         imgdata = base64.b64decode(data)
#         filename = '%s/%s_%s.jpg'%(image_path,table_name[0],row[0])  # I assume you have a way of picking unique filenames
#         with open(filename, 'wb') as f:
#             f.write(imgdata)
#
#         conn = getConnection()
#         cur = conn.cursor()
#
#         cur.execute("update %s set image ='http://172.16.23.7/images/%s_%s.jpg', img_data=null where id=%s "%(table_name[0],table_name[0],row[0],row[0]))
#         conn.commit()
#         cur.close()
#         conn.close()
#
#     conn = getConnection()
#     cur = conn.cursor()
#     cur.execute("select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,image,update_time from %s"%table_name[0])
#     rows_excel = cur.fetchall()
#     conn.commit()
#     cur.close()
#     conn.close()
#     #logging.info(rows_excel)
#     size = 20000000
#
#     df = pd.DataFrame(rows_excel)
#     df.columns = ['Stt', 'Agent', 'Link','Title', 'Customize', 'VariantCheck','PriceCheck','PageProblem', 'PriceDetail', 'Price',
#                   'Currency', 'Condition', 'Availability','Cds_key','Image','Time']
#     #filepath = join(dirname(dirname(__file__)), "data", "%s.xlsx"%table_name)
#     filepath ="%s/%s.xlsx"% (data_path,table_name[0])
#     df.to_excel(filepath.format(size), index=False)


while True:
    try:
        table_name = table_names.__next__()[0]
        while True:
            try:
                conn = getConnection()
                cur = conn.cursor()
                cur.execute(f"select id,img_data from {table_name} where img_data ilike '%%data:image%%' limit 1")
                row = cur.fetchone()
                conn.commit()
                cur.close()
                conn.close()
                if row == None:
                    break
                #logging.info("img_data : %s"%row[1])
                img64 = row[1].replace('data:image/png;base64,','')
                data = img64.replace(" ","+")
                imgdata = base64.b64decode(data)
                filename = f'{image_path}/{table_name}_{row[0]}.jpg'  # I assume you have a way of picking unique filenames
                with open(filename, 'wb') as f:
                    f.write(imgdata)

                conn = getConnection()
                cur = conn.cursor()

                cur.execute(f"update {table_name} set image ='http://172.16.23.7/images/{table_name}_{row[0]}.jpg', img_data=null where id={row[0]} ")
                conn.commit()
                cur.close()
                conn.close()
                logging.info(f"done id {row[0]} of table : {table_name}")
            except Exception as e:
                break
    except StopIteration:
        break

# convert to excel
conn = getConnection()
cur = conn.cursor()
cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%%%s%%'  and not tablename ilike '%%master_table%%' and not tablename ilike '%%disagreement%%'" % today)
table_names = iter(cur.fetchall())
conn.commit()
cur.close()
conn.close()

while True:
    try:
        table_name = table_names.__next__()[0]
        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,image,update_time from {table_name} where img_data is null order by id")
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
    except StopIteration:
        break

logging.info("tables: %s",str(table_names))
logging.info("Done!")
