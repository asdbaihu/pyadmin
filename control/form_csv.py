from beaker.middleware import SessionMiddleware
import importlib
def application(environ, start_response):
	from webob import Request, Response
	#from datetime import datetime
	#request = Request(environ)
	#post = request.POST
	import geo.login
	importlib.reload(geo.login)

	from geo import login
	

	# Get the session object from the environ
	session = environ['beaker.session']

	# Check to see if a value is in the session
	user = 'username' in session
	passwd = 'password' in session

	# Set some other session variable
	#session['user_id'] = 10
	#user_id = 'user_id' in session

	if not 'username' in session:
		page = login.loginform
	elif not 'password' in session:
		page = login.loginform
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,hashlib,geo.conn
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
			from geo.module import head,headlink,menuadmin,menuuser
			page =""
			page += head + headlink
			page +="<title>home page</title>"
			page +="""
			</head>
			<body>
					<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
						<div class="container">
						<div class="navbar-collapse collapse">
							<ul class="nav navbar-nav">"""

			if int(ps[0][2]) == 2:
				page += menuadmin
			else:
				page += menuuser
			page += """</ul>
						</div></div>
						</nav>								
						<br />
						<br />
						<br />
						<br />"""
						
			page +=""" 
						<h1>Upload file csv  bo dem  </h1>
			<form name="test" method="post" action="/wsgi/apolo/save/upload_csv" enctype="multipart/form-data">
			File: <input type="file" name="file" multiple/><br />
			Table :<input type="text" name="table" value='' required/> (omnivore_nam_thang_ngay omnivore_2015_5_7 : bang csv 2015-5-7 ) <br />
				  <input type="submit" name="submit" value="Submit" />
			</form>
			<p>Note: files with the same name with overwrite any existing files.</p>
			"""

		con.commit()
		cur.close()
		con.close()
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
	 
	return response(environ, start_response)

# Configure the SessionMiddleware
import geo.sess
importlib.reload(geo.sess)
session_opts = geo.sess.session_opts
application = SessionMiddleware(application, session_opts)
