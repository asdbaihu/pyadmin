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
	session['user_id'] = 10
	
	session.save()
	
	#page="testing %s "%user
	page ="""<!DOCTYPE html>
<html>
<body>
<form action="https://www.w3schools.com/action_page.php">
  First name:<br>
  <input type="text" id="firstName" name="firstname" value="Mickey">
  <br>
  Last name:<br>
  <input type="text" id="lastName" name="lastname" value="Mouse">
  <br><br>
  <input type="submit" value="Submit">
</form> 
<p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>
</body>
</html>	"""

	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)

# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,# hoac 3000 tuong ung 3 giay
#	'session.data_dir': './data',
	'session.data_dir': '/tmp',
	'session.auto': True    
}
application = SessionMiddleware(application, session_opts)
