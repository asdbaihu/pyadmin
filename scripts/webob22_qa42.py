def application(environment, start_response):
	from webob import Request, Response
	from datetime import datetime
	import psycopg2
	conn = psycopg2.connect("host=localhost dbname=Google_qc user=postgres password=12345678")
	cur = conn.cursor()
	request = Request(environment)
	#params = request.params
	post = request.POST

	agent = post['agent']
	link = post['link']
	title = post['title']
	customize = post['customize']
	variant_check = post['variant_check']
	correct_check = post['correct_check']
	status = post['status']
	price = post['price']
	currency = post['currency']
	condition = post['condition']
	availability = post['availability']
	process_time = post['process_time']
	cds_key = post['cds_key']
	if not 'date_time' in post:
		year = datetime.datetime.today().year
		month = datetime.datetime.today().month
		day = datetime.datetime.today().day
	else:
		month = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').month)
		year = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').year)
		day = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').day)

	cur.execute("""create table if not exists qc_project%s%s%s(id serial8 primary key,agent text,link text,	title text,	customize text,	variant_check text,	correct_check text,	status text, price text,currency text,condition text,availability text,	process_time text,cds_key text,update_time timestamp default now())""",(year,month,day))

	cur.execute("""insert into qc_project%s%s%s"""%(year,month,day) + """(agent,link,title,customize,variant_check,correct_check,status,price,currency,condition,availability,process_time,cds_key) values (nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''))""",(agent,link,title,customize,variant_check,correct_check,status,price,currency,condition,availability,process_time,cds_key))
	conn.commit()
	cur.close()
	conn.close()
	page ="ok"
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)
