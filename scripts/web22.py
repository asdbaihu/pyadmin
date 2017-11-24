def application(environ, start_response):
	from webob import Request, Response
	from datetime import datetime
	request = Request(environ)
	post = request.POST
	#table = "%s%s"%(post["domain"].split(".")[-1].replace("&amp;","").replace(" ","").replace("-",""),post["quest"].replace(" ",""))
	page=""
	import psycopg2
	con = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = con.cursor()
	find = """select answer from %s%s where link = '%s' """%(post["domain"].split(".")[-1].replace("&amp;","").replace(" ","").replace("-",""),post["quest"].replace(" ",""),post["link"])
	cur.execute(find)
	page +="%s"%cur.fetchone()[0]
	#if cur.fetchone() is None:
	#	page +="%s"%cur.fetchone()[0]
	#else:
	#	page +="None"
	#page += "%s"%ps[0]
	#page +="%s -- %s, %s, %s"%(find,post["domain"].split(".")[-1].replace("&amp;","").replace(" ","").replace("-",""),post["quest"].replace(" ",""),post["link"])
	con.commit()
	cur.close()
	con.close()
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)
