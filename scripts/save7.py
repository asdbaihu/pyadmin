def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	import psycopg2
	conn = psycopg2.connect("dbname=apolo user=postgres password=12345678")
	cur =conn.cursor()
	#import redis
	#r = redis.StrictRedis(host='localhost', port=6379, db=0)
	post = request.POST
	page=""
	
	for row in range(int(len(post.getall('changes[value][]')))):
		inid =  post['inid']
		link = 	post['link']
		label = post['label']
		origin = post['origin']
		table = 'pali'	
		cur.execute("""insert into """ +table + """ (page,content,imte,imteuse ) values (NULLIF(%s,''),  NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,'')) """,(inid,link,label,origin,))
		#r.set("%s_%s"%(post.getall('changes[value][]')[int(row)].split("<#>")[1],post['changes[account]'].split('<#>')[3]),"%s_%s"%(post.getall('changes[value][]')[int(row)].split("<#>")[2],post['changes[account]'].split('<#>')[0]),57600)
		conn.commit()
	cur.close()
	conn.close()		
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


