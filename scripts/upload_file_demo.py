import logging
logging.basicConfig(
    filename='/var/log/pyadmin/runtime.log',
    format='[%(asctime)s] - [%(levelname)s] - %(funcName)s() - %(lineno)d\t - %(message)s',
    level=logging.DEBUG
)

def application(environ, start_response):
    import cgi, os, sys
    from datetime import datetime
    from webob import Request, Response
    request = Request(environ)

    page =""
    post = request.POST

    if 'file' in post:
        filefield = post.getall('file')
        if not isinstance(filefield, list):
            filefield = [filefield]
        for fileitem in filefield:
            if fileitem.filename:
                # strip leading path from file name to avoid directory traversal attacks
                fn = os.path.basename(fileitem.filename)
                open(f'/usr/local/www/apache24/data/{fn}', 'wb').write(fileitem.file.read())
                page += f'upload file {fn} successfull! </br>'
    else:
        page ="""
			<html>
			<head><title>Upload</title></head>
			<body>
			<form name="test" method="post" action="upload_file_demo.py" enctype="multipart/form-data">
				Import file csv : <input type="file" name="file" multiple> <br />
				<p>--------------</p>
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
