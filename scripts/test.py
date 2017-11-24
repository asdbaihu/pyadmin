def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import importlib,apolo.login
	importlib.reload(apolo.login)
	from apolo import login


	import psycopg2,psycopg2.extras,psycopg2.extensions,apolo.conn
	importlib.reload(apolo.conn)
	from apolo.conn import conn

	try:
		con = psycopg2.connect(conn)
	except:
		page ="Can not access databases"

	cur = con.cursor()
	page ="ok"	



	con.commit()
	cur.close()
	con.close()	
	response = Response(body = page,
	content_type = "text/html",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)
