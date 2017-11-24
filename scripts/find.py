def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	post = request.POST
	page='Lam on dung chay cai nay nua ma'
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


