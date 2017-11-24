def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	import psycopg2
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur =conn.cursor()
	#import redis
	#r = redis.StrictRedis(host='localhost', port=6379, db=0)
	post = request.POST
	page=""
	
	for row in range(int(len(post.getall('changes[value][]')))):
		answer =  post.getall('changes[value][]')[int(row)].split("<#>")[2]
		link = 	post.getall('changes[value][]')[int(row)].split("<#>")[1]
		domain = post['changes[account]'].split('<#>')[2]
		quest = post['changes[account]'].split('<#>')[3]	
		table = domain.split(".")[-1].replace("&amp;","").replace(" ","").replace("-","") + quest.replace(" ","")
		insert = """INSERT INTO """ + table +""" (link, answer, gio) SELECT '%s', '%s', now()  WHERE NOT EXISTS (SELECT 1 FROM """%(link, answer ) + table + """ WHERE link ='%s');"""%(link)
		cur.execute(insert)	
		#r.set("%s_%s"%(post.getall('changes[value][]')[int(row)].split("<#>")[1],post['changes[account]'].split('<#>')[3]),"%s_%s"%(post.getall('changes[value][]')[int(row)].split("<#>")[2],post['changes[account]'].split('<#>')[0]),57600)
		conn.commit()
	cur.close()
	conn.close()		
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


