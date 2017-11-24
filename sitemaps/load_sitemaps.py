from webob import Request, Response
import psycopg2
import json, collections


def application(environ, start_response):
    request = Request(environ)
    post = request.POST
    # link title agent
    #page = """{"result":"ok"}"""
    if not 'accounts' in post:
        accounts = 'test'
    else:
        accounts = post['accounts']


    try:
        conn = psycopg2.connect("user=postgres password=12345678 host=localhost port=5432 dbname=pyadmin")
    except:
        page += "Can not access database"
    cur = conn.cursor()
    cur.execute("""select id, sitemaps, accounts, interval, delay from sitemaps where id= (select min(id) from sitemaps where confirm is null and accounts ='%s')"""%accounts)
    column_names = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    row = []
    for ro in rows:
        row.append(list(ro))
    page = '{"product":'
    objects_list = []
    import json, collections

    for i in range(len(row)):
        d = collections.OrderedDict()
        d['index'] = i + 1  # row[0]
        for index in range(len(column_names)):
            if type(row[i][index]).__name__ == 'datetime':
                d[column_names[index]] = str(row[i][index])
            else:
                d[column_names[index]] = row[i][index]
        objects_list.append(d)

    # print(objects_list)
    page += json.dumps(objects_list)
    page += """}"""
    # page = "{"
    # page += """"id":'%s',"""%ps[0]
    # page += "sitemaps:'%s',"%ps[1]
    # page += "accounts:'%s',"%ps[2]
    # page += "interval:%s,"%ps[3]
    # page += "delay:%s,"%ps[4]
    # page += "}"

    # page = """{"result":"ok testing ngoc trinh ha an ha han ha an ha an"}"""

    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

