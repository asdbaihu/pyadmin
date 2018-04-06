def application(environ, start_response):
    import os, sys, cgi
    import postgresql.driver as pg_driver
    from webob import Request, Response
    db = pg_driver.connect(host='localhost', user='postgres', password='12345678', database='omnivore', port=5432)
    # request = Request(environ)
    # params = request.params
    # post = request.POST
    page = ""
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=True
        )
        table = post.getvalue('table')
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
                    # page += 'File was uploaded %s roi sao %s'%(fn,table)
                    db.execute("""create table if not exists %s
								(
								id serial8 primary key,
agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp,update_time timestamp default now() )""" % (
                        table))
                    try:
                        # db.execute("""copy %s(no,agent, module,domain,title,link, quest, answer, time, process_time,img_id) from '/usr/local/www/apache24/wsgi-scripts/file_upload/%s' delimiter ';' CSV HEADER quote '"' """%(table,fn))
                        db.execute(
                            """copy %s(agent, module,domain,title,link, quest, answer, time) from '/tmp/file_upload/%s' delimiter ';' CSV HEADER escape '\\' quote '"' """ % (
                            table, fn))
                        # db.execute("""update qc_project_csv%s%s set status =null ,price =null,currency=null,condition=null,availability=null where status ='' or price ='' or currency='' or condition ='' or availability=''"""%(year,month))

                        page += 'The file "' + fn + '" was uploaded and import into table %s successfully! <br />' % table
                    # db.execute("""insert into log_import_csv(filename,agent) values('%s','%s')"""%(fn,username))

                    # page += "Upload file sucessfull"
                    # #xoa file vua gui len
                    # try:
                    # os.remove('c:/wsgi_app/file_upload/' + fn)
                    # except OSError:
                    # pass
                    except IOError as err:
                        page += "I/O error: {0}".format(err)
                    except ValueError:
                        page += "Could not import data file csv to database"
                        raise
    # db.execute("update omnivore_%s_%s_%s set answer='' where answer='unselected'"%(year,month,day))
    else:
        page = u"""
			<html>
			<head><title>Upload Z</title></head>
			<body>
			<h1>Upload file csv  bo dem  </h1>
			<form name="test" method="post" action="" enctype="multipart/form-data">
			File: <input type="file" name="file" multiple/><br />
			Table :<input type="text" name="table" value='' required/> (omnivore_nam_thang_ngay omnivore_2015_5_7 : bang csv 2015-5-7 ) <br />
				  <input type="submit" name="submit" value="Submit" />
			</form>
			<p>Note: files with the same name with overwrite any existing files.</p>
			</body>
			</html>
			"""

    db.close()

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)
