def application(environ, start_response):
	from datetime import datetime
	from webob import Request, Response
	request = Request(environ)
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = conn.cursor()
	y = datetime.today().year
	m = datetime.today().month
	d = datetime.today().day
	
	post = request.POST
	page="ok"
	
	#cur.execute("""create table if not exists submitted_%s_%s_%s
	#			(id serial8 primary key,
	#			date_time timestamp default now(),
	#			agent text,
	#			submitted int,
	#			process_time numeric,
	#			end_time timestamp default now())""",(y,m,d))	
	
	cur.execute("""select count(*) from submitted_%s_%s_%s where agent=%s""",(y,m,d,post['account'].strip()))			
	ps = cur.fetchone()
	if int(ps[0])>0:
		if int(post['answer_count'].strip())>0:
			cur.execute("update submitted_%s_%s_%s set submitted=%s,end_time=%s where id =(select max(id) from submitted_%s_%s_%s where agent=%s)",(y,m,d,post['answer_count'].strip(),str(datetime.now()),y,m,d,post['account'].strip()))
		else:
			cur.execute("insert into submitted_%s_%s_%s(date_time,agent,submitted) values(%s,%s,%s)",(y,m,d,str(datetime.today()),post['account'].strip(),post['answer_count'].strip()))
	else:
		cur.execute("insert into submitted_%s_%s_%s(date_time,agent,submitted) values(%s,%s,%s)",(y,m,d,str(datetime.today()),post['account'].strip(),post['answer_count'].strip()))		
	conn.commit()
	cur.close()
	conn.close()			

	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


