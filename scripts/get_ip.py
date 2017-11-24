def application(environment, start_response):
	from webob import Request, Response
	from datetime import datetime
	import psycopg2
	conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
	cur = conn.cursor()
	request = Request(environment)
	#params = request.params
	post = request.POST

	ip = post['ip']
	country_name = post['country_name']
	if not 'date_time' in post:
		year = datetime.today().year
		month = datetime.today().month
		day = datetime.today().day
	else:
		month = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').month)
		year = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').year)
		day = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').day)

	cur.execute("""create table if not exists ip%s%s%s(id serial8 primary key,ip inet,country_name text,update_time timestamp default now())""",(year,month,day))

	cur.execute("""insert into ip%s%s%s"""%(year,month,day) + """(ip,country_name) values (nullif(%s,'')::inet,nullif(%s,''))""",(ip,country_name))
	conn.commit()
	cur.close()
	conn.close()
	page ="ok"
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)
