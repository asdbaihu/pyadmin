from beaker.middleware import SessionMiddleware
import importlib
def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	params = request.params
	post = request.POST
	res = Response()
	from geo.conn import conn
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

		import psycopg2,psycopg2.extras,psycopg2.extensions,importlib
		
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
			#if int(ps[0][2]) == 2:
			import os,sys

			post = request.POST
			table = post['table']

			if 'file' in post:	
				filefield = post['file']
				if not isinstance(filefield, list):
					filefield = [filefield]
				for fileitem in filefield:
				# #account = request.headers["account"]

					if fileitem.filename:
						page =""
						# strip leading path from file name to avoid directory traversal attacks
						fn = os.path.basename(fileitem.filename)
						open('/tmp/file_upload/'+ fn , 'wb').write(fileitem.file.read())
						cur.execute("create table if not exists " + table + " (id serial8 primary key,agent text,url text,link text,tab text,idlab text,label text,inlab int,value text,time timestamp,letter text,confirm text,note text,country text)")
								
						try:
							cur.copy_expert("""copy """ + table +""" (agent,url,link,tab,idlab,label,inlab,value,time) from '/tmp/file_upload/%s' delimiter ';' CSV HEADER escape '\\' quote """%(fn),_io_buffer) #sys.stdout
								
							page += 'THANKS TINH YEU (♥_♥)  \n   '
							
							#page += "Upload file sucessfull"
						# #xoa file vua gui len
							#try:
							#	os.remove('/usr/local/www/apache24/wsgi-scripts/file_upload/' + fn + account + '%s_%s_%s_%s_%s_%s.csv'%(year,month,day,hour,minute,second))
							#except OSError:
							#	pass
						except IOError as err:
							page += "I/O error: {0}".format(err)
						except ValueError:
							page += "Could not import data file csv to database"
							raise
				page = """
					<!doctype html>
							<html>
								<head>
								<meta http-equiv="refresh" content="0; url=/wsgi/apolo/form_csv"/>
									<title> redirect login </title>
								</head>	
							<body>
							</body>
						</html>"""


	conn.commit()
	cur.close()
	conn.close()			
	

 
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
