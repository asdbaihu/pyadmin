def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	#request.headers['Cookie'] = ‘test=value’
	from http.cookies import  SimpleCookie
	cookie = SimpleCookie()
	login_form = """
	
	<!doctype html>
		<html>
			<head>
                <title> Login </title>
                
				<script src="bootstrap/js/bootstrap-3.3.4.min.js"></script>
				<link rel="stylesheet" href="bootstrap/v3/css/bootstrap-3.3.4.min.css">
            </head>	

		<body>
			<h1>Google QC Report</h1>
				<p>Ban chua dang nhap dung username hoac password. Ban can phai dang nhap lai</p>
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
							<h4 class="modal-title">Login</h4>
						</div>
						<div class="modal-body">
						<form class="form-horizontal" role="form" action = 'login3.py' method='post'>
							<div class="form-group">
								<label for="inputEmail1" class="col-lg-4 control-label">User name</label>
								<div class="col-lg-5">
									<input type="text" class="form-control" id="inputuser1" name='username' placeholder="user name">
								</div>
							</div>
								<div class="form-group">
									<label for="inputPassword1" class="col-lg-4 control-label">Password</label>
									<div class="col-lg-5">
										<input type="password" class="form-control" id="inputPassword1" name='password' placeholder="Password">
									</div>
								</div>
								<div class="form-group">
								<div class="col-lg-offset-4 col-lg-5">
									<div class="checkbox">
										<label>
											<input type="checkbox"> Remember me
										</label>
									</div>
								</div>
							</div>
							<div class="form-group">
								<div class="col-lg-offset-4 col-lg-5">
									<button type="submit" class="btn btn-default">Sign in</button>
								</div>
							</div>
						</form>
					</div>
					<div class="modal-footer">

					</div>
				</div><!-- /.modal-content -->
			</div><!-- /.modal-dialog -->		

		</body>
	</html>"""
	
	if not 'HTTP_COOKIE' in environment:
		page= login_form
	else:
		cookie.load(environment['HTTP_COOKIE'])		
		if not 'username' in cookie:
			page=login_form
		else:
		
			username = cookie['username'].value
			password = cookie['password'].value
			import psycopg2
			import psycopg2.extras
			import psycopg2.extensions
			
			try:
				conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
			except:
				page = "Can not access database"	
			cur = conn.cursor()
			
			cur.execute("Select username,account_password,account_level from account where username= %s and account_password = %s ",(username,password))
			ps = cur.fetchall()
			if len(ps) == 0:
				page = login_form
			else:
				if ps[0][2] == 2:
					from datetime import datetime,date
					year_today = date.today().year
					month_today = date.today().month
					day_today = date.today().day
					if not 'display' in post:
						display = 50
					else:
						display = post['display']					
					if not 'date_time' in post:
						date_time = '%s/%s/%s'%(month_today,day_today,year_today)
					else:
						date_time = post['date_time']
						date_time_input = datetime.strptime(date_time, '%m/%d/%Y')	
						month_input = date_time_input.month
						day_input = date_time_input.day
						year_input = date_time_input.year	
					if not 'table' in post:
						table = 'example'
					else:
						table = post['table']
					if not 'agent' in post:
						agent=''
					else:
						if post['agent']=='admin':
							agent=''
						else:
							agent = post['agent']
					if not 'module' in post:
						module =''
					else:
						module = post['module']
					if not 'domain' in post:
						domain =''
					else:
						domain = post['domain']
					if not 'title' in post:
						title = ''
					else:
						title = post['title']
					if not 'link' in post:
						link = ''
					else:
						link = post['link']
					if not 'quest' in post:
						quest=''
					else:
						quest = post['quest']
					if not 'answer' in post:
						answer = 'all'
					else:
						answer = post['answer']		
					import os
					statvfs = os.statvfs('/')
					#cur.execute("""create table a(id serial8 primary key, a text);insert into a(a) values ('a');""")
					cur.execute("""insert into a(a) values ('a');
									insert into a(a) values ('a');""")
					page="""
					<!doctype html>
					<html>
					<head>
						<meta charset='utf-8'>
						<title>Con trong : %s GB</title>

					  <!--
					  Loading Handsontable (full distribution that includes all dependencies apart from jQuery)
					  -->
						<script data-jsfiddle="common" src="../lib/jquery-2.1.3.min.js"></script>
						<script src="bootstrap/js/bootstrap-3.3.4.min.js"></script>
						
						<script type="text/javascript" src="js/jquery.bootpag.min.js"></script>
						<link rel="stylesheet" href="bootstrap/v3/css/bootstrap-3.3.4.min.css">
						<script data-jsfiddle="common" src="../dist/handsontable.full.js"></script>
						<script data-jsfiddle="common" src="../dist/hilitor-utf8.js.js"></script>
						<link data-jsfiddle="common" rel="stylesheet" media="screen" href="../dist/handsontable.full.css">
						
          <style data-jsfiddle="common">
            .handsontable .currentRow {
              background-color: #E7E8EF;
            }

            .handsontable .currentCol {
              background-color: #F9F9FB;
            }
          </style>
					</head>

					<body>"""%round(((((statvfs.f_frsize * statvfs.f_bavail)/1024)/1024)/1024),2)

					page += """
		<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
		<div class="container">
		<div class="navbar-collapse collapse">
		<ul class="nav navbar-nav">"""
					if ps[0][2] == 2:
						cur.execute("""Select id,menu1,link from admin_first_menu order by id""")
						ps_admin_menu1 = cur.fetchall()
						cur.execute("""Select id,menu1,link from first_menu order by id""")
						ps_menu1 = cur.fetchall()

						for row_admin1 in ps_admin_menu1:
							cur.execute("""Select menu2,link from admin_second_menu where first_menu_id = %s order by id """%row_admin1[0])
							ps_admin_menu2 = cur.fetchall()
							if len(ps_admin_menu2)>0:
								page +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row_admin1[2],row_admin1[1])
								page +="""<ul class="dropdown-menu">"""
								for row_admin2 in ps_admin_menu2:
									page +="""<li><a href='%s'>%s</a></li>"""%(row_admin2[1],row_admin2[0])
								page +="""</ul></li>"""
							else:
								page +="""<li><a href='%s'>%s</a></li>"""%(row_admin1[2],row_admin1[1])
						for row1 in ps_menu1:
							cur.execute("""Select menu2,link from second_menu where first_menu_id = %s order by id """%row1[0])
							ps_menu2 = cur.fetchall()
							if len(ps_menu2)>0:
								page +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row1[2],row1[1])
								page +="""<ul class="dropdown-menu">"""
								for row2 in ps_menu2:
									page +="""<li><a href='%s'>%s</a></li>"""%(row2[1],row2[0])
								page +="""</ul></li>"""
							else:
								page +="""<li><a href='%s'>%s</a></li>"""%(row1[2],row1[1])

					else:
						cur.execute("""Select id,menu1,link from first_menu order by id""")
						ps_menu1 = cur.fetchall()
						for row1 in ps_menu1:
							cur.execute("""Select menu2,link from second_menu where first_menu_id = %s order by id """%row1[0])
							ps_menu2= cur.fetchall()
							if len(ps_menu2)>0:
								page +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row1[2],row1[1])
								page +="""<ul class="dropdown-menu">"""
								for row2 in ps_menu2:
									page +="""<li><a href='%s'>%s</a></li>"""%(row2[1],row2[0])
								page +="""</ul></li>"""
							else:
								page +="""<li><a href='%s'>%s</a></li>"""%(row1[2],row1[1])

					page += """</ul>
								</div></div>
								</nav>								
								<br />
								<br />"""


					#statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
					#statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
					#statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
					page += """<h1>O cung con trong : %s GB</h1>
								<p>* <a href='https://172.16.29.6/wsgi/omnivore/demo/emptytmp'> Don dep folder /tmp/file_upload</a></p>
								<p>* <a href='https://172.16.29.6/wsgi/omnivore/demo/table'> Xóa bảng trong CSDL </a></p>
								"""%round(((((statvfs.f_frsize * statvfs.f_bavail)/1024)/1024)/1024),2)



					page +="""	<form method="post" action="">
									Ngay : <input type="text" id="datepicker" name ="date_time" size="30" value = '%s' required>
									<input type="submit" value="Cap nhat" />
									</form>
</body>
</html>
"""%date_time

				else:
					page = login_form
			conn.commit()
			cur.close()
			conn.close()						
			#request.headers['Cookie']
	response = Response(body = page,
	content_type = "text/html",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)
