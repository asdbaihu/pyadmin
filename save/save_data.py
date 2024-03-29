from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import importlib,geo.conn
	importlib.reload(geo.conn)
	from geo import login
	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	#user = 'username' in session

	if not 'username' in session:
		page = login.loginform
	elif not 'password' in session:
		page = login.loginform
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,geo.conn
		importlib.reload(geo.conn)
		from geo.conn import conn

		try:
			con = psycopg2.connect(conn)
		except:
			page ="Can not access databases"
		
		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = login.login_again
		else:
			if not 'table' in post:
				table = ''
			else:
				table = post['table']		
										
			page = ""
			if 'leninsert' in post:
				if int(post['leninsert']) > 0:
					for i in range(int(post['leninsert'])):
						#row = [None if post['insert[%s][inid]'%i] == 'NULL' else post['insert[%s][inid]'%i] for post['insert[%s][inid]'%i] in row]
						row = post['insert[%s][inid]'%i]
						cur.execute("""insert into """ +table + """ (inid, page, content, imte, imteuse, imtead, link, lang, origin, afterchange, url, note, country) values ( NULLIF(%s,'')::integer, NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,'')) """,(row,post['insert[%s][page]'%i],post['insert[%s][content]'%i],post['insert[%s][imte]'%i],post['insert[%s][imteuse]'%i],post['insert[%s][imtead]'%i],post['insert[%s][link]'%i],post['insert[%s][lang]'%i],post['insert[%s][origin]'%i],post['insert[%s][afterchange]'%i],post['insert[%s][url]'%i],post['insert[%s][note]'%i], post['insert[%s][country]'%i],))
			if 'lenupdate' in post:
				if int(post['lenupdate']) > 0:
					for i in range(int(post['lenupdate'])):
						if post['update[%s][column]'%i]=='inid':
							cur.execute("update " + table + " set "+ post['update[%s][column]'%i] +""" = NULLIF(%s,'')::int where id = %s """,(post['update[%s][value]'%i],post['update[%s][id]'%i]))
						else:
							cur.execute("update " + table + " set "+ post['update[%s][column]'%i] +""" = NULLIF(%s,'') where id = %s """,(post['update[%s][value]'%i],post['update[%s][id]'%i]))	
													
			if 'delete[]' in post:
				for row in list(post.getall('delete[]')):
					cur.execute("delete from " + table + " where id = %s """,(int(row),))	
			page ="""{"result":"ok"}"""	

			con.commit()
			cur.close()
			con.close()

	response = Response(body = page,
	content_type = "application/json",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)

import geo.sess
importlib.reload(geo.sess)
session_opts = geo.sess.session_opts
	
application = SessionMiddleware(application, session_opts)
