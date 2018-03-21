import logging

# create the logging instance for logging to file only
logger = logging.getLogger('SmartfileTest')

# create the handler for the main logger
file_logger = logging.FileHandler('smartfile_test.log')
NEW_FORMAT = '[%(asctime)s - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
logger.addHandler(file_logger)

# remember that by default, logging will start at 'warning' unless
# we set it manually
logger.setLevel(logging.DEBUG)

def application(environ, start_response):
    import os, sys, cgi

    from webob import Request, Response

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
                    logger.info("Testing fn")
                    open('/tmp/file_upload/' + fn, 'wb').write(fileitem.file.read())
                    # page += 'File was uploaded %s roi sao %s'%(fn,table)
                    try:
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

    else:
        page = """
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

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)
