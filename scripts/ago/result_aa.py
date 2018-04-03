def application(environment, start_response):
	from webob import Request, Response
	from datetime import datetime
	import psycopg2
	conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
	cur = conn.cursor()
	request = Request(environment)
	#params = request.params
	post = request.POST

	agent = post['agent']
	link = post['link']
	title = post['title']
	customize = post['customize']
	variant_check = post['variantCheck']
	price_check = post['priceCheck']
	page_problem = post['pageProblem']
	price_detail = post['priceDetail']
	price = post['price']
	currency = post['currency']
	condition = post['condition']
	availability = post['availability']
	cds_key = post['cds_key']
	img_data = post['img_data']

	year = datetime.today().year
	month = datetime.today().month
	day = datetime.today().day

	cur.execute("""create table if not exists """+ agent.split('@')[0].replace(".","") +"""_%s_%s_%s(id serial8 primary key,agent text default %s,link text,	title text,	customize text,	variant_check text,	price_check text, page_problem text, price_detail text, price text,currency text,condition text,availability text,cds_key text,img_data text,image text, update_time timestamp default now())""",(year,month,day,agent))
	conn.commit()
	cur.close()
	conn.close()

	conn = psycopg2.connect("host=localhost dbname=pyadmin user=postgres password=12345678")
	cur = conn.cursor()
	cur.execute("""insert into """ + agent.split('@')[0].replace(".","") + """_%s_%s_%s"""%(year,month,day) + """(link,title,customize,variant_check,price_check, page_problem,price_detail,price,currency,condition,availability,cds_key,img_data) values (nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''))""",(link,title,customize,variant_check,price_check,page_problem,price_detail,price,currency,condition,availability,cds_key,img_data))
	conn.commit()
	cur.close()
	conn.close()
	page ="ok"
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)
