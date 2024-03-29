import pandas as pd
import psycopg2,logging,base64,os
from datetime import datetime

from os.path import join, dirname

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

print("Ngay can nhap theo dinh dang : nam_thang_ngay (2018_3_28")
day = input("Moi ban nhap ngay : ")
if day !='':
    today = day


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

image_path = '/usr/local/www/apache24/data/images'
data_path = '/usr/local/www/apache24/data/data'

if not os.path.exists(image_path):
    os.makedirs(image_path)
    logging.info("create folder %s"%image_path)

if not os.path.exists(data_path):
    os.makedirs(data_path)
    logging.info("create folder %s"%data_path)

conn = getConnection()
cur = conn.cursor()

cur.execute("select tablename from pg_tables where schemaname='public' and tablename ilike '%%%s%%' and not tablename ilike '%%master_table%%' and not tablename ilike '%%disagreement%%'" % today)
table_names = iter(cur.fetchall())
conn.commit()
cur.close()
conn.close()

conn = getConnection()
cur = conn.cursor()
try:
    cur.execute("drop table master_table_%s"%today)
except Exception as e:
    pass
conn.commit()
cur.close()
conn.close()

# create table master

conn = getConnection()
cur = conn.cursor()
cur.execute("""create table if not exists master_table_%s(
    id_master serial8 primary key,
    id int,
    agent text,
    link text,
    title text,
    customize text,
    variant_check text,
    price_check text,
    page_problem text,
    price_detail text,
    price text,
    currency text,
    condition text,
    availability text,
    cds_key text,
    img_data text,
    image text,
    update_time timestamp,
    master_update_time timestamp default now())"""%today)
conn.commit()
cur.close()
conn.close()



while True:
    try:
        table_name = table_names.__next__()[0]
        conn = getConnection()
        cur = conn.cursor()
        logging.info("table name : %s "%table_name)
        cur.execute("""  insert into master_table_%s(id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,img_data,image,update_time) select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,img_data, image,update_time from %s """%(today,table_name))
        conn.commit()
        cur.close()
        conn.close()
    except StopIteration:
        break


# delete table;
conn = getConnection()
cur = conn.cursor()
try:
    cur.execute("drop table disagreement_%s" % today)
except Exception as e:
    pass
conn.commit()
cur.close()
conn.close()


# create disagreement table
conn = getConnection()
cur = conn.cursor()
cur.execute("""
create table disagreement_%s as select e.id,e.agent,e.link,e.title,e.customize,e.variant_check,e.price_check,e.page_problem,e.price_detail,e.price,e.currency,e.condition,e.availability,e.cds_key,e.img_data,e.image,e.update_time from (select a.cds_key,a.title,a.count from
(select cds_key,title,count(*) from master_table_%s group by cds_key,title  having count(*)>1) as a left join
(select cds_key,title, count(*) from master_table_%s group by cds_key ,title,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability having count(*)>1) as b on a.cds_key = b.cds_key
and a.count = b.count where a.cds_key !='undefined' and b.cds_key is null) as d inner join
(select *from master_table_%s ) as e on e.cds_key = d.cds_key and e.title=d.title;"""%(today,today,today,today))
conn.commit()
cur.close()
conn.close()


# convert image
table_name = 'disagreement_%s'%today
conn = getConnection()
cur = conn.cursor()
logging.info("table name : %s " % table_name)
cur.execute("select id,img_data from %s where img_data ilike '%%data:image%%' " % table_name)
rows = iter(cur.fetchall())
conn.commit()
cur.close()
conn.close()


while True:
    try:
        row = rows.__next__()
        # logging.info("img_data : %s"%row[1])
        img64 = row[1].replace('data:image/png;base64,', '')
        data = img64.replace(" ", "+")
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
    except StopIteration:
        break



conn = getConnection()
cur = conn.cursor()
cur.execute("select id,agent,link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,img_data,image,update_time from disagreement_%s"%today)
rows_excel_dis = cur.fetchall()
conn.commit()
cur.close()
conn.close()
#logging.info(rows_excel)
size = 20000000
try:
    df = pd.DataFrame(rows_excel_dis)
    df.columns = ['Stt', 'Agent', 'Link','Title', 'Customize', 'VariantCheck','PriceCheck','PageProblem','PriceDetail', 'Price',
                  'Currency', 'Condition', 'Availability','Cds_key','Img_data','Image','Time']
    #filepath = join(dirname(dirname(__file__)), "data", "%s.xlsx"%table_name)
    filepath ="%s/%s.xlsx"% (data_path,"disagreement%s"%today)
    df.to_excel(filepath.format(size), index=False)
except Exception as e:
    pass

logging.info("disagreement_%s"%today)
logging.info("Done!")
#
# logging.info("tables: %s",str(table_names))
