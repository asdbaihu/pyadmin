def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	post = request.POST
	page="ok" 
	import psycopg2
	from omnivore import conn
	#link title agent
	page="ok" 
	page += "%s -  "%(post['len'])
	try:
		conn = psycopg2.connect(conn.conn)
	except:
		page += "Can not access database"
	cur = conn.cursor()

	for i in range(int(post['len'])):
		cur.execute("""insert into home (gmail,datehome,qt,qa,ts,qu,lu) values(%s,%s,%s,%s,%s,%s,%s)""",(post['account'],post['data[%s][date]'%i],post['data[%s][qt]'%i],post['data[%s][qa]'%i],post['data[%s][ts]'%i],post['data[%s][qu]'%i],post['lu']))
	
	#for i in range(6):
		#execu="""%s %s %s %s %s %s %s """%(post['data[%s][date]'%i],post['data[%s][qt]'%i],post['data[%s][qa]'%i],post['data[%s][ts]'%i],post['data[%s][qu]'%i],post['account'],post['lu'])
	
	
	conn.commit()
	cur.close()
	conn.close()	
	
	response = Response(body = page,
				  content_type = "text/plain",
				  charset = "utf8",
				  status = "200 OK")
 
	return response(environ, start_response)


