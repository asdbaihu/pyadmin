from beaker.middleware import SessionMiddleware
import importlib
def application(environ, start_response):
	from webob import Request, Response
	# Get the session object from the environ
	session = environ['beaker.session']
	session.delete()
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
