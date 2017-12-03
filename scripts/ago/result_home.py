def application(environment, start_response):
	from webob import Request, Response
	from datetime import datetime
	import psycopg2
	conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
	cur = conn.cursor()
	request = Request(environment)
	#params = request.params
	post = request.POST

	agent = post['account']
	lu = post['lu']
	year = datetime.today().year
	cur.execute("""create table if not exists home_%s(
	id serial8 primary key,
    agent text,
	report_date date, 
	q_type text,	
	q_answered text,	
	time_spent text,
	quality text,
	lastupdate timestamp,
	update_time timestamp default now())""",[year])
	for i in range(int(post['len'])):
		cur.execute("""insert into home_%s"""%year+""" (agent,report_date,q_type,q_answered,time_spent,quality,lastupdate) values(%s,%s,%s,%s,%s,%s,%s)""",(post['account'],post['data[%s][date]'%i],post['data[%s][qt]'%i],post['data[%s][qa]'%i],post['data[%s][ts]'%i],post['data[%s][qu]'%i],post['lu']))

	conn.commit()
	cur.close()
	conn.close()
	page ="ok"
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)
