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
		response = Response(body = page,
		content_type = "text/html",
		charset = "utf8",
		status = "200 OK")			
	elif not 'password' in session:
		page = agora.login.loginform
		response = Response(body = page,
		content_type = "text/html",
		charset = "utf8",
		status = "200 OK")			
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
			response = Response(body = page,
			content_type = "text/html",
			charset = "utf8",
			status = "200 OK")			
		else:
			if ps[0][2] == 2:
				if not 'menu' in post:
					menu = 'admin_first_menu'
				else:
					menu = post['menu']

				if not 'display' in post:
					display = 200
				else:
					display = int(post['display'])
				if not 'page' in post:
					page = 1
				else: 
					page = post['page']					
				start = (int(page)-1)*display					
				if menu == 'admin_first_menu' or menu =='first_menu':
					query_count = """select count(*) from %s"""%menu
					query_rows= """select id,menu1,link from %s order by id limit %s offset %s """%(menu,display,start)
				elif menu == 'admin_second_menu' or menu == 'second_menu' :
					query_count = """select count(*) from %s"""%menu
					query_rows= """select id,first_menu_id,menu2,link from %s order by id limit %s offset %s """%(menu,display,start)
				cur.execute(query_count)
				rows_count = cur.fetchall()		
				cur.execute(query_rows)
				rows= cur.fetchall()						
				sum_page = (int(rows_count[0][0])/display)+1
				row = []
				for ro in rows:
					row.append(list(ro))
				page = '{"product":'
				objects_list = []
				import json,collections				
				if menu == 'admin_first_menu' or menu =='first_menu':
					for i in range(len(row)):
						d = collections.OrderedDict()
						d['index'] = i+1 #row[0]
						d['id']=row[i][0]
						d['menu1']=row[i][1]
						d['link'] = row[i][2]						
						objects_list.append(d)
				elif menu == 'admin_second_menu' or menu == 'second_menu' :
					for i in range(len(row)):
						d = collections.OrderedDict()
						d['index'] = i+1 #row[0]
						d['id']=row[i][0]
						d['first_menu_id']=row[i][1]
						d['menu2'] = row[i][2]
						d['link'] = row[i][3]
						objects_list.append(d)
				#print(objects_list)
				page += json.dumps(objects_list)
				page +=""","sum_page":%s}"""%sum_page
				response = Response(body = page,
				content_type = "application/json",
				charset = "utf8",
				status = "200 OK")					
			else:
				page = agora.login.login_again
				response = Response(body = page,
				content_type = "text/html",
				charset = "utf8",
				status = "200 OK")			
			con.commit()
			cur.close()
			con.close()		
	return response(environment, start_response)

# Configure the SessionMiddleware
import agora.sess
importlib.reload(agora.sess)
session_opts = agora.sess.session_opts
application = SessionMiddleware(application, session_opts)
