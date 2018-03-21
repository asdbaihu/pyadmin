from webob import Request, Response
import psycopg2
import json, collections

def application(environ, start_response):
    request = Request(environ)
    post = request.POST
    # link title agent
    page = """{"result":"ok"}"""
    try:
        conn = psycopg2.connect("user=postgres password=12345678 host=localhost port=5432 dbname=pyadmin")
    except:
        page += "Can not access database"
    cur = conn.cursor()
# "data":data,"accounts":"test","columns":dataColumns,"dale":data.length, "id":localStorage['id']
    columns = post.getall('columns[]')
    datalength = post['dale']

    for i in range(int(datalength)):
        d = collections.OrderedDict()
        for col in columns:
            d[col] = post["data[%s][%s]"%(i,col)]

        cur.execute("""insert into crawler (crawler,accounts) values(%s,NULLIF(%s,''))""", (json.dumps(d,ensure_ascii=False), post['accounts']))

    cur.execute("""update sitemaps set confirm='y' where id=%s""", (int(post['id']),))


    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

