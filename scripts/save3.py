def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	import psycopg2,psycopg2.extras,psycopg2.extensions
	conn = psycopg2.connect("dbname=apolo user=postgres password=12345678")
	cur =conn.cursor()
	#import redis
	#r = redis.StrictRedis(host='localhost', port=6379, db=0)
	post = request.POST
	page="ok"
	table = post["table"]
	cur.execute("create table if not exists " + table + " (id serial8 primary key,agent text,url text,link text,tab text,idlab text,label text,inlab int,value text,time timestamp default now(),letter text,confirm text,note text,country text)")
	for row in range(int(len(post.getall('value[]')))):
		agent = post.getall('value[]')[int(row)].split("<#>")[0]
		url = post.getall('value[]')[int(row)].split("<#>")[1]
		link = post.getall('value[]')[int(row)].split("<#>")[2]
		tab = post.getall('value[]')[int(row)].split("<#>")[3]
		idlab = post.getall('value[]')[int(row)].split("<#>")[4]
		label = post.getall('value[]')[int(row)].split("<#>")[5]
		inlab = post.getall('value[]')[int(row)].split("<#>")[6]
		value = post.getall('value[]')[int(row)].split("<#>")[7]
		#time = listvalue[int(row)].split("<#>")[8]

		cur.execute("""insert into """ +table + """ (agent,url,link,tab,idlab,label,inlab,value) values ( NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,'')::integer, NULLIF(%s,'')) """,(agent,url,link,tab,idlab,label,inlab,value))


		conn.commit()
	cur.close()
	conn.close()		
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


