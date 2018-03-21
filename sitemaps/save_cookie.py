from webob import Request, Response
import pymysql
import datetime


def application(environ, start_response):
    connection = pymysql.connect(host='192.168.0.118',
                                 port=3306,
                                 user='docker',
                                 password='docker',
                                 db='docker',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    request = Request(environ)
    post = request.POST
    # link title agent
    page = """{"result":"ok"}"""
    cookie = post['cookie']
    url = post['url']

    try:
        with connection.cursor() as cursor:
            sql = "insert into fbcrawler_service_account (email,on_off,mission_id,engine_id,cookies,homepage) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (str(datetime.datetime.today()), 0, 2, 2, cookie, url))

        connection.commit()
    finally:
        connection.close()

    # #241
    connection2 = pymysql.connect(host='192.168.0.241',
                                  port=3307,
                                  user='docker',
                                  password='docker',
                                  db='docker',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor,
                                  autocommit=True)

    try:
        with connection2.cursor() as cursor:
            sql = "insert into fbcrawler_service_account (email,on_off,mission_id,engine_id,cookies,homepage) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (str(datetime.datetime.today()), 0, 2, 2, cookie, url))

        connection2.commit()
    finally:
        connection2.close()

    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)
