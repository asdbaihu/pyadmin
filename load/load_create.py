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
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
	elif not 'password' in session:
		page = pyad.login.loginform
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,pyad.conn
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
				if not 'cols[]' in post:
					cols =[]
					query_cols = "*"
				else:
					cols = post.getall('cols[]')
					query_cols = ",".join(post.getall('cols[]'))

				if not 'filcols[]' in post:
					filcols =[]
				else:
					filcols = post.getall('filcols[]')

				if not 'orderby[]' in post:
					orderby =['id']
				else:
					orderby = post.getall('orderby[]')

				if not 'by' in post:
					by = 'asc'
				else:
					by = post['by']
				# post['types[id]']
				query=[]
				for c in cols:
					if post['types[%s]'%c] =='int':
						if 'mor%s'%c in post:
							if post['mor%s'%c] != "":
								query.append(c + " > " + post['mor%s'%c] +" and ")
						if 'les%s'%c in post:
							if post['les%s'%c] != "":
								query.append(c + " < " + post['les%s'%c] +" and ")

					elif post['types[%s]'%c] =='datetime':
						if 'mor%s'%c in post:
							if post['mor%s'%c] != "":
								query.append(c + " > '" + post['mor%s'%c] +"' and ")
						if 'les%s'%c in post:
							if post['les%s'%c] != "":
								query.append(c + " < '" + post['les%s'%c] +"' and ")

					else:
						if 'fil%s'%c in post:
							if post['fil%s'%c] !="":
								query.append(c + " like '%%" + post['fil%s'%c] +"%%' and ")
					if '%snull'%c in post:
						if post['%snull'%c] !="":
							query.append(c + " is " + post['%snull'%c].replace("_"," ") + " and ")


				if 'movecols[]' in post:
					if len(post.getall('movecols[]')) != 0:
						query_cols = ",".join(post.getall('movecols[]'))

				start = (int(page)-1)*display

				cur.execute("""select count(*) from """ + table + " where " +  " ".join(query) +   " id > 0")
				rows_count = cur.fetchone()
				a ="select "+ query_cols +" from " + table + " where " + " ".join(query) + " id > 0 order by " + ",".join(orderby) +" " + by + " limit %s offset %s "%(display,start)
				cur.execute("select "+ query_cols +" from " + table + " where " + " ".join(query) + " id > 0 order by " + ",".join(orderby) +" " + by + " limit %s offset %s "%(display,start))
				rows = cur.fetchall()
				#column_names = [desc[0] for desc in cur.description if desc[0] not in hidecols]
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
					for index in range(len(cols)):
						if type(row[i][index]).__name__ == 'datetime':
							d[cols[index]] = str(row[i][index])
						else:
							d[cols[index]] = row[i][index]
					objects_list.append(d)

				#print(objects_list)
				page += json.dumps(objects_list)
				page +=""","sum_page":%s,"test":"%s" """%(int(sum_page),a)

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
				page = pyad.login.login_again
				response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
			con.commit()
			cur.close()
			con.close()
	return response(environment, start_response)
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts

application = SessionMiddleware(application, session_opts)
