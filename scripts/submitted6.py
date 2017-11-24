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
	d1 = date(2015,9,22)
	d2 = date(2016,9,23)
	delta = d2 -d1
	for i in range(delta.days + 1):	
		cur.execute("""create table if not exists submitted_%s_%s_%s
				(id serial8 primary key,
				date_time timestamp default now(),
				agent text,
				submitted int,
				process_time numeric,
				end_time timestamp default now())""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day))	
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3backup8@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthiphuongdung@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthihoa@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamvanchien@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthithuhien@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3levulinh@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phammytrang@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthihoa1@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3luuthihau@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3vuvangiang@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3quachthihue@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3truongthuydung@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tranthuthao@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3lengoclan@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamthiminhhue@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamthianhhong@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3hoangthithuhuong1@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamhungcuong@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tavannam@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tranxuanhan@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tranngocdung@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phungthimai@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3hoangducviet@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nghiemdackhoe@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3backup13@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3backup6@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3backup5@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthikhanhly@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamthimai@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyendinhkhanh@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3khuatquanghuy@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3hoangthithuhuong@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3leminhhoai@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthuyquynh@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tranquoctien@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3tranhoainam@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3dongthigiang@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyenthile@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3daothianh@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3nguyentuyetlan@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3phamthianh@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
		cur.execute("""insert into  submitted_%s_%s_%s (agent,submitted) values('bpo3ngothithanhphuong@gmail.com',0)""",((d1+td(days=i)).year,(d1+td(days=i)).month,(d1+td(days=i)).day)) 
	
	conn.commit()
	cur.close()
	conn.close()			

	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


