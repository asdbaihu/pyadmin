import psycopg2, pyad.module,pyad.conn

try:
  con = psycopg2.connect(pyad.conn.conn)
except:
  page = "Can not access databases"

cur = con.cursor()
import re
que = """SELECT relname as "Table", pg_size_pretty(pg_total_relation_size(relid)) As "Size", pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as "External Size" FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC"""


b = "SELECT relname as \"Table\", pg_size_pretty(pg_total_relation_size(relid)) As \"Size\", pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as \"ExternalSize\" FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC"
#c =re.sub('\s+','',b)
c = b.replace("'","\\'")
print(c)
cur.execute(c)
d =cur.fetchall()
print(d)


