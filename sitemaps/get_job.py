from webob import Request, Response
import psycopg2
import json, collections


def application(environ, start_response):
    request = Request(environ)
    post = request.POST
    param = request.params

    # link title agent
    #page = """{"result":"ok"}"""
    if not 'account_id' in post:
        accounts = '27'
    else:
        accounts = param['account_id']


    try:
        conn = psycopg2.connect("user=postgres password=12345678 host=localhost port=5432 dbname=pyadmin")
    except:
        page += "Can not access database"
    cur = conn.cursor()
    cur.execute("""select job from job where id= (select min(id) from job where confirm is null and accounts ='%s')"""%accounts)
    rows = cur.fetchone()
    page = "%s"%rows[0]
    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

