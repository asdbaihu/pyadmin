def application(environ, start_response):
	import cgi,os,sys,csv
	from datetime import datetime
	#import postgresql.driver as pg_driver
	from webob import Request, Response
	#db = pg_driver.connect(host='localhost',user='postgres',password='12345678',database='Google_qc',port=5432)
	request = Request(environ)
	
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = conn.cursor()


	#params = request.params
	try: # Windows needs stdio set for binary mode.
		import msvcrt
		msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		msvcrt.setmode (1, os.O_BINARY) # stdout = 1
	except ImportError:
		pass
	def fbuffer(f, chunk_size=100000):
		while True:
			chunk = f.read(chunk_size)
			if not chunk: break
			#page = chunk		
	if environ['REQUEST_METHOD'] == 'POST':
		#post = cgi.FieldStorage(
		#	fp=environ['wsgi.input'],
		#	environ=environ,
		#	keep_blank_values=True
		#)
		post = request.POST
		fileitem = post['file']
		account = request.headers["account"]#.replace("A","")
		time = request.headers["time"]
		table_name = time.replace(" ","_").replace(":","_")
		year = table_name.split("_")[3]
		day = int(table_name.split("_")[2])
		month = int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').month)
		#year = int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').year)
		#day = int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').day)
		
		#hour= int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').hour)
		#minute = int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').minute)
		#second = int(datetime.strptime(time,'%a %b %d %Y %H:%M:%S').second)
		if 'file' in post:	
			filefield = post['file']
			if not isinstance(filefield, list):
				filefield = [filefield]
			for fileitem in filefield:
			# #account = request.headers["account"]
			# #time = request.headers["time"]
				if fileitem.filename:
					page =""
					# strip leading path from file name to avoid directory traversal attacks
					fn = os.path.basename(fileitem.filename)
					open('/tmp/file_upload/'+ fn + account + '%s'%(table_name) , 'wb').write(fileitem.file.read())
					with open('/tmp/file_upload/'+fn + account + '%s'%(table_name),'r',encoding='utf-8') as csvfile:
						spamreader = list(csv.reader(csvfile,delimiter=';',quotechar='"'))[1][8]
					if spamreader !=None:	
						years = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').year)	
						months = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').month)
						days = int(datetime.strptime(spamreader,'%a %b %d %Y %H:%M:%S').day)						
					cur.execute("""create table if not exists omnivore_%s_%s_%s
								(
								id serial8 primary key,
no text,agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp, process_time numeric ,img_id text,
								update_time timestamp default now() )"""%(years,months,days))
					# page += """copy qc_project_csv%s%s(no ,agent , module ,domain ,title ,link , quest , answer , time, process_time) from 'c:/wsgi_app/file_upload/%s%s%s_%s_%s_%s_%s_%s' delimiter ';' CSV HEADER escape '\\' quote '"' """%(year,month,fn,account,year,month,day,hour,minute,second)

								
					try:
						cur.copy_expert("""copy omnivore_%s_%s_%s(no ,agent , module ,domain ,title ,link , quest , answer , time , process_time, img_id ) from '/tmp/file_upload/%s%s%s' delimiter ';' CSV HEADER escape '\\' quote '"' """%(years,months,days,fn,account,table_name),sys.stdout)
						#db.execute("""delete  from qc_project_csv%s%s where agent='%s' and not update_time =(select max(update_time) from qc_project_csv%s%s)  """%(year,month,account,year,month))
						#db.execute("""update qc_project_csv%s%s set status =null ,price =null,currency=null,condition=null,availability=null where status ='' or price ='' or currency='' or condition ='' or availability=''"""%(year,month))
						
						#cur.execute("select count(*) from qc_project_csv%s%s where process_time='NaN'"%(year,month))
						#ps3 = cur.fetchone()	
						#if int(ps3[0]) > 0:
						#3	cur.execute("""update qc_project_csv%s%s set process_time='10' where process_time='NaN'"""%(year,month))							
						page += ' file was uploaded %s%s%s'%(fn,account,table_name)				
						#page += 'The file "' + fn + '" was uploaded and import successfully'
						#db.execute("""insert into log_import_csv(filename,agent) values('%s','%s')"""%(fn,username))
						
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
				
			cur.execute("update omnivore_%s_%s_%s set answer='' where answer='unselected'"%(years,months,days))		
	else:
		page = u"""
			<html>
			<head><title>Upload</title></head>
			<body>
			<form name="test" method="post" action="upload_file2a" enctype="multipart/form-data">
				Import file csv : <input type="file" name="file" multiple/> <br />
				<p>--------------</p>
			
				<!--Upload file anh va excel:<br />
				<input type="file" name="file2" multiple/><br />
				<input type="file" name="file3" multiple/><br />-->
				<input type="submit" name="submit" value="Submit" />
			</form>
			<p>Note: files with the same name with overwrite any existing files.</p>
			</body>
			</html>
			"""

	conn.commit()
	cur.close()
	conn.close()			
	

 
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


