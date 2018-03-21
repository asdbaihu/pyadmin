from beaker.middleware import SessionMiddleware

def application(environ, start_response):
from webob import Request, Response
from datetime import datetime
	request = Request(environ)
	post = request.POST
	# Get the session object from the environ
	session = environ['beaker.session']

	# Check to see if a value is in the session
	user = 'logged_in' in session

	# Set some other session variable
	#session['user_id'] = 10
	user_id = 'user_id' in session
	page="testing %s "%(user)

	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)

# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires':True, #True hoac 300 3000 ..v.v..v
#	'session.data_dir': './data',
	'session.data_dir': '/tmp',
	'session.auto': True    
}
application = SessionMiddleware(application, session_opts)
