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
    cur.execute("insert into crawler(crawler) values(%s)", [json.dumps(post['data'], ensure_ascii=False)])


    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

