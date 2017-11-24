from webob import Request, Response
import psycopg2

def application(environ, start_response):
    request = Request(environ)
    post = request.POST
    # link title agent
    page = """{"result":"ok"}"""
    try:
        conn = psycopg2.connect("user=docker password=docker host=192.168.0.242 port=5432 dbname=pyadmin")
    except:
        page += "Can not access database"
    cur = conn.cursor()
    cur.execute("""insert into sitemaps (sitemaps,accounts) values(%s,NULLIF(%s,''))""", (post['sitemaps'],post['accounts']))


    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

