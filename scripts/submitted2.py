def application(environ, start_response):
	from datetime import date,timedelta as td
	from webob import Request, Response
	request = Request(environ)
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = conn.cursor()

	post = request.POST
	page="ok"
	d1 = date(2015,8,15)
	d2 = date(2015,9,15)
	delta = d2 -d1
	for i in range(delta.days + 1):	
		cur.execute("""create table if not exists submitted_%s_%s_%s
				(id serial8 primary key,
				date_time timestamp default now(),
				agent text,
				submitted int,
				process_time numeric,
				end_time timestamp default now())""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day))	

	conn.commit()
	cur.close()
	conn.close()			

	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


