def application(environ, start_response):
    import cgi, os, sys
    from datetime import datetime
    from webob import Request, Response
    request = Request(environ)

    import psycopg2
    import psycopg2.extras
    import psycopg2.extensions
    conn = psycopg2.connect("host=localhost dbname=omnivore user=postgres password=12345678")
    cur = conn.cursor()

    try:  # Windows needs stdio set for binary mode.
        import msvcrt
        msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
        msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
    except ImportError:
        pass

    def fbuffer(f, chunk_size=100000):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break

    # page = chunk
    if environ['REQUEST_METHOD'] == 'POST':
        post = request.POST
        fileitem = post['file']
        if 'file' in post:
            filefield = post['file']
            if not isinstance(filefield, list):
                filefield = [filefield]
            for fileitem in filefield:
                if fileitem.filename:
                    page = ""
                    # strip leading path from file name to avoid directory traversal attacks
                    fn = os.path.basename(fileitem.filename)
                    open('/tmp/file_upload/' + fn, 'wb').write(fileitem.file.read())

#                     cur.execute("""create table if not exists omnivore_%s_%s_%s
# 								(
# 								id serial8 primary key,
# no text,agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp, process_time numeric,img_id text,
# 								update_time timestamp default now() )""" % (year, month, day))
                    try:
                        # cur.copy_expert(
                        #     """copy omnivore_%s_%s_%s(no ,agent , module ,domain ,title ,link , quest , answer , time , process_time ) from '/tmp/file_upload/%s%s%s' delimiter ';' CSV HEADER escape '\\' quote '"' """ % (
                        #     year, month, day, fn, account, table_name), sys.stdout)

                        page += ' file was uploaded %s' % (fn)

                    except IOError as err:
                        page += "I/O error: {0}".format(err)
                    except ValueError:
                        page += "Could not import data file csv to database"
                        raise

    else:
        page = u"""
			<html>
			<head><title>Upload</title></head>
			<body>
			<form name="test" method="post" action="upload_file_demo.py" enctype="multipart/form-data">
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

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)
