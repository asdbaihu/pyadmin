from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import pyad.login
	importlib.reload(pyad.login)
	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	#user = 'username' in session

	if not 'username' in session:
		page = pyad.login.loginform
		response = Response(body = page,
		content_type = "text/html",
		charset = "utf8",
		status = "200 OK")

	elif not 'password' in session:
		page = pyad.login.loginform
		response = Response(body = page,
		content_type = "text/html",
		charset = "utf8",
		status = "200 OK")
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,pyad.conn,hashlib,datetime
		importlib.reload(pyad.conn)

		try:
			con = psycopg2.connect(pyad.conn.conn)
		except:
			page ="Can not access databases"

		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = pyad.login.login_again
			response = Response(body = page,
			content_type = "text/html",
			charset = "utf8",
			status = "200 OK")

		else:
			if ps[0][2] == 2:
				if not 'table' in post:
					page = pyad.login.login_again
					response = Response(body = page,content_type = "text/html",	charset = "utf8", status = "200 OK")
				else:
					table = post['table']
				cur.execute("select column_name, data_type from information_schema.columns where table_name = '" + table + "'")
				rows = cur.fetchall()

				#cur.execute("select * from %s limit 1"%table)
				#cols = [desc[0] for desc in cur.description]

				cols = [desc[0] for desc in rows]
				insertcols = [col for col in cols if col not in ['id','update_time']]
				types = {}

				for row in rows:
					types[row[0]] =row[1]

				page = ""

				if 'leninsert' in post:
					if int(post['leninsert']) > 0:
						for i in range(int(post['leninsert'])):
							values = ()
							for colname in insertcols:
								if colname =='account_password':
									values +=("NULLIF('" + hashlib.sha512(post['insert[%s][%s]'%(i,colname)].encode('utf-8')).hexdigest() + "','')",)
								elif types[colname]=='integer':
									values +=("NULLIF('" + post['insert[%s][%s]'%(i,colname)] + "','')::integer",)
								elif types[colname]=='bigint':
									values +=("NULLIF('" + post['insert[%s][%s]'%(i,colname)] + "','')::integer",)
								else:
									values +=("NULLIF('" + post['insert[%s][%s]'%(i,colname)] + "','')",)
							try:
								cur.execute("""insert into """ + table + """ (""" + ",".join(insertcols) + """) values ( """+ ",".join(values) + """)""")
							except:
								con.rollback()

				if 'lenupdate' in post:
					if int(post['lenupdate']) > 0:
						for i in range(int(post['lenupdate'])):
							if post['update[%s][column]'%i] == 'account_password':
								cur.execute("update " + table + " set "+ post['update[%s][column]'%i] +""" = %s, update_time = %s where id = %s """,(hashlib.sha512(post['update[%s][value]'%i].encode('utf-8')).hexdigest(), datetime.datetime.today(), post['update[%s][id]'%i]))
							else:
								cur.execute("update " + table + " set "+ post['update[%s][column]'%i] +""" = %s, update_time = %s  where id = %s """,(post['update[%s][value]'%i], datetime.datetime.today(),post['update[%s][id]'%i]))
				if 'delete[]' in post:
					for row in list(post.getall('delete[]')):
						if row !='' :
							cur.execute("delete from " + table + " where id = %s""",(int(row),))

				page ="""{"result":"ok"}"""
				response = Response(body = page,
				content_type = "application/json",
				charset = "utf8",
				status = "200 OK")
			else:
				page = pyad.login.login_again
				response = Response(body = page,
				content_type = "text/html",
				charset = "utf8",
				status = "200 OK")
		con.commit()
		cur.close()
		con.close()



	return response(environment, start_response)
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application,session_opts)
