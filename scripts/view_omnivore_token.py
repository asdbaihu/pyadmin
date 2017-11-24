def application(environ, start_response):
	#from datetime import datetime
	from webob import Request, Response
	request = Request(environ)
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = conn.cursor()
	#y = datetime.today().year
	#m = datetime.today().month
	post = request.POST
	page="Token key: "
	
	#cur.execute("""create table if not exists token	(id serial8 primary key,date_time timestamp default now(),token text)""")	
	cur.execute("select token from token")
	rows = cur.fetchall()
	for row in rows:
		page += " %s"%row[0]
	conn.commit()
	cur.close()
	conn.close()			

	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


