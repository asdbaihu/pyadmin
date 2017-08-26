from beaker.middleware import SessionMiddleware
import importlib

def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import geo.conn
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
			import redis, decimal
			r = redis.StrictRedis(host='localhost',port=6379,db=0)
			
			
			if not 'key' in post:
				key = ''
			else:
				key = post['key']		
										
			page = ""
			if 'leninsert' in post:
				if int(post['leninsert']) > 0:
					for i in range(int(post['leninsert'])):
						#row = [None if post['insert[%s][inid]'%i] == 'NULL' else post['insert[%s][inid]'%i] for post['insert[%s][inid]'%i] in row]
						r.execute_command("geoadd %s %s %s %s"%(post['insert[%s][key]'%i],post['insert[%s][lon]'%i],post['insert[%s][lat]'%i],post['insert[%s][member]'%i]))
			
			if 'lenupdate' in post:
				if int(post['lenupdate']) > 0:
					for i in range(int(post['lenupdate'])):
						r.execute_command("geoadd %s %s %s %s"%(post['update[%s][key]'%i],post['update[%s][lon]'%i],post['update[%s][lat]'%i],post['update[%s][member]'%i]))
													
			if 'delete[]' in post:
				for row in list(post.getall('delete[]')):
					r.execute_command("zrem %s %s"%(key,row))
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
