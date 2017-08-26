from beaker.middleware import SessionMiddleware
import importlib
def application(environ, start_response):


	from webob import Request, Response
	from datetime import datetime
	request = Request(environ)
	post = request.POST
	import pyad.login
	importlib.reload(pyad.login)

	# Get the session object from the environ
	session = environ['beaker.session']

	# Check to see if a value is in the session
	user = 'username' in session
	passwd = 'password' in session

	# Set some other session variable
	#session['user_id'] = 10
	#user_id = 'user_id' in session

	if not 'username' in post:
		page = pyad.login.loginform
	elif not 'password' in post:
		page = pyad.login.loginform
	else:
		user = post['username']
		passwd = post['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,hashlib,pyad.conn
		importlib.reload(pyad.conn)
		from pyad.conn import conn
		try:
			con = psycopg2.connect(conn)
		except:
			page ="Can not access databases"

		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,hashlib.sha512(passwd.encode('utf-8')).hexdigest(),))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = pyad.login.login_again
		else:
			session['username'] = user
			session['password'] = hashlib.sha512(passwd.encode('utf-8')).hexdigest()
			session.save()
			page = """
<!doctype html>
		<html>
			<head>
			<meta http-equiv="refresh" content="0; url=/wsgi/pyad/index"/>
                <title> redirect login </title>
            </head>	
		<body>
		</body>
	</html>"""
		con.commit()
		cur.close()
		con.close()
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")

	return response(environ, start_response)

# Configure the SessionMiddleware
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application, session_opts)
