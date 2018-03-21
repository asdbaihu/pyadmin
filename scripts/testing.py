def application(environ, start_response):
	from webob import Request, Response
	from datetime import datetime
	request = Request(environ)
	post = request.POST
	page="""
<!DOCTYPE html>
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
</html>		
	"""

	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)
