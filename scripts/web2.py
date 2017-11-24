def application(environ, start_response):
	from webob import Request, Response
	from datetime import datetime
	request = Request(environ)
	post = request.POST
	page=""
	import psycopg2
	con = psycopg2.connect("dbname=apolo user=postgres password=12345678")
	cur = con.cursor()
	values = post['find']
	#page += values
	link = values.split("<#>")[0].strip()

	if link.find("/") >=0:
		lang = link.split("/")[0].split(" - ")[1].strip()
	else:
		lang = link.split("-")[1].strip()
		
	tab = values.split("<#>")[1].strip()
	
	if values.find("_") >= 0:
		idlab = values.split("_")[2].strip()
	else:
		idlab = values.strip()
			
	label = values.split("<#>")[3].strip()	
	value = values.split("<#>")[4].strip()
	
	page += "language: " + lang +"; \n" + "link: " + link + ";\n tab: "+ tab + ";\n label: " + label + ";\n value: " + value
	
	
	#lang = 
	#find = """select answer from %s%s where link = '%s' """%(post["domain"].split(".")[-1].replace("&amp;","").replace(" ","").replace("-",""),post["quest"].replace(" ",""),post["link"])
	#cur.execute(find)
	#ps = cur.fetchone()
	#if ps == None:
		#page += "None"
	#else:
		#page +="%s"%ps[0]
	

	con.commit()
	cur.close()
	con.close()
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


