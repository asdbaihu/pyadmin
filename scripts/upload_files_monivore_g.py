def application(environment, start_response):
	import os,sys,cgi,csv
	import postgresql.driver as pg_driver
	try:
		db = pg_driver.connect(host='localhost',user='postgres',password='12345678',database='omnivore',port=5432)
	except:
		page = """Can not access database"""		
	from webob import Request, Response
	#request = Request(environ)
	#params = request.params
	#post = request.POST
	from http.cookies import  SimpleCookie
	cookie = SimpleCookie()
	login_form = """
	
	<!doctype html>
		<html>
			<head>
                <title> Login </title>
                
				<script src="../bootstrap/js/bootstrap-3.3.4.min.js"></script>
				<link rel="stylesheet" href="../bootstrap/v3/css/bootstrap-3.3.4.min.css">
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
						<form class="form-horizontal" role="form" action = '../omnivore/demo/login3.py' method='post'>
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
		
			ps = db.prepare("""Select username,account_password,account_level,gmail from account where username= '%s' and account_password = '%s' """%(username.replace("'","''"),password.replace("'","''")))
			if len(ps()) == 0:
				page = login_form
			else:
				if ps()[0][2] == 2:	
					page =""	
					if environment['REQUEST_METHOD'] == 'POST':
						post = cgi.FieldStorage(
							fp=environment['wsgi.input'],
							environment=environment,
							keep_blank_values=True
						)
						table = post.getvalue('table')
						page1=''
						if 'file' in post:	
							filefield = post['file']
							if not isinstance(filefield, list):
								filefield = [filefield]
								
							for fileitem in filefield:
							# #account = request.headers["account"]
							# #time = request.headers["time"]
								if fileitem.filename:
									
									# strip leading path from file name to avoid directory traversal attacks
									fn = os.path.basename(fileitem.filename)
									open('/tmp/file_upload/' + fn, 'wb').write(fileitem.file.read())
									#page += 'File was uploaded %s roi sao %s'%(fn,table)
									from datetime import datetime
									with open('tmp/file_upload/'+fn,'r',encoding='utf-8') as csvfile:
										spamreader = list(csv.reader(csvfile,delimiter=';',quotechar='"'))[1][8]
									years = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').year)	
									months = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').month)
									days = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').day)					
									db.execute("""create table if not exists omnivore_%s_%s_%s
												(
												id serial8 primary key,
				no text,agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp, process_time numeric,img_id text,
												update_time timestamp default now() )"""%(years,months,days))
									db = pg_driver.connect(host='localhost',user='postgres',password='12345678',database='omnivore',port=5432)								
									try:
										db.execute("""copy omnivore_%s_%s_%s(no,agent, module,domain,title,link, quest, answer, time, process_time,img_id) from '/tmp/file_upload/%s' delimiter ';' CSV HEADER escape '\\' quote '"' """%(years,months,days,fn))
										#db.execute("""update qc_project_csv%s%s set status =null ,price =null,currency=null,condition=null,availability=null where status ='' or price ='' or currency='' or condition ='' or availability=''"""%(year,month))
										
										page1 += 'The file "' + fn + '" was uploaded and import successfully! <br />'
										#db.execute("""insert into log_import_csv(filename,agent) values('%s','%s')"""%(fn,username))
										
										#page += "Upload file sucessfull"
									# #xoa file vua gui len
										# try:
											# os.remove('c:/wsgi_app/file_upload/' + fn)
										# except OSError:
											# pass
									except IOError as err:
										page1 += "I/O error: {0}".format(err)
									except ValueError:
										page1 += "Could not import data file csv to database"
										raise		
						page +="""
				<html>
				  <head>
					<title>IU Webmaster redirect</title>
					<META http-equiv="refresh" content="25;URL=upload_files_monivore_g">
				  </head>
				  <body bgcolor="#ffffff">
					<center>%s 
					You will be redirected to the new location automatically in 25 seconds. If you can not wait , click <a href="upload_files_monivore_g"> Upload file csv</a>
					</center>
				  </body>
				</html>
						
						"""%page1
						
						cur.execute("update omnivore_%s_%s_%s set answer='' where answer='unselected'"%(years,months,days))			
					else:
						page = u"""
							<html>
							<head><title>Upload</title></head>
							<body>
							<h1>Upload file csv cua bo dem beta Q . Khong can dat ten bang </h1>
							<p> 
							<form name="test" method="post" action="" enctype="multipart/form-data">
							Chon file (co the chon nhieu file mot luc): <input type="file" name="file" multiple/><br />
							<!--Table :<input type="text" name="table" value='' required/> (om_2015_5_7 : bang csv 2015-5-7 , vi du minh hoa, ban co the lay ten bang bat ky) <br />
								  --><input type="submit" name="submit" value="Submit" />
							</form>
							<p>Note: files with the same name with overwrite any existing files.</p
							<h1> Upload file csv cho bo dem beta G tro len <a href='upload_files_monivore_g.py'>Tai day</a></h1>
							</body>
							</html>
							"""

				else:
					page = login_form
	db.close()			
	

 
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)


