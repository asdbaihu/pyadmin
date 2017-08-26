from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import agora.login
	importlib.reload(agora.login)

	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	#user = 'username' in session

	if not 'username' in session:
		page = agora.login.loginform
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")		
	elif not 'password' in session:
		page = agora.login.loginform
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,agora.conn
		importlib.reload(agora.conn)


		try:
			con = psycopg2.connect(agora.conn.conn)
		except:
			page ="Can not access databases"
		
		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = agora.login.login_again
			response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
		else:
			if ps[0][2] == 2:
				if not 'display' in post:
					display = 200
				else:
					display = int(post['display'])
				if not 'page' in post:
					page = 1
				else: 
					page = post['page']
				if not 'table' in post:
					table = 'account'
				else:
					table = post['table']	
					
					
				start = (int(page)-1)*display	
				#que = "select *from information_schema.tables where table_schema='public'"				
				#count = "select count(*) from (select * from information_schema.tables where table_schema='public') as a "
				que ="select * from pg_database order by datname"
				count = "select count(*) from (" + que + ") as a"
				
				
				#cur.execute("""select count(*) from """ + table)
				cur.execute(count)

				
				rows_count = cur.fetchone()
				#cur.execute("""select * from """ + table + """   order by id limit %s offset %s """%(display,start))
				
				cur.execute(que)
				rows = cur.fetchall()
				column_names = [desc[0] for desc in cur.description]
				#data_types = [type(val).__name__ for index,val in enumerate(rows[0])]
				
				
				sum_page = (int(rows_count[0])/display)+1
				row = []
				for ro in rows:
					row.append(list(ro))
				page = '{"product":'
				objects_list = []
				import json,collections		
						
				for i in range(len(row)):
					d = collections.OrderedDict()
					d['index'] = i+1 #row[0]
					for index in range(len(column_names)):
						if type(row[i][index]).__name__ == 'datetime':
							d[column_names[index]] = str(row[i][index])
						else:
							d[column_names[index]] = row[i][index]
					objects_list.append(d)

				#print(objects_list)
				page += json.dumps(objects_list)
				page +=""","sum_page":%s"""%(int(sum_page))
				
				#page +=""","sum_page":%s ,"columns":"""%(int(sum_page))
				#objects_columns =[]
				#for column in column_names:
				#	c = collections.OrderedDict()
				#	c["column"] = column
				#	objects_columns.append(c)
				#columns = json.dumps(objects_columns)
				#page += str(columns)
				
				
				page +="""}"""
				response = Response(body = page,
				content_type = "application/json",
				charset = "utf8",
				status = "200 OK")				
			else:
				page = agora.login.login_again
				response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
			con.commit()
			cur.close()
			con.close()
	return response(environment, start_response)
import agora.sess
importlib.reload(agora.sess)
session_opts = agora.sess.session_opts

application = SessionMiddleware(application, session_opts)
